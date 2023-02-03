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
		self.processes = await asyncio.gather(
			# create subprocess for each host
			*map(lambda h: asyncio.subprocess.create_subprocess_shell(
				f"ssh {h} {self.sshOptions} -- {command}",
				stdin=asyncio.subprocess.PIPE,
				stdout=asyncio.subprocess.PIPE,
				stderr=asyncio.subprocess.PIPE
			), self.hosts)
		)
		
	"""
	Wait for all commands to finish
	Return a list of return codes
	"""
	async def wait(self) -> list[int]:
		return_codes = await asyncio.gather(
			*map(lambda p: p.wait(), self.processes)
		)
		return return_codes

	"""
	Write data to all stdins
	"""
	async def write_stdin(self, data):
		for p in self.processes:
			p.stdin.write(data)
			# wait until all consumed
		await asyncio.gather(*map(
			lambda p: p.stdin.drain(),
			self.hosts
		))


	"""
	Use an stream (iterator) to pipe to all stdins
	It can be async by setting asynchronous to True
	"""
	async def pipe_stdin(self, it, asynchronous=False):
		if asynchronous:
			async for data in it:
				# wait until all stdins drain
				await self.write_stdin(data)
		else:
			for data in it:
				# wait until all stdins drain
				await self.write_stdin(data)

	
	"""
	Get a stream (async iterator) to lines in stdout: (host, stdout_line)
	"""
	def get_stdout(self):
		return stream.merge(
			*map(
				lambda h, p: stream.map(
					p.stdout,
					lambda v: (h, v)
				),
				self.hosts,
				self.processes
			)
		)
		
	"""
	Get an async iterator to lines in stderr: (host, stderr_line)
	"""
	def get_stderr(self):
		return stream.merge(
			*map(
				lambda h, p: stream.map(
					p.stderr,
					lambda v: (h, v)
				),
				self.hosts,
				self.processes
			)
		)

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

