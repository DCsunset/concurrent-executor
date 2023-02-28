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

