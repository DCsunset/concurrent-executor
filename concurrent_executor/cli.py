# concurrent-executor
# Copyright (C) 2023 DCsunset
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from ._version import __version__
from .executor import SshExecutor, Executor
from .signal_handler import SignalHandler
from .io import get_stdin_stream
from aiostream import stream
from functools import reduce
from rich.console import Console
import argparse
import asyncio
import sys

# handle I/O, signals and return codes
async def handle_executor(executor: Executor, stdout_transformer, stderr_transformer):
	console = Console(highlight=False)
	err_console = Console(highlight=False, stderr=True)
	
	def signal_callback(counter):
		if counter == 1:
			console.print(f"[bright_yellow]Terminating all processes...[/bright_yellow]")
			executor.terminate()
		else:
			# send more than twice to kill all processes
			console.print(f"[bright_red]Killing all processes...[/bright_red]")
			executor.kill()

	_signal_handler = SignalHandler(signal_callback)

	# pipe stdin to all processes in the background
	stdin_reader = await get_stdin_stream()
	stdin_task = asyncio.create_task(executor.pipe_stdin(stdin_reader))

	stdout = stream.map(executor.get_stdout(), lambda v: (v, True))
	stderr = stream.map(executor.get_stderr(), lambda v: (v, False))
	
	# use async with to ensure it is cleaned up correctly
	async with stream.merge(stdout, stderr).stream() as s:
		async for output, is_stdout in s:
			index, out = output
			out = out.decode().rstrip()
			if is_stdout:
				console.print(stdout_transformer(index, out))
			else:
				err_console.print(stderr_transformer(index, out))
	
	# return code
	ret = 0
	# wait until all finished
	ret_codes = await executor.wait()
	if not stdin_task.done():
		stdin_task.cancel()
	for r in ret_codes:
		# use the first non-zero code
		if r != 0:
			ret = r

	return ret


# concurrent ssh
async def cssh_main():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		description="Executing commands using SSH concurrently on multiple hosts",
	)
	parser.add_argument("-b", "--bin", default="ssh", help="custom binary executable to use for ssh")
	parser.add_argument("-f", "--file", help="a file where each line specifies a host to execute command on")
	parser.add_argument("-H", "--hosts", nargs="+", help="a list of hosts to execute command on (appended to the host list in file if both specified)")
	parser.add_argument("-o", "--options", default="", help="extra options passed to ssh command. use a single string")
	parser.add_argument("cmd", nargs="+", help="command to run (can use placeholder `{0}` for the host name)")
	parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
	args = parser.parse_args()

	hosts = []
	if args.file is not None:
		with open(args.file, "r") as f:
			for line in f:
				# strip whitespaces
				h = line.strip()
				if h:
					hosts.append(h)

	if args.hosts is not None:
		hosts.extend(args.hosts)
	
	if len(hosts) == 0:
		err_console.print("Error: no host specified")
		sys.exit(1)

	# The max host length (for padding)
	host_len = 0
	for h in hosts:
		if len(h) > host_len:
			host_len = len(h)

	executor = SshExecutor(
		hosts,
		sshOptions=args.options,
		sshBin=args.bin
	)

	await executor.run(" ".join(args.cmd))

	return await handle_executor(
		executor,
		stdout_transformer=lambda i, out: f"[bright_black]{hosts[i]:{host_len}} |[/bright_black] {out}",
		stderr_transformer=lambda i, out: f"[bright_black]{hosts[i]:{host_len}}[/bright_black] [bright_red]|[/bright_red] {out}",
	)
	

# concurrent exec
async def cexec_main():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		description="Executing multiple commands concurrently using template command",
	)
	parser.add_argument("-f", "--file", help="a file where each line specifies a variable to use in template command")
	parser.add_argument("-V", "--vars", nargs="+", help="a list of variables used in the template command (appended to the variable list in file if both specified)")
	parser.add_argument("template", nargs="+", help="template command (each variable generates an individual command)")
	parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
	args = parser.parse_args()

	variables = []
	if args.file is not None:
		with open(args.file, "r") as f:
			for line in f:
				# strip whitespaces
				h = line.strip()
				if h:
					variables.append(h)

	if args.vars is not None:
		variables.extend(args.vars)
	
	if len(variables) == 0:
		err_console.print("Error: no variable specified")
		sys.exit(1)

	# The max var length (for padding)
	var_len = 0
	for v in variables:
		if len(v) > var_len:
			var_len = len(v)

	executor = Executor(variables)

	await executor.run(" ".join(args.template))

	return await handle_executor(
		executor,
		stdout_transformer=lambda i, out: f"[bright_black]{variables[i]:{var_len}} |[/bright_black] {out}",
		stderr_transformer=lambda i, out: f"[bright_black]{variables[i]:{var_len}}[/bright_black] [bright_red]|[/bright_red] {out}",
	)
		