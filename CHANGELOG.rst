^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package clearpath_config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.0.1 (2023-05-04)
------------------
* Merge pull request `#17 <https://github.com/clearpathrobotics/clearpath_config/issues/17>`_ from clearpathrobotics/readme
  Updated README with up-to-date configs
* Merge pull request `#16 <https://github.com/clearpathrobotics/clearpath_config/issues/16>`_ from clearpathrobotics/ros2
  ROS2 Package
* Merge pull request `#15 <https://github.com/clearpathrobotics/clearpath_config/issues/15>`_ from clearpathrobotics/controller
  Controller
* Merge pull request `#14 <https://github.com/clearpathrobotics/clearpath_config/issues/14>`_ from clearpathrobotics/accessory
  Accessory
* Add metadatat to  setup.py
* Added ROS tests
* Updated cfg with install directories
* Added package.xml
* Fixed decoration parser
* Fixed Decoration parsing
* Linter errors
* Added controller
* Added Accessories to YAML
* Added all lists for Accessories
* Fixed type assertion
* Updated link to common BaseAccessory
* Added visual file path
* Added check for triple values
* Add Mesh
* Added Sphere
* Added Cylinder
* Added Box
* Added
* BaseAccessory
* Updated sample config
* Added  to decorations
* Set 'None' does nothing
* Decorations are now Accessories
* Merge pull request `#13 <https://github.com/clearpathrobotics/clearpath_config/issues/13>`_ from clearpathrobotics/gps
  Added GPS
* Default microstrain port to
* Added Fixed and Target frame to Velodyne
* Fixed GPS ros_parameter keys
* Merge pull request `#12 <https://github.com/clearpathrobotics/clearpath_config/issues/12>`_ from clearpathrobotics/lidar_3d
  Lidar3D
* Added GPS
* Added Lidar3D to sample config
* Parse Lidar3D
* Added lidar3d
* Updated Port to ensure always stores
* Merge pull request `#11 <https://github.com/clearpathrobotics/clearpath_config/issues/11>`_ from clearpathrobotics/imu
  IMU
* Add IMU to get_all_sensors
* Merge pull request `#10 <https://github.com/clearpathrobotics/clearpath_config/issues/10>`_ from clearpathrobotics/ros_parameters
  ROS Parameters
* Added check to increment IMU index
* Added IMU to sample A200 config
* Minor fix to return type
* Added IMU to parser
* Removed checking for nested parameters (assume flattened ros_parameters)
* Flatten ros_parameters dict
* Added flatten dict
* Added  to Realsense
* Fixed camera return type
* Initial IMU commit
* Added frame_id to parser
* Fixed comments
* Added FRAME_ID
* Added ros_parameters to config
* Parse ros_parameters
* Added ros_parameters
* Merge pull request `#9 <https://github.com/clearpathrobotics/clearpath_config/issues/9>`_ from clearpathrobotics/indexing
  Indexing
* Added ros_parameters as empty dict
* Added empty config
* Mounts, sensors, and decorations no longer required
* Sensors use IndexedAccessory and can have first index changed
* All mounts have indexes
* Created IndexedAccessory as base to all iterable accessories
* Use built-in set and get for idx
* Merge pull request `#8 <https://github.com/clearpathrobotics/clearpath_config/issues/8>`_ from clearpathrobotics/wip-iterable-sensors
  Iterable Sensors
* Removed tests for older versions of python
* Fixed imports for Decoration tests
* Manufacturer names added to sensor models and class names
* Sensor Types and Sensor Models
* Updated setuptools
* Fixed  get_all_sensors
* Added __init\_\_
* added sensors to clearpath config
* Added sensors to the parser
* Fixed bug in get function
* Added OrderedList of sensors with access functions
* Added sensors
* Added sub-type models
* Added SENSOR_MODEL
* Added Port class
* Added Base class for lidars and cameras
* Added sensors
* Added Topic, URDF Enable, and Launch Enable to BaseSensor
* Init Sensors
* Merge pull request `#7 <https://github.com/clearpathrobotics/clearpath_config/issues/7>`_ from clearpathrobotics/wip-iterables
  Iterables
