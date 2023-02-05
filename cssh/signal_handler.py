import signal
from enum import Enum

class SignalHandler:
	def __init__(self, callback, signals=[signal.SIGTERM, signal.SIGINT]):
		# How many times it receives SIGINT or SIGTERM
		self.counter = 0
		self.callback = callback

		# register handlers
		for sig in signals:
			signal.signal(sig, self.signal_handler)
	
	def signal_handler(self, _sig, _frame):
		self.counter += 1
		self.callback(self.counter)

