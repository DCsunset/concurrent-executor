# pssh
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

from .executor import SshExecutor
from aiostream import stream
import argparse

async def main():
	parser = argparse.ArgumentParser(
		description="Control audio with ALSA API easily via CLI",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument("-H", "--hosts", nargs="+", required=True, help="a list of hosts to execute command on")
	parser.add_argument("cmd", nargs="+", help="command to run")
	args = parser.parse_args()

	executor = SshExecutor(args.hosts)
	await executor.run(" ".join(args.cmd))


	stdout = stream.map(executor.get_stdout(), lambda v: (v, True))
	stderr = stream.map(executor.get_stderr(), lambda v: (v, False))
	
	# use async with to ensure it is cleaned up correctly
	async with stream.merge(stdout, stderr).stream() as s:
		async for host_out, is_stdout in s:
			host, out = host_out
			out = out.decode().rstrip()
			if is_stdout:
				print(f"{host} | {out}")
			else:
				print(f"{host} x {out}")