* Removed height from Husky sample
* Updated A200 sample
* Added get_enabled
* Added method to retrieve all decorations
* Added Decoration.NEW class
* Added method to retrieve all mounts
* Set decorations to enabled if not specified but exist
* Fixed top plate in parser
* Added BaseDecoration; by default disabled
* Added __init_\_ to mounts
* Updated A200 sample
* Fixed key error print statement
* Upgraded parser to match new mounts
* Removed name as required argument
* Completely disabled all PACS testing
* Removed 'pacs\_' prefix from brackets and risers
* BaseMount no longer requires a name, default to index
* Clear OrderedConfigList if empty list is set
* Updated sample to new mount iterables
* Added mounts as individual ordered lists
* Moved ListConfig and all PACS from the Platform base
* Removed PACS from platform
* Removed name as a default parameter
* Added name from id to BaseMount
* Added OrderedListConfig
* Removed mounting link from fath and flir moutns
* Removed mounting link and model
* Added uid checks to ListConfig
* Split up mounts
* Added get and set methods for individual mounts
* Small lint fixes in common
* Removed mount pseudo namespace
* Updated remove function
* Moved ListConfig
* Fixed lint errors in mounts
* Fixed lint errors in clearpath_config
* Removed PACS Config testers
* Switched parser to new decorations config
* Updated path to base decorations config
* Updated path to config in Platform
* Updated J100 to iterable decorations
* Updated A200 to iterable decorations
* Fixed assertion indenting
* Removed unused imports
* Fixed assertion indenting
* Added get and set functions to ListConfig
* Removed PACS specific configs
* Added base decorations config
* Removed unecessary platform specific decorations
* Merge pull request `#5 <https://github.com/clearpathrobotics/clearpath_config/issues/5>`_ from clearpathrobotics/wip-mounts
  Mounts: Flir PTU and Fath Pivot
* Fixed merge issues
* Added mounts config
* Added mounts to sample config
* Added platform parser
* Added  check to Accessory
* Merge branch 'main' of https://github.com/clearpathrobotics/clearpath_config into main
* Remove old test config yaml
* Merge pull request `#4 <https://github.com/clearpathrobotics/clearpath_config/issues/4>`_ from clearpathrobotics/wip-lint
  Lint Errors and Warnings
* Increased flake8 line length to 100
* Fixed all lint errors
* Merge pull request `#3 <https://github.com/clearpathrobotics/clearpath_config/issues/3>`_ from clearpathrobotics/wip-tests
  Moved tests into the clearpath_config package
* Added PyYaml
* Added pytest-cov
* Create python-package.yml
* Moved tests into the clearpath_config package
* Merge pull request `#2 <https://github.com/clearpathrobotics/clearpath_config/issues/2>`_ from clearpathrobotics/wip-platform
  Added Platform and Updated Parser
* Added init files to submodules
* Updated setuptools
* Removed unused unittest dependency
* Added platform config tests
* Added sets to all PACS parts and configs
* Added checks on bumper extension
* Renamed genx to generic in platform
* Renamed genx to generic in common
* Renamed GENX to generic
* Added a200 and j100 sample config
* Added J100 to parser
* Changed import path to match new file structure
* Added A200, J100, and GENX (generic)
* Moved platform and system to new folder structure
* Changed parser to math new folder structure
* Fixed RPY and XYZ setters
* Changed import for the new folder structure
* Platforms referenced only by product code, i.e. A200, to avoid version issues
* Use setters to initialize Accessory
* Merge pull request `#1 <https://github.com/clearpathrobotics/clearpath_config/issues/1>`_ from clearpathrobotics/wip-object-structure
  Split Parsing and Config Containers
* Updated sample config to match changes
* Added extras to parser
* Default extras file paths set to empty strings
* Fixed File class __str_\_ method
* Moved everything out of Parser class, and added Parser suffix
* Swap to multi-class inheritance for PACS configs
* Removed parsing from clearpath_config
* Fixed bugs in setting remotes
* Added Platform Config, Only Husky and Jackal
* Changed prefix to name
* Added Accessory class
* Added Platform to common
* Added File and SerialNumber classes
* Added proper spacing
* Added too many fields test
* Regex expression set to raw string
* Fixed SystemConfig init
* Added check that hostname must be str
* Fixed initialization of HostConfig
* Removed checks from parser
* Added UnitTest information to README
* Removed utils
* Added tests for SystemConfig
* Moved all class files out of base
* Added keys
* Moved version
* Initial config parser structure
* Initial commit
* Contributors: Luis Camero, luis-camero