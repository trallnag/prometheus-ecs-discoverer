# Development

This document describes everything necessary to get started with developing.

## Pre-Commit

Used for maintaining pre-commit hooks.

* <https://pre-commit.com/>
* <https://github.com/pre-commit/pre-commit>

It must be installed on the system level. It is not installed automatically with
Poetry. Also don't forget to execute `pre-commit install` if you haven't
initialized pre-commit before.

Pre-commit is configured via [`.pre-commit-config.yaml`](.pre-commit-config.yaml).
It should automatically run on every commit.

To trigger pre-commit manually, execute `pre-commit run --all-files`.

Pre-commit is also run as part of the CI/CD pipeline.

Several of the defined hooks are local using dependencies installed via Poetry.
This means that you can also use tools like `black`, `yapf`, and `mypy` directly.

## Shell Scripts

In [`./bin`](bin) you can find a bunch of small Shell scripts that provide
useful utilites. Every script has a description that can be accessed with the
`--help` or `-h` option.
