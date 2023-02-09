from clearpath_config.base.keys import Keys

# Single Configuration Base:
#  - entry within the larger config
#  - examples: PLatform, Single Sensor, Single Mount
#  - structured around:
#     - required keys
#     - required value type per key
#     - optional value tester
class BaseConfig():

    def __init__(self, name, config) -> None:
        # Complete YAML Config
        self.config = config
        self.name = name

        self.required_keys = []
        self.optional_keys = []

    def check_required_keys(self):
        for key in self.required_keys:
            if not self.key_exists(key):
                return False
        return True

    def key_exists(self, key):
        return not self.config.get(key, "NULL") == "NULL"

    def key_is_required(self, key):
        return key in self.required_keys

    def key_is_optional(self, key):
        return key in self.optional_keys

    def key_is_key(self, key):
        return self.key_is_required(key) or self.key_is_optional(key)

    def get_key(self, key):
        if self.key_exists(key):
            return self.config.get(key)
        else:
            return None

    def set_key(self, key, value):
        # If Key is Required or Optional and Valid, Update It
        if self.key_is_key(key) and Keys.is_valid(key, value):
            self.config[key] = value
            return True
        else:
            return False

    def update_config(self):
        pass

    def get_config(self):
        self.update_config()
        return {self.name, self.config}