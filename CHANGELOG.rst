^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package clearpath_config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

0.2.9 (2024-05-28)
------------------
* Added Zed to configuration
* Added Zed as type of camera
* Contributors: Luis Camero

0.2.8 (2024-05-14)
------------------
* Renamed node to intel_realsense in config
* Contributors: Luis Camero

0.2.7 (2024-04-08)
------------------
* Re-added host and namespace
* W200 attachments default to 0
* Minimal samples.
* Removed long line
* Added launch to extras
* Contributors: Luis Camero

0.2.6 (2024-03-18)
------------------
* Switched local server to be referenced as loopback in the ROS_DISCOVERY_SERVER envar
* Add discovery server support
* assertion error if the hostname is blank (otherwise causes an invalid index exception)
* Add localhost field which is set automatically
* Reformat hosts section to single list of all computers
* Contributors: Hilary Luo

0.2.5 (2024-03-06)
------------------
* Add republishers to camera
* Added battery launch arguments to support launching the valence bms node
* Fix ros_parameters
* Contributors: Hilary Luo, Luis Camero

0.2.4 (2024-01-22)
------------------
* Install the W200 samples.
* Fixed j100 and w200 laser sample
* Contributors: Roni Kreinin, Tony Baltovski

0.2.3 (2024-01-10)
------------------
* Give option to get topic without namespace
* Contributors: Hilary Luo

0.2.2 (2024-01-08)
------------------
* Fix how blank urdf extras is handled
* Contributors: Hilary Luo

0.2.1 (2024-01-04)
------------------
* Find packages for meshes / extras urdf (`#45 <https://github.com/clearpathrobotics/clearpath_config/issues/45>`_)
  * Allow meshes visual and extras urdf to be linked using find package functionality
* Contributors: Hilary Luo

0.2.0 (2023-12-07)
------------------
* Added wheel parameter to platform
* Fixed typo
* Added dd150 samples
* Added dd100 samples
* Fixed origin of pacs mounts
* Renamed SLA on Dingo
* Added entries for all dingo
* Updated sample to match attachments rework
* Fixed merge issues
* Added more warthog samples
* Updated sample default_mount
* Removed duplicate
* Added W200 attachments
* Updated default mounts on j100
* Updated default mounts on a200
* Changed default parent link to default_mount
* Changed the parent link of attachments
* Removed blannk line
* Removed top_plate from tests
* Updated samples
* Common attachments accross platforms
* Concatenate lists
* Updated all platform attachments
* Updated base attachment
* Attachments now list
* Updated Attachments to more genric case
* Removed specific attachment classes
* Remove all from list
* Accessory from/to dict
* Fixed long line for linter
* Moved username out of ros2 section
* Re-define DEFAULTS based on platform
* Detailed errors
* Fixed typo in samples
* Updated battery model
* Switched configurations
* Update commit
* Revert "Added battery to platform"
  This reverts commit fce11835ca8d6c477890084761075b5b46532bf2.
* Added battery to platform
* Added control section
* Consistent naming
* Added topics to base and fixed typos
* Added get_topic and get_topic_rate
* Added TOPICS and get_topic
* Added description and launch to generic robot platform
* Added Warthog without Attachments or ROS Parameters
* Contributors: Luis Camero, luis-camero

0.1.1 (2023-10-02)
------------------
* Removed micro_ros_ws
* Velodyne changes
* clearpath_config/sensors/types/lidars_2d.py
* FPS expected as float
* Added ros_parameter_template
* Contributors: Hilary Luo, Luis Camero

0.1.0 (2023-08-31)
------------------
* Updated samples to include workspace
* Contributors: Luis Camero

0.0.6 (2023-08-10)
------------------
* Added all modules to setup.py
* Removed J100 bumpers from samples
* Updated sample configs
* Added posts and disks to samples
* Removed unused include
* Split tower into post and disk
* Renamed ust10 to ust
* Updated README
* Updated samples
* Removed eof line
* Fixed port paths
* Added fenders, default disabled
* Added ROS CI, issue templates and codeowners.
* Added sick stand and variable-leg tower
* Added UM7/UM6
* Contributors: Luis Camero, Tony Baltovski

0.0.5 (2023-07-31)
------------------
* Split novatel GPS
* PyTest issues
* Linter issues
* Node names and flatten dictionaries
* Added ros_parameters to extras
* Added Garmin and Novatel gps
* Added node names to rosparameters in sensors
* Update hostname and namespace to match serial
* Resolved indexing issue
* Contributors: Luis Camero

0.0.4 (2023-07-17)
------------------
* Added __init_\_ to common
* Only run pytest on clearpath_config
* Linting errors
* Added samples to installed share
* Removed parser
* Updated pytests
* Renamed configs
* Added license file
* Added license headers
* Renamed accessories to links in top level config
* Replaced accessories module with links
* Renamed decorations and accessories
* Standard lists
* Removed all old samples
* Added workspace setter
* Added workspaces
* Fixed rpy type
* Removed copy
* Contributors: Luis Camero

0.0.3 (2023-07-06)
------------------
* Fixed parsing issues
* Added python3-yaml to dependencies
* Removed old parser
* Removed unused code
* Added updates to change indexing based on serial number
* Added sensors to property system
* Added __init_\_ to all subfolders
* Added mounts to main config
* Moved mount types to separate folder
* Added read and write functions to ClearpathConfig
* Added accessories to property method
* Updated all configs to use properties instead of setters
* Updated base config to use properties to update config
* Updated clearpath config to property setters
* Removed old common and updated serial number type
* Updated system to use global serial number
* Updated platform to property setters
* Changed System config to property setters
* Contributors: Luis Camero

0.0.2 (2023-06-12)
------------------
* Fixed gps indexing
* Added system ROS2 parameters
* Decorations enabled by default
* Added resource and package.xml to install data files
* Contributors: Luis Camero

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
