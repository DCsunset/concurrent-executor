# cssh

[![PyPI](https://img.shields.io/pypi/v/cssh)](https://pypi.org/project/cssh/)

## Installation

```sh
pip install cssh
# Or from the latest GitHub version
pip install git+https://github.com/DCsunset/cssh

```

## Usage

Use `-H` or `--hosts` to specify the hosts to run the commands on:

```sh
cssh -H <host1> <host2> .... <host_n> -- <command>
# Or pass extra ssh options
cssh -o="-q -4" -H <host1> <host2> .... <host_n> -- <command>
```

Note that `--` is necessary to separate the options and the command.
For `-o/--options` to work correctly, use `=` to prevent it from being parsed as another option.


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

    cssh
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


