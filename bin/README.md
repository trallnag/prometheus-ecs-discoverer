# Chart

Project specific Shell scripts. Some of them can be used locally. Some are used
in CI/CD pipelines. Others just are "documentation as code".

## Content

| Element                        | Description                                       |
| ------------------------------ | ------------------------------------------------- |
| [`log.sh`](log.sh)             | Logsh. A minimal POSIX compliant logging library. |
| [`main.sh`](main.sh)           | Script that is sourced by other scripts.          |
| [`pdoc`](pdoc)                 | Generate code docs with pdoc.                     |
| [`test`](test)                 | Run Pytests.                                      |
| [`update-logsh`](update-logsh) | Add or update logsh library.                      |
| [`sm-verify`](sm-verify)       | @semantic-release/exec verify step.               |
