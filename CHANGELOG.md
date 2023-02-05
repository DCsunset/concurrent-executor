# Changelog

All notable changes to this project will be documented in this file. See [commit-and-tag-version](https://github.com/absolute-version/commit-and-tag-version) for commit guidelines.

## [0.2.0](https://github.com/DCsunset/concurrent-ssh/compare/v0.1.0...v0.2.0) (2023-02-05)


### Features

* handle signals to terminate or kill processes ([276db94](https://github.com/DCsunset/concurrent-ssh/commit/276db9477a959c88ef13379dbdde7728d1186c02))


### Bug Fixes

* avoid writing to finished process to prevent deadlock ([357eaf7](https://github.com/DCsunset/concurrent-ssh/commit/357eaf7e3eb1118328fc4626e60638054fb63e2e))
* supoprt piping stdin correctly ([fd2c021](https://github.com/DCsunset/concurrent-ssh/commit/fd2c02132e896e94c735fea50b17519371cd0935))

## 0.1.0 (2023-02-04)


### Features

* add highlighting for errors and host names ([5087471](https://github.com/DCsunset/concurrent-ssh/commit/508747174048a238e7489c899b998e7eff5247af))
* add stdin piping and wait until all finished ([c49bfce](https://github.com/DCsunset/concurrent-ssh/commit/c49bfcef1199731d4b8e152d82666d196a4af6b4))
* allow passing extra options ([bb0f0c0](https://github.com/DCsunset/concurrent-ssh/commit/bb0f0c04a813dd43b449b4c83a280c41ebef0209))


### Bug Fixes

* add dependencies to setup.py ([835fb96](https://github.com/DCsunset/concurrent-ssh/commit/835fb96586ec77ff83b1ccab56faf140a4db17f1))
* add version flag for cli ([2889a9a](https://github.com/DCsunset/concurrent-ssh/commit/2889a9a933e3bf218de19dd6d2cd4756b218c97a))
* align host prefix ([7f863ff](https://github.com/DCsunset/concurrent-ssh/commit/7f863ff3d70297f84ef0fe0edb70a212cf5ab6db))
* exit with non-zero code if any command fails ([ea915a4](https://github.com/DCsunset/concurrent-ssh/commit/ea915a4aa96d5fe3993ed6c89139bd54fd660f36))
