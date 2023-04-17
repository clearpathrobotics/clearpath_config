from setuptools import setup
import clearpath_config

setup(
    name="clearpath_config",
    packages=[
        "clearpath_config",
        "clearpath_config.platform",
        "clearpath_config.system",
        "clearpath_config.mounts",
        "clearpath_config.sensors"
    ],
    version=clearpath_config.__version__,
    install_requires=[
        "requests",
        'importlib-metadata; python_version == "3.8"',
    ],
)
