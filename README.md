# concurrent-executor

[![PyPI](https://img.shields.io/pypi/v/concurrent-executor)](https://pypi.org/project/concurrent-executor/)

Executing commands with ssh concurrently on multiple hosts using asyncio

## Installation

```sh
pip install concurrent-executor
# Or from the latest GitHub version
pip install git+https://github.com/DCsunset/concurrent-executor

```

## CLI Usage

All the following tools can handle signals as follows:

* Upon receiving one `SIGINT` (including keyboard interrupt) or `SIGTERM`, the program will send `SIGTERM` to all spawned processes.
* Upon receiving more than one of them, the program will instead send `SIGKILL` to kill all spawned processes.

### cssh

`cssh` is a command line tool provided by this package.
It is used to executing commands concurrently on remote servers vis SSH.

Use `-H` or `--hosts` to specify the hosts to run the commands on:

```sh
cssh -H host1 host2 ... host_n -- command
# pass extra ssh options
cssh -o="-q -4" -H host1 host2 ... host_n -- command
# read hosts from file
cssh -f hosts.txt -- command
# string interpolation (to include host name in command by {0})
cssh -H host1 host2 -- command --host {0}
```

Note that `--` is necessary to separate the options and the command.
For `-o/--options` to work correctly, use `=` to prevent it from being parsed as another option.

The standard input (stdin) of the `cssh` process is piped to the stdin of every spawned processes.

For more details, see `cssh -h`.

### cexec

`cexec` is another command line tool provided by this package.
It is used to execute arbitrary shell commands concurrently using template (string interpolation in Python).

The command itself can container placeholder in strings: (See [Python string interpolation](https://peps.python.org/pep-0498/) for more detail.)

```sh
# The variables are a, b, c in the template command
# This command creates 3 directories and write to a file in each directory
cexec -V a b c -- "mkdir {0} && echo 1 > {0}/out"
# Read variables from a file
cexec -f vars.txt -- "mkdir {0} && echo 1 > {0}/out"
# Run different commands directly
cexec -V "cmd1" "cmd2" "cmd3" -- "{}"
```

For more details, see `cexec -h`.

### Library

It can also be used as a library:

```python
import asyncio
from concurrent_executor.executor import SshExecutor

async def main():
  hosts = ["host1", "host2"]
  executor = SshExecutor(hosts)
  # running concurrently
  await executor.run("some_command --test")

  # access stdout for all hosts (or stderr)
  async for index, out in executor.stdout:
    print(f"{host[index]}: {out}")

  # wait until all finished
  ret_codes = await executor.wait()
  
asyncio.run(main())
```

See more usage in `concurrent_executor/cli.py`.

## Development

To set up the development environment,
first clone this repo.

Then it's recommended to use`venv`:

```sh
# suppose PWD is the root dir of the repo
python -m venv venv
# activate the environment``
source venv/bin/activate
pip install -r requirements.txt
```

To deactivate, run `deactivate`.


## License

This project is licensed under AGPL-3.0. Copyright notice:

    concurrent-executor
    Copyright (C) 2023 DCsunset

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


