# concurrent-ssh

[![PyPI](https://img.shields.io/pypi/v/concurrent-ssh)](https://pypi.org/project/concurrent-ssh/)

Executing commands with ssh concurrently on multiple hosts using asyncio

## Installation

```sh
pip install concurrent-ssh
# Or from the latest GitHub version
pip install git+https://github.com/DCsunset/concurrent-ssh

```

## Usage

**Note**: ensure that `ssh` is in your `PATH` environment variables.

### CLI

Use `-H` or `--hosts` to specify the hosts to run the commands on:

```sh
cssh -H <host1> <host2> .... <host_n> -- <command>
# Or pass extra ssh options
cssh -o="-q -4" -H <host1> <host2> .... <host_n> -- <command>
```

Note that `--` is necessary to separate the options and the command.
For `-o/--options` to work correctly, use `=` to prevent it from being parsed as another option.

The standard input (stdin) of the `cssh` process is piped to the stdin of every spawned processes.
Upon receiving one `SIGINT` (including keyboard interrupt) or `SIGTERM`, `cssh` will send `SIGTERM` to all spawned processes.
Upon receiving more than one of them, `cssh` will instead send `SIGKLL` to kill all spawned processes.

### Library

It can also be used as a library:

```python
import asyncio
from cssh.executor import SshExecutor

async def main():
  hosts = ["host1", "host2"]
  executor = SshExecutor(hosts)
  # running concurrently
  await executor.run("some_command --test")

  # access stdout for all hosts (or stderr)
  async for host, out in executor.stdout:
    print(f"{host}: {out}")

	# wait until all finished
	ret_codes = await executor.wait()
  
asyncio.run(main())
```

See more usage in `cssh/cli.py`.

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

    concurrent-ssh
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


