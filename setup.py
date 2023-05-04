from setuptools import setup

package_name = "clearpath_config"

setup(
    name=package_name,
    version="0.0.1",
    packages=[
        package_name,
        package_name + ".platform",
        package_name + ".system",
        package_name + ".mounts",
        package_name + ".sensors"
    ],
    install_requires=[
        "setuptools",
        "requests",
        'importlib-metadata; python_version == "3.8"',
    ],
    zip_safe=True,
    maintainer="Luis Camero",
    maintainer_email="lcamero@clearpathrobotics.com",
    description="Clearpath Configuration YAML Parser and Writer",
    license="BSD-3",
    tests_require=['pytest']
)
