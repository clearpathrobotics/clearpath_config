# clearpath_config
Clearpath Configuration YAML Parser

Find documentation on the Clearpath Configuration YAML and more about the Clearpath ROS 2 System on the [Clearpath Documentation](https://docs.clearpathrobotics.com/docs/ros/config/yaml) webpage.

# Configration Examples
Under the **_sample_** folder there are example configurations that can be used as the starting point of your `robot.yaml`.


# Unit Tests
All unit tests are written using **PyTest** following the [Good Integration Practices](https://docs.pytest.org/en/6.2.x/goodpractices.html#goodpractices).

Therefore, `clearpath_config_test` is a package that mirrors the `clearpath_config` package structure. Each file from `clearpath_config` that is to be tested should have a corresponding file with the same name and the suffix `_test.py`.

To run the tests:
```bash
cd .../clearpath_config
python3 -m pytest
```
> **PyTest** will automatically search for the suffix `_test` throughout the current directory and run the tests.
