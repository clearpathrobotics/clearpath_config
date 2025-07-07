^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package clearpath_config
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.6.1 (2025-07-07)
------------------
* Forward Fix: Add ur_type parameter to UniversalRobots manipulator (`#177 <https://github.com/clearpathrobotics/clearpath_config/issues/177>`_)
* Contributors: luis-camero

2.6.0 (2025-07-04)
------------------
* Feature: All Platforms Supported (`#176 <https://github.com/clearpathrobotics/clearpath_config/issues/176>`_)
  * All platforms are now supported
  * Remove unused dependencies
* Added sensor sample for phidgets_spatial. (`#175 <https://github.com/clearpathrobotics/clearpath_config/issues/175>`_)
* Enable foxglove bridge by default (`#173 <https://github.com/clearpathrobotics/clearpath_config/issues/173>`_)
* Add A300 AMP attachments, samples (`#158 <https://github.com/clearpathrobotics/clearpath_config/issues/158>`_)
  * Add attachments for A300 Observer
  * Add A300 Observer sample
  * Add parameters to set the Ouster OS-1 base & cap type
  * Add spotlight attachment
* Contributors: Chris Iverach-Brereton, Hilary Luo, Tony Baltovski, luis-camero

2.5.0 (2025-05-29)
------------------
* Fix: PACS Limits (`#171 <https://github.com/clearpathrobotics/clearpath_config/issues/171>`_)
* Add foxglove bridge enable to platform section (`#169 <https://github.com/clearpathrobotics/clearpath_config/issues/169>`_)
* Add enable setting for wireless-watcher (`#170 <https://github.com/clearpathrobotics/clearpath_config/issues/170>`_)
* Feature: CAN Bridge Parameters (`#166 <https://github.com/clearpathrobotics/clearpath_config/issues/166>`_)
* Add cap_type parameter to the OS1 sample since it's supported (`#163 <https://github.com/clearpathrobotics/clearpath_config/issues/163>`_)
* Fix/issue typos (`#168 <https://github.com/clearpathrobotics/clearpath_config/issues/168>`_)
* Contributors: Chris Iverach-Brereton, Hilary Luo, luis-camero

2.4.0 (2025-05-01)
------------------
* Keep default can_bridge entries (`#160 <https://github.com/clearpathrobotics/clearpath_config/issues/160>`_)
* Contributors: Luis Camero

2.3.1 (2025-04-28)
------------------
* Fixed the Husky A300 serial sample to match the real serial.
* Contributors: Tony Baltovski

2.3.0 (2025-04-11)
------------------
* Added a single Hokuyo laser to default R100 sample. (`#157 <https://github.com/clearpathrobotics/clearpath_config/issues/157>`_)
* Maintain default can adapters but allow overwriting if matching names (`#155 <https://github.com/clearpathrobotics/clearpath_config/issues/155>`_)
* Feature: Wiferion Charger (`#154 <https://github.com/clearpathrobotics/clearpath_config/issues/154>`_)
* Feature: Add CAN adapters  (`#153 <https://github.com/clearpathrobotics/clearpath_config/issues/153>`_)
* Rename camera IMU topics from imu to imu/data_raw (per RPSW-2503) (`#150 <https://github.com/clearpathrobotics/clearpath_config/issues/150>`_)
* Feature: Add delay to manipulator controller (`#146 <https://github.com/clearpathrobotics/clearpath_config/issues/146>`_)
* Feature: Manipulator URDF Parameters (`#145 <https://github.com/clearpathrobotics/clearpath_config/issues/145>`_)
* Feature: MoveIt Parameters and Enable (`#144 <https://github.com/clearpathrobotics/clearpath_config/issues/144>`_)
* Fast-Forward Feature: Manipulator Samples and Poses (`#143 <https://github.com/clearpathrobotics/clearpath_config/issues/143>`_)
* Removed J100 from unsupported platforms (`#149 <https://github.com/clearpathrobotics/clearpath_config/issues/149>`_)
* Changed all sensor samples to the Husky A300. (`#148 <https://github.com/clearpathrobotics/clearpath_config/issues/148>`_)
* Add support for INS sensors + Fixposition XVN (`#142 <https://github.com/clearpathrobotics/clearpath_config/issues/142>`_)
* Removed Dingo and Ridgeback from unsupported exception (`#137 <https://github.com/clearpathrobotics/clearpath_config/issues/137>`_)
* Contributors: Chris Iverach-Brereton, Roni Kreinin, Tony Baltovski, Luis Camero

