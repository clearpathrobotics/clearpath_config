# clearpath_config
Clearpath Configuration YAML Parser 

# Configration Examples
## Primary Computer Config
```xml
version: 0
 
system: # These are system level configs
    self: J100-1
    hosts: # These are the hosts that are involved in this system
        platform: # The main computer for this system, ie the robot's computer
            J100-1: 192.168.131.1
        onboard: # These are additional on-board computers such as a secondary computer or software kit
            J100-1B: 192.168.131.5
            ONAV-KIT: 192.168.131.1
        remote: # These are remote machines which need to interact with this system such as laptops or other robots
            CPR12345: 10.10.10.101
            A200-1: 192.168.1.111
    ros2:
        namespace: HOSTNAME
        domain_id: 123
        rmw_implementation: rmw_fastrtps_cpp
        FASTRTPS_DEFAULT_PROFILES_FILE (optional)
        CYCLONEDDS_URI (optional)
 
 
platform: # These are are parameters specific to a a platform
    serial_number: J100-XXXXX
    model: J100
    decorations: # Platform specific accessories
        fenders:
        wibotic_mount: true
        pacs:
            risers
            partial_riser
            brackets
    extras:
        control: PATH_TO_CONTROL_EXTRAS_YAML
 
mounts:
    front_pivot:
        enabled: true
        parent_link: front_mount
        accessory_link: front_pivot_mount
        model: fath_pivot
        angle: 0
        xyz: [0, 0, 0]
        rpy: [0, 0, 0]
 
sensors: # Various sensors
    lidars:
        0:
            model: hokuyo_ust10 # model of the sensor
            driver: true # If the driver should be launched
            host: J100-1 # The host where the driver will launched on
            description: true # If the description is enabled
            parent_link: front_pivot_mount
            xyz: [0, 0, 0]
            rpy: [0, 0, 0]
            # Below are sensor specific params
            error_limit: 5
        1:
            model: sick-lms100
            driver: true
            host: J100-1B
            description: true
            parent_link: front_pivot_1
            xyz: [0, 0, 0]
            rpy: [0, 0, 0]
            error_limit: 5
    gps:
        0:
            model: nmea
            driver: true
            host: J100-1
            description: true
            parent_link: front_gps_mount
            xyz: [0, 0, 0]
            rpy: [0, 0, 0]
```

## Secondary Computer Config
```xml
version: 0
 
system: # These are system level configs
    self: J100-1B
    hosts: # These are the hosts that are involved in this system
        platform: # The main computer for this system, ie the robot's computer
            J100-1: 192.168.131.1
        onboard: # These are additional on-board computers such as a secondary computer or software kit
            J100-1B: 192.168.131.5
            ONAV-KIT: 192.168.131.1
        remote: # These are remote machines which need to interact with this system such as laptops or other robots
            CPR12345: 10.10.10.101
            A200-1: 192.168.1.111
    ros2:
        namespace: HOSTNAME
        domain_id: 123
        rmw_implementation: rmw_fastrtps_cpp
        FASTRTPS_DEFAULT_PROFILES_FILE (optional)
        CYCLONEDDS_URI (optional)
 
 
platform: # These are are parameters specific to a a platform
    serial_number: J100-XXXXX
    model: J100
    decorations: # Platform specific accessories
        fenders:
        wibotic_mount: true
        pacs:
            risers
            partial_riser
            brackets
    extras:
        control: PATH_TO_CONTROL_EXTRAS_YAML
 
mounts:
    front_pivot:
        enabled: true
        parent_link: front_mount
        accessory_link: front_pivot_mount
        model: fath_pivot
        angle: 0
        xyz: [0, 0, 0]
        rpy: [0, 0, 0]
 
sensors: # Various sensors
    lidars:
        0:
            model: hokuyo_ust10 # model of the sensor
            driver: true # If the driver should be launched
            host: J100-1 # The host where the driver will launched on
            description: true # If the description is enabled
            parent_link: front_pivot_mount
            xyz: [0, 0, 0]
            rpy: [0, 0, 0]
            # Below are sensor specific params
            error_limit: 5
        1:
            model: sick-lms100
            driver: true
            host: J100-1B
            description: true
            parent_link: front_pivot_1
            xyz: [0, 0, 0]
            rpy: [0, 0, 0]
            error_limit: 5
    gps:
        0:
            model: nmea
            driver: true
            host: J100-1
            description: true
            parent_link: front_gps_mount
            xyz: [0, 0, 0]
            rpy: [0, 0, 0]
```

# Unit Tests
All unit tests are written using **PyTest** following the [Good Integration Practices](https://docs.pytest.org/en/6.2.x/goodpractices.html#goodpractices).

Therefore, `clearpath_config_test` is a package that mirrors the `clearpath_config` package structure. Each file from `clearpath_config` that is to be tested should have a corresponding file with the same name and the suffix `_test.py`.

To run the tests:
```bash
cd .../clearpath_config
python3 -m pytest
```
> **PyTest** will automatically search for the suffix `_test` throughout the current directory and run the tests. 