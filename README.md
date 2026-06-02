# clearpath_config

Clearpath Configuration YAML Parser

Find documentation on the Clearpath Configuration YAML and more about the Clearpath ROS 2 System on the [Clearpath Documentation](https://docs.clearpathrobotics.com/docs/ros/config/yaml/overview) webpage.

## Configuration Examples

Under the **_sample_** folder there are example configurations that can be used as the starting point of your `robot.yaml`.

## Pre-commit

This repository uses [pre-commit](https://pre-commit.com/) to run linting and formatting checks before each commit.

Install the hooks (one-time setup):

```bash
pip install pre-commit
pre-commit install
```

Run against all files manually:

```bash
pre-commit run --all-files
```

## Unit Tests

All unit tests are written using **PyTest** following the [Good Integration Practices](https://docs.pytest.org/en/6.2.x/goodpractices.html#goodpractices).

Therefore, `clearpath_config_test` is a package that mirrors the `clearpath_config` package structure. Each file from `clearpath_config` that is to be tested should have a corresponding file with the same name and the suffix `_test.py`.

To run the tests:

```bash
cd .../clearpath_config
python3 -m pytest
```

> **PyTest** will automatically search for the suffix `_test` throughout the current directory and run the tests.

## Generator Tests

Changes to `clearpath_config` (e.g. adding or modifying test samples, config structure, or
defaults) may affect the output of the Clearpath generators. The
[clearpath_generator_tests](https://github.com/clearpathrobotics/clearpath_generator_tests)
repository versions the expected generator output and validates it through CI.

Before merging, ensure a corresponding branch with the **same name** exists in
`clearpath_generator_tests` with regenerated samples. See the
[Development Workflow](https://github.com/clearpathrobotics/clearpath_generator_tests#development-workflow)
section of `clearpath_generator_tests` for the full process.