2.2.2 (2025-03-27)
------------------
* Updated the parent link of the base IMU on the A300.
* Contributors: Tony Baltovski

2.2.1 (2025-03-17)
------------------
* Added battery to A300 samples.
* Contributors: Tony Baltovski

2.2.0 (2025-03-11)
------------------
* Feature Jazzy Ouster (`#132 <https://github.com/clearpathrobotics/clearpath_config/issues/132>`_)
  * Add OusterOS1
  * Add ouster sample
  * Alphabetical entries to Lidar3D models
* Add D455, D456 to supported devices (`#136 <https://github.com/clearpathrobotics/clearpath_config/issues/136>`_)
* Add support for OAK-D Pro W PoE (`#135 <https://github.com/clearpathrobotics/clearpath_config/issues/135>`_)
  * Add OAK-D Pro W PoE to sensor types. Add IP address field to OAK-D camera class, defaulting to None (for non-PoE models). Add a new assertion to validate IPv4 addresses
  * Support the `device_type` parameter for OAK-D cameras
  * Add i_mx_id, i_ip for identifying multiple cameras. Fix serial so it maps to i_usb_port_id
  * Rename variable to avoid overwriting python builtin
  * Allow empty strings as well as None for the IP address
  * Add assert_is_ipv4_address to BaseSensor
* Add URDF-only support for the Seyond Robin W (`#131 <https://github.com/clearpathrobotics/clearpath_config/issues/131>`_)
  * Add the SeyondLidar class
  * Add sample for the Seyond Robin W
* Contributors: Chris Iverach-Brereton, luis-camero

2.1.1 (2025-02-05)
------------------
* Fixed docs link for Robot YAML. (`#124 <https://github.com/clearpathrobotics/clearpath_config/issues/124>`_)
* Updated the A300's default IMU location.
* Contributors: Tony Baltovski

2.1.0 (2025-01-31)
------------------
* Jazzy Phidgets IMU Filter (`#119 <https://github.com/clearpathrobotics/clearpath_config/issues/119>`_)
  * Add filter to IMU entry
  * Enable mag only for Phidgets
  * Add DATA topic to Phidget
* Add the phidget to default sample (`#120 <https://github.com/clearpathrobotics/clearpath_config/issues/120>`_)
* Change default user to robot (`#121 <https://github.com/clearpathrobotics/clearpath_config/issues/121>`_)
* Feature/diagnostics (`#117 <https://github.com/clearpathrobotics/clearpath_config/issues/117>`_)
  * Switched class (shared) variables to non-muteable types to prevent unexpected behaviour if they were ever changed
  * Remove redundant getters and setters
  * Remove duplicate variable definition
  * Add topic message type and correct rates so they are not shared muteable variables
* Ewellix Lift (`#115 <https://github.com/clearpathrobotics/clearpath_config/issues/115>`_)
  * Added Ewellix Lift (`#109 <https://github.com/clearpathrobotics/clearpath_config/issues/109>`_)
  * Initial add of lifts to config
  * Added ewellix parameters
  * Fix lint
* Removed deprecated parameters
* Contributors: Hilary Luo, Luis Camero

