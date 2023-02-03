# Single Configuration Base:
#  - entry within the larger config
#  - examples: PLatform, Single Sensor, Single Mount
#  - structured around:
#     - required keys
#     - required value type per key
#     - optional value tester
class ConfigBase():

    def __init__(self, name, config) -> None:
        # Complete YAML Config
        self.config = config
        self.name = name
