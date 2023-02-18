# Changelog

All notable changes to this project will be documented in this file. See [commit-and-tag-version](https://github.com/absolute-version/commit-and-tag-version) for commit guidelines.

## [1.0.1](https://github.com/DCsunset/concurrent-executor/compare/v1.0.0...v1.0.1) (2023-02-18)


### Bug Fixes

* fix logging in cli ([fad30c2](https://github.com/DCsunset/concurrent-executor/commit/fad30c2b672b125cab5afef5a4bd0cb504f6edbe))

## [1.0.0](https://github.com/DCsunset/concurrent-executor/compare/v0.3.1...v1.0.0) (2023-02-17)


### ⚠ BREAKING CHANGES

* rename package to concurrent-executor
* extract general Executor class and add bin option

### Features

* add cexec to execute arbitrary command using Executor ([2d9e3f3](https://github.com/DCsunset/concurrent-executor/commit/2d9e3f31859b5d00dac989f07a1e9826ebe12ca0))
* extract general Executor class and add bin option ([f3e87d0](https://github.com/DCsunset/concurrent-executor/commit/f3e87d0658c9db8ec0ea0f38db1e5768feaec641))
* rename package to concurrent-executor ([91b4ee3](https://github.com/DCsunset/concurrent-executor/commit/91b4ee39061c062346705accdb412b8c72e50241))
* support string interpolation for ssh command ([4645a27](https://github.com/DCsunset/concurrent-executor/commit/4645a2743c1e5a5ed8f1ca667c81730b1c6916c1))
* support template command in Executor ([f98de94](https://github.com/DCsunset/concurrent-executor/commit/f98de945bf25ce7ef1d712845327f0a1fb60f9c5))


### Bug Fixes

* remove default template command and add default values to help message ([52f640a](https://github.com/DCsunset/concurrent-executor/commit/52f640ae73989fb101c7c2e1b38e0526642164fd))

## [0.3.1](https://github.com/DCsunset/concurrent-executor/compare/v0.3.0...v0.3.1) (2023-02-13)


### Bug Fixes

* strip whitespaces and empty lines in host file ([75ec007](https://github.com/DCsunset/concurrent-executor/commit/75ec0070d5f5d3c24e36d6c105990ac91887069e))

## [0.3.0](https://github.com/DCsunset/concurrent-executor/compare/v0.2.2...v0.3.0) (2023-02-13)


### Features

* support read hosts from file ([9cd47a0](https://github.com/DCsunset/concurrent-executor/commit/9cd47a00e1ae1ea1985879f6c367a285e60d967f))

## [0.2.2](https://github.com/DCsunset/concurrent-executor/compare/v0.2.1...v0.2.2) (2023-02-10)


### Bug Fixes

* add min python version in setup.py ([07d24ed](https://github.com/DCsunset/concurrent-executor/commit/07d24ed5441e4f660a32320d5bc5680212615b6d))

## [0.2.1](https://github.com/DCsunset/concurrent-executor/compare/v0.1.0...v0.2.1) (2023-02-06)


### Features

* handle signals to terminate or kill processes ([f26cbfa](https://github.com/DCsunset/concurrent-executor/commit/f26cbfa2a80a32c8d32347f3ac312eb667b0a5e2))


### Bug Fixes

* avoid writing to finished process to prevent deadlock ([8130e7d](https://github.com/DCsunset/concurrent-executor/commit/8130e7d2d6281af14a862b0036801e3bb5b12497))
* output error to stderr ([3b3b9e0](https://github.com/DCsunset/concurrent-executor/commit/3b3b9e0f2796b5e50390ce4a63d66a2c5f91b222))
* supoprt piping stdin correctly ([16a5052](https://github.com/DCsunset/concurrent-executor/commit/16a5052ed2acb346adb85d8c7f33e34e8067ebd8))

## [0.2.0](https://github.com/DCsunset/concurrent-executor/compare/v0.1.0...v0.2.0) (2023-02-05)


### Features

* handle signals to terminate or kill processes ([276db94](https://github.com/DCsunset/concurrent-executor/commit/276db9477a959c88ef13379dbdde7728d1186c02))


### Bug Fixes

* avoid writing to finished process to prevent deadlock ([357eaf7](https://github.com/DCsunset/concurrent-executor/commit/357eaf7e3eb1118328fc4626e60638054fb63e2e))
* supoprt piping stdin correctly ([fd2c021](https://github.com/DCsunset/concurrent-executor/commit/fd2c02132e896e94c735fea50b17519371cd0935))

## 0.1.0 (2023-02-04)


### Features

* add highlighting for errors and host names ([5087471](https://github.com/DCsunset/concurrent-executor/commit/508747174048a238e7489c899b998e7eff5247af))
* add stdin piping and wait until all finished ([c49bfce](https://github.com/DCsunset/concurrent-executor/commit/c49bfcef1199731d4b8e152d82666d196a4af6b4))
* allow passing extra options ([bb0f0c0](https://github.com/DCsunset/concurrent-executor/commit/bb0f0c04a813dd43b449b4c83a280c41ebef0209))


### Bug Fixes

* add dependencies to setup.py ([835fb96](https://github.com/DCsunset/concurrent-executor/commit/835fb96586ec77ff83b1ccab56faf140a4db17f1))
* add version flag for cli ([2889a9a](https://github.com/DCsunset/concurrent-executor/commit/2889a9a933e3bf218de19dd6d2cd4756b218c97a))
* align host prefix ([7f863ff](https://github.com/DCsunset/concurrent-executor/commit/7f863ff3d70297f84ef0fe0edb70a212cf5ab6db))
* exit with non-zero code if any command fails ([ea915a4](https://github.com/DCsunset/concurrent-executor/commit/ea915a4aa96d5fe3993ed6c89139bd54fd660f36))