2.0.1 (2025-01-16)
------------------
* Add Zenoh support (`#113 <https://github.com/clearpathrobotics/clearpath_config/issues/113>`_)
  * Add Zenoh to the list of supported RMW implementations
  * Add zenoh_router_config_uri parameter to middleware config
  * Add a sanity check to make sure we aren't trying to use Zenoh on a MicroROS-using platform
  * Allow Zenoh on generic platforms
* Contributors: Chris Iverach-Brereton

2.0.0 (2025-01-14)
------------------
* Add HE2410 & HE2411 battery support (`#110 <https://github.com/clearpathrobotics/clearpath_config/issues/110>`_) (`#111 <https://github.com/clearpathrobotics/clearpath_config/issues/111>`_)
  * Add support for the HE2410 and HE2411 batteries to J100 and A200
* Fixed tests.
* Add additional controllers (`#105 <https://github.com/clearpathrobotics/clearpath_config/issues/105>`_)
  * Add Xbox controller support
  * Add PS5 controller support
* Add enable_ekf property to platform (`#106 <https://github.com/clearpathrobotics/clearpath_config/issues/106>`_)
* Re-add the A200/A201 Observer sample now that https://github.com/clearpathrobotics/clearpath_common/pull/122 is merged (`#107 <https://github.com/clearpathrobotics/clearpath_config/issues/107>`_)
* Fix failing tests (`#104 <https://github.com/clearpathrobotics/clearpath_config/issues/104>`_)
  * Remove the husky observer sample; it depends on as-yet-unmerged changes to clearpath_common
  * Flag the Zed camera as unsupported for now
  * Skip any additional tests if there's an unsupported platform or accessory in the sample
* Fix the Axis camera topics (`#100 <https://github.com/clearpathrobotics/clearpath_config/issues/100>`_)
* Raise an UnsupportedPlatformException for the Jackal (for now); we don't have Jazzy firmware for it yet (`#103 <https://github.com/clearpathrobotics/clearpath_config/issues/103>`_)
* A300 VCAN (`#102 <https://github.com/clearpathrobotics/clearpath_config/issues/102>`_)
  * A300 vcan0 bridge
  * Disable vcan1 bridge for now
* Fix support for the device_type parameter; previously the camera would always be a Q62 (`#99 <https://github.com/clearpathrobotics/clearpath_config/issues/99>`_)
* Add the A200 Observer backpack attachment (`#96 <https://github.com/clearpathrobotics/clearpath_config/issues/96>`_)
  * Add the A200 Observer backpack attachment
  * Add the Husky Observer sample
  * Add the IMU to the sample
  * Add source CI
  * Linting for new CI
  * More linting
  * Silently replace the A201 prefix with A200; this lets us support the Observer with minimal changes elsewhere (and the number of A201 bases is very small)
  * Update the Observer sample to use the A201 serial numbers
* Add A300 samples (`#98 <https://github.com/clearpathrobotics/clearpath_config/issues/98>`_)
  * Add the AMP mount attachment
  * Add A300 samples
  * Add the outline sample
  * Add AMP frame to sample
