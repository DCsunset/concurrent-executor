# concurrent-ssh
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
from .executor import SshExecutor
from .signal_handler import SignalHandler
from .io import get_stdin_stream
from aiostream import stream
from functools import reduce
from rich.console import Console
import argparse
import asyncio
import sys

console = Console(highlight=False)

async def main():
	parser = argparse.ArgumentParser(
		description="Executing commands using SSH concurrently on multiple hosts",
	)
	parser.add_argument("-H", "--hosts", nargs="+", required=True, help="a list of hosts to execute command on")
	parser.add_argument("-o", "--options", default="", help="extra options passed to ssh command. use a single string")
	parser.add_argument("cmd", nargs="+", help="command to run")
	parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
	args = parser.parse_args()

	executor = SshExecutor(args.hosts, args.options)
	await executor.run(" ".join(args.cmd))
	
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

	# The max host length (for padding)
	host_len = 0
	for h in args.hosts:
		if len(h) > host_len:
			host_len = len(h)
	
	# use async with to ensure it is cleaned up correctly
	async with stream.merge(stdout, stderr).stream() as s:
		async for host_out, is_stdout in s:
			host, out = host_out
			out = out.decode().rstrip()
			if is_stdout:
				console.print(f"[bright_black]{host:{host_len}} |[/bright_black] {out}")
			else:
				console.print(f"[bright_black]{host:{host_len}}[/bright_black] [red]|[/red] {out}")
	
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
