import os
import yaml


# Get Valid Path
def find_valid_path(path, cwd=None):
    abspath = path
    if cwd:
        relpath = os.path.join(cwd, path)
    else:
        relpath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), path)
    if not os.path.isfile(abspath) and not os.path.isfile(relpath):
        return None
    if os.path.isfile(abspath):
        path = abspath
    elif os.path.isfile(relpath):
        path = relpath
    return path


def read_yaml(path: str) -> dict:
    # Check YAML Path
    path = find_valid_path(path, os.getcwd())
    assert path, "YAML file '%s' could not be found" % path
    # Check YAML can be Opened
    try:
        config = yaml.load(open(path), Loader=yaml.SafeLoader)
    except yaml.scanner.ScannerError:
        raise AssertionError(
            "YAML file '%s' is not well formed" % path)
    except yaml.constructor.ConstructorError:
        raise AssertionError(
            "YAML file '%s' is attempting to create unsafe objects" % (
                path))
    # Check contents are a Dictionary
    assert isinstance(config, dict), (
        "YAML file '%s' is not a dictionary" % path)
    return config


def write_yaml(path: str, config: dict) -> None:
    yaml_file = open(path, "w+")
    yaml.Dumper.ignore_aliases = lambda *args: True
    yaml.dump(
        config,
        yaml_file,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
