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

import asyncio
from aioconsole.stream import is_pipe_transport_compatible, StandardStreamReader, StandardStreamReaderProtocol, NonFileStreamReader
import sys
import os
import stat


"""
convert stdin to asyncio StreamReader
(see https://github.com/vxgmichel/aioconsole/blob/main/aioconsole/stream.py)
"""
async def get_stdin_stream():
	loop = asyncio.get_event_loop()
	if is_pipe_transport_compatible(sys.stdin):
		# use pipe transport
		reader = StandardStreamReader(loop=loop)
		protocol = StandardStreamReaderProtocol(reader, loop=loop)
		await loop.connect_read_pipe(lambda: protocol, sys.stdin)
	else:
		reader = NonFileStreamReader(sys.stdin, loop=loop)

	return reader
