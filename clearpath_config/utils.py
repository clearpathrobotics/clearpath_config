import os
import yaml

# Get Valid Path
def find_valid_path(path, cwd=None):
    abspath = path
    if cwd:
        relpath = os.path.join(cwd, path)
    else:
        relpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if not os.path.isfile(abspath) and not os.path.isfile(relpath):
        return None
    if os.path.isfile(abspath):
        path = abspath
    elif os.path.isfile(relpath):
        path = relpath
    return path

def read_yaml(path):
    path = find_valid_path(path, os.getcwd())
    if path is None:
        print('YAML file {0} could not be found'.format(path))
        return False
    # Check YAML can be Opened
    try:
        config = yaml.load(open(path), Loader=yaml.SafeLoader)
    except yaml.scanner.ScannerError:
        print('YAML file {0} is not well formed'.format(path))
        return None
    except yaml.constructor.ConstructorError:
        print('YAML file {0} is attempting to create unsafe objects'.format(path))
        return None
    # Check contents are a Dictionary
    if not isinstance(config, dict):
        print('YAML file {0} is not a dictionary'.format(path))
        return None
    return config

def write_yaml(path, config):
    yaml_file = open(path, 'w+')
    yaml.dump(config, yaml_file, sort_keys=False, default_flow_style=None, allow_unicode=True)
