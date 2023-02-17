import asyncio
import sys

"""
convert stdin to asyncio StreamReader
"""
async def get_stdin_stream():
	loop = asyncio.get_event_loop()
	reader = asyncio.StreamReader()
	protocol = asyncio.StreamReaderProtocol(reader)
	await loop.connect_read_pipe(lambda: protocol, sys.stdin)
	return reader