* Bugfix MODEL.keys() (`#97 <https://github.com/clearpathrobotics/clearpath_config/issues/97>`_)
* A300 battery comment to LiFEPO4
* Fix all linting errors
* Add a300 extra ros parameters
* Add a300 to attachment mux
* Add a300 platform empty ros parameters
* Add a300 can interfaces
* Add a300 platform battery
* Add a300 platform attachments
* Add A300 platform entry
* Add the ability to flag previously-supported accessories & platforms as not (currently) supported (`#86 <https://github.com/clearpathrobotics/clearpath_config/issues/86>`_)
  * Add initial support for flagging unsupported accessories (e.g. Kinova arms, whose binary drivers don't exist in Jazzy yet)
  * classmethod -> staticmethod
  * Use the ROS_DISTRO variable from clearpath_generator_common instead of hard-coding the distro
  * Start fixing up python linter errors, code formatting, replace % strings with f'' strings.
  * Finish first-pass replacing " -> '
  * Fix remaining linter errors. Some tests are still failing, but the major code tidying-up should be done now
  * Fix type -> _type
  * Update CI for Jazy
  * Update Python package workflow for Jazzy
  * Remove dependency on clearpath_generator_common; doing so creates a circular dependency. Instead use the system level envar
  * Add the ability to flag whole platforms as deprecated and/or unsupported
  * Docs
  * Fix imperative tone, missing periods in docstrings, missing newline at end of file
  * Mark everything besides Jackal and Husky as presently unsupported
  * Fix up sample yaml formatting. Remove unmatched quotation marks, restructure to avoid `foo.bar.spam: eggs` notation
  * Fix quotation marks for the sample serial number
* Add default vcan ROS interfaces based on platform
* Add support for Axis cameras (`#90 <https://github.com/clearpathrobotics/clearpath_config/issues/90>`_)
  * Add the initial AxisCamera class with all ROS parameters defined in axis_camera's launch files & nodes
  * Remove duplicate argument
  * Add the AxisCamera class to the sensors generator
  * Add the serial to the axis camera's template
  * Add serial to the template keys too
  * Add serial getter/setter. Use empty string as default serial
  * Refactoring, set the property to the value for the template
  * frame_width -> width, frame_height -> height
  * Rename setter
  * Make the scales & offsets floats by default
  * Add the TF prefix parameter
  * Add the camera_info_url parameter
  * camera_num -> camera
  * Note that the serial isn't used, fix the name of the PTZ teleop parameter
  * Add the remaining camera topics to the Topics object
  * image_raw -> image
  * Add axis_camera sample
  * Linting fixes
  * End docstring with `.`
* Add ur_arm
* Add a sample for each sensor
* Add default vcan ROS interfaces based on platform
* Add support for Axis cameras (`#90 <https://github.com/clearpathrobotics/clearpath_config/issues/90>`_)
  * Add the initial AxisCamera class with all ROS parameters defined in axis_camera's launch files & nodes
  * Remove duplicate argument
  * Add the AxisCamera class to the sensors generator
  * Add the serial to the axis camera's template
  * Add serial to the template keys too
  * Add serial getter/setter. Use empty string as default serial
  * Refactoring, set the property to the value for the template
  * frame_width -> width, frame_height -> height
  * Rename setter
  * Make the scales & offsets floats by default
  * Add the TF prefix parameter
  * Add the camera_info_url parameter
  * camera_num -> camera
  * Note that the serial isn't used, fix the name of the PTZ teleop parameter
  * Add the remaining camera topics to the Topics object
  * image_raw -> image
  * Add axis_camera sample
  * Linting fixes
  * End docstring with `.`
* Remove empty line at EoF
* Add header
* rx and tx topics for can bridge
* Initial can_bridges add
* Add ur_arm
* Add a sample for each sensor
* Add the ability to flag previously-supported accessories & platforms as not (currently) supported (`#86 <https://github.com/clearpathrobotics/clearpath_config/issues/86>`_)
  * Add initial support for flagging unsupported accessories (e.g. Kinova arms, whose binary drivers don't exist in Jazzy yet)
  * classmethod -> staticmethod
  * Use the ROS_DISTRO variable from clearpath_generator_common instead of hard-coding the distro
  * Start fixing up python linter errors, code formatting, replace % strings with f'' strings.
  * Finish first-pass replacing " -> '
  * Fix remaining linter errors. Some tests are still failing, but the major code tidying-up should be done now
  * Fix type -> _type
  * Update CI for Jazy
  * Update Python package workflow for Jazzy
  * Remove dependency on clearpath_generator_common; doing so creates a circular dependency. Instead use the system level envar
  * Add the ability to flag whole platforms as deprecated and/or unsupported
  * Docs
  * Fix imperative tone, missing periods in docstrings, missing newline at end of file
  * Mark everything besides Jackal and Husky as presently unsupported
  * Fix up sample yaml formatting. Remove unmatched quotation marks, restructure to avoid `foo.bar.spam: eggs` notation
  * Fix quotation marks for the sample serial number
* Removed line at EOF
* Add header
* Merge pull request `#82 <https://github.com/clearpathrobotics/clearpath_config/issues/82>`_ from clearpathrobotics/lcamero/phidgets_spatial
  Add phidgets spatial to config
* Add OAKD
* rx and tx topics for can bridge
* Initial can_bridges add
* Contributors: Chris Iverach-Brereton, Luis Camero, Roni Kreinin, Tony Baltovski, Yoan Mollard

0.3.4 (2024-10-04)
------------------
* Add OAKD
* Add phidgets spatial to config
* Contributors: Luis Camero

0.3.3 (2024-09-29)
------------------
* Allow all parameters to be modified
* Contributors: Luis Camero

0.3.2 (2024-09-23)
------------------
* Alphabetically order packages
* Add manipulators to setup
* Contributors: Luis Camero

0.3.1 (2024-09-19)
------------------
* Fix battery in r100 sample
* Contributors: Luis Camero

0.3.0 (2024-09-19)
------------------
* Add samples to setup.py
* Remove empty line in D150 attachments
* Height parameters for tower shoulder
* FAMS, HAMS, and Tower as separate attachments
* Add height parameter to Dingo top plate
* Add samples for Dingo O and Ridgeback
* 0.3 Release Candidate with Main Changes (`#73 <https://github.com/clearpathrobotics/clearpath_config/issues/73>`_)
  * Renamed node to intel_realsense in config
  * Changes.
  * 0.2.8
  * Added Zed as type of camera
  * Added Zed to configuration
  * Changes.
  * 0.2.9
  * Updated Realsense parameters
  * Updated Microstrain link parameter
  * Changes.
  * 0.2.10
  * Adds GQ7 as possible sensor
  * Changes.
  * 0.2.11
  ---------
  Co-authored-by: Tony Baltovski <tbaltovski@clearpathrobotics.com>
  Co-authored-by: robbiefish <rob.fisher@hbkworld.com>
* Fix ridgeback battery configuration
* 0.2.8
* Changes.
* Renamed node to intel_realsense in config
* 0.2.7
* Changes.
* W200 attachments default to 0
* Re-added host and namespace
* Minimal samples.
* Removed long line
* Added launch to extras
* 0.2.6
* Changes.
* Switched local server to be referenced as loopback in the ROS_DISCOVERY_SERVER envar
* Add discovery server support
* assertion error if the hostname is blank (otherwise causes an invalid index exception)
* Add localhost field which is set automatically
* Reformat hosts section to single list of all computers
* 0.2.5
* Changes.
* Added battery launch arguments to support launching the valence bms node
* Add republishers to camera
* Add IP and Port parameters to manipulator config
* Added manipulator to config
* Added methods to replace entries in a dictionary
* YAML reader properly displays original path in assertions
* Fix ros_parameters
* 0.2.4
* Changes.
* Install the W200 samples.
* Fixed j100 and w200 laser sample
* 0.2.3
* Changes.
* Give option to get topic without namespace
* 0.2.2
* Changes.
* Fix how blank urdf extras is handled
* 0.2.1
* Changes.
* Find packages for meshes / extras urdf (`#45 <https://github.com/clearpathrobotics/clearpath_config/issues/45>`_)
  * Allow meshes visual and extras urdf to be linked using find package functionality
* Added Ridgeback attachments
* Initial Ridgeback
* Contributors: Hilary Luo, Luis Camero, Roni Kreinin, Tony Baltovski, luis-camero

0.2.11 (2024-08-08)
-------------------
* Adds GQ7 as possible sensor
* Contributors: robbiefish

0.2.10 (2024-07-22)
-------------------
* Updated Microstrain link parameter
* Updated Realsense parameters
* Contributors: Luis Camero

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
