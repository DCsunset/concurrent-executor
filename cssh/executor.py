# cssh
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

import asyncio
from aiostream import stream

class SshExecutor:
	"""
	Execute multiple ssh commands in parallel
	"""
	def __init__(self, hosts: list[str], sshOptions: str = ""):
		self.hosts = hosts
		self.sshOptions = sshOptions
		self.processes = []
	
	"""
	Run ssh commands in parallel
	"""
	async def run(self, command: str):
		awaitable_processes = []
		for host in self.hosts:
			p = asyncio.subprocess.create_subprocess_shell(
				f"ssh {host} {self.sshOptions} -- {command}",
				stdin=asyncio.subprocess.PIPE,
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.PIPE
			)
			awaitable_processes.append(p)

		self.processes = await asyncio.gather(*awaitable_processes)
		
	"""
	Wait for all commands to finish
	Return a list of return codes
	"""
	async def wait(self) -> list[int]:
		awaitables = [] 
		for p in self.processes:
			awaitables.append(p.wait())
		return_codes = await asyncio.gather(*awaitables)
		return return_codes
	
	async def write_stdin(data):
		awaitables = []
		for p in self.processes:
			p.stdin.write(data)
			awaitables.append(p.stdin.drain())

		await asyncio.gather(*awaitables)
	
	"""
	Get an async iterator to lines in stdout: (host, stdout_line)
	"""
	def get_stdout(self):
		stdouts = []
		for i, p in enumerate(self.processes):
			# must capture the current host by assigning it to h
			stdouts.append(stream.map(p.stdout, lambda v, h=self.hosts[i]: (h, v)))
		return stream.merge(*stdouts)
		
	"""
	Get an async iterator to lines in stderr: (host, stderr_line)
	"""
	def get_stderr(self):
		stderrs = []
		for i, p in enumerate(self.processes):
			# must capture the current host by assigning it to h
			stderrs.append(stream.map(p.stderr, lambda v, h=self.hosts[i]: (h, v)))
		return stream.merge(*stderrs)

	"""
	Terminate all commands
	"""
	def terminate(self):
		for p in self.processes:
			p.terminate()

	"""
	Kill all commands
	"""
	def kill(self):
		for p in self.processes:
			p.kill()

	"""
	Send signal all commands
	"""
	def send_signal(self, sig):
		for p in self.processes:
			p.send_signal(sig)

