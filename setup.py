from setuptools import setup
import os

package_name = "clearpath_config"

setup(
    name=package_name,
    version="0.0.2",
    packages=[
        package_name,
        package_name + ".platform",
        package_name + ".system",
        package_name + ".mounts",
        package_name + ".sensors",
        package_name + ".accessories",
    ],
    data_files=[
        # Install marker file in the package index
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        # Include the package.xml file
        (os.path.join("share", package_name), ["package.xml"]),
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
