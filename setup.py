from setuptools import setup
import clearpath_config

setup(
    name="clearpath_config",
    packages=["clearpath_config", "clearpath_config.platform",
              "clearpath_system"],
    version=clearpath_config.__version__,
    install_requires=[
        'requests',
        'importlib-metadata; python_version == "3.8"',
    ],
)