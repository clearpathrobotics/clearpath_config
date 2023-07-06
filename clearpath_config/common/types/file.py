import os


# File
# - file class
class File:
    def __init__(self, path: str, creatable=False, exists=False) -> None:
        if creatable:
            assert File.is_creatable(path)
        if exists:
            assert File.is_exists(path)
        self.path = File.clean(path)

    def __str__(self) -> str:
        return self.path

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.path == other
        elif isinstance(other, File):
            return self.path == other.path
        else:
            return False

    @staticmethod
    def clean(path: str) -> str:
        if not path:
            return ""
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        return path

    @staticmethod
    def is_creatable(path: str) -> bool:
        path = File.clean(path)
        dirname = os.path.dirname(path) or os.getcwd()
        return os.access(dirname, os.W_OK)

    @staticmethod
    def is_exists(path: str) -> bool:
        path = File.clean(path)
        return os.path.exists(path)

    def get_path(self) -> str:
        return self.path
