# Contributing to clearpath_config

Thanks for your interest in improving `clearpath_config`! This package is the entry point of the
Clearpath ROS 2 system: it parses and validates a robot's `robot.yaml` into a typed Python object
tree that the Clearpath generators consume. Because of that central role, changes here can ripple
through the rest of the stack, so please read the notes below before opening a pull request.

## Getting started

1. Fork the repository and clone your fork.
2. Create a feature branch off `jazzy`:

   ```bash
   git checkout -b my-feature jazzy
   ```

3. Install the pre-commit hooks (one-time setup):

   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Where things live

The top-level [`ClearpathConfig`](clearpath_config/clearpath_config.py) class delegates each
top-level YAML key to a dedicated sub-config module (`system`, `platform`, `links`,
`manipulators`, `mounts`, `sensors`). Shared plumbing (base classes, YAML read/write, type
helpers) lives under [`clearpath_config/common/`](clearpath_config/common). See the
[Architecture section of the README](README.md#architecture) for the full map.

A few conventions to keep in mind:

- Use `read_yaml`/`write_yaml` from `common/utils/yaml.py` rather than calling PyYAML directly,
  so ordering and formatting stay consistent with the generators.
- Each sub-config validates its own section and exposes typed accessors; keep new validation
  close to the section it belongs to.

## Coding style

- Follow [PEP 8](https://peps.python.org/pep-0008/); the CI enforces `flake8` with a
  100-character line limit.
- Docstrings and comments should follow `pep257`.
- Keep changes focused. Avoid unrelated refactors in the same pull request.

## Linting and formatting

This repository uses [pre-commit](https://pre-commit.com/) to run linting and formatting checks
(trailing whitespace, `flake8`, `markdownlint`, YAML checks, and more) before each commit. Run
them against the whole tree before pushing:

```bash
pre-commit run --all-files
```

## Tests

Unit tests are written with **PyTest** following the
[Good Integration Practices](https://docs.pytest.org/en/6.2.x/goodpractices.html#goodpractices).
Every file to be tested has a corresponding file with the same name and the suffix `_test.py`.

Run the suite from the package root:

```bash
cd .../clearpath_config
python3 -m pytest
```

Please add or update tests for any behavior you change, and make sure the full suite passes
before opening a pull request.

## Sample configurations

The [`clearpath_config/sample/`](clearpath_config/sample) folder holds example configurations.
Sample files whose names contain `test` (e.g. `test_a300.yaml`) are the fixtures consumed by
[clearpath_generator_tests](https://github.com/clearpathrobotics/clearpath_generator_tests), so
adding or renaming one changes what CI validates.

## Generator tests

Changes to `clearpath_config` (config structure, defaults, or test samples) may affect the output
of the Clearpath generators. The
[clearpath_generator_tests](https://github.com/clearpathrobotics/clearpath_generator_tests)
repository versions the expected generator output and validates it through CI.

Before merging, ensure a corresponding branch with the **same name** exists in
`clearpath_generator_tests` with regenerated samples. See the
[Development Workflow](https://github.com/clearpathrobotics/clearpath_generator_tests#development-workflow)
section of that repository for the full process.

## Submitting a pull request

1. Make sure `pre-commit run --all-files` and `python3 -m pytest` both pass.
2. Push your branch and open a pull request against `jazzy`.
3. Write a clear description of what the change does and why. Link any related issues.
4. If your change touches config structure, defaults, or samples, note the matching
   `clearpath_generator_tests` branch in the pull request description.

The changelog (`CHANGELOG.rst`) is maintained by the maintainers at release time, so you do not
need to edit it in your pull request.

## Reporting issues

Please open issues on the
[GitHub issue tracker](https://github.com/clearpathrobotics/clearpath_config/issues) and fill out
the bug report template, which walks you through the details we need to reproduce the problem.

## License

By contributing, you agree that your contributions will be licensed under the
[BSD-3-Clause license](LICENSE) that covers this project.
