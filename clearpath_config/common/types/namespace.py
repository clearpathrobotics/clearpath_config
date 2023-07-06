import re


class Namespace:
    def __init__(
            self,
            name: str = "/"
            ) -> None:
        self.assert_valid(name)
        self.name = name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Namespace):
            return self.name == other.name
        else:
            return False

    def __str__(self) -> str:
        return str(self.name)

    @staticmethod
    def is_valid(name: str) -> bool:
        # Must not be Empty
        if name == "":
            return False
        # Must Contain:
        #  - [0-9|a-z|A-Z]
        #  - Underscores (_)
        #  - Forward Slashed (/)
        allowed = re.compile("[a-z|0-9|_|/|~]", re.IGNORECASE)
        if not all(allowed.match(c) for c in name):
            return False
        # May start with (~) but be followed by (/)
        if name[0] == "~":
            if name[1] != "/":
                return False
        # Must not Start with Digit [0-9], May Start with (~)
        if str(name[0]).isdigit():
            return False
        # Must not End with Forward Slash (/)
        if name[-1] == "/":
            return False
        # Must not contain any number of repeated forward slashed (/)
        if "//" in name:
            return False
        # Must not contain any number of repeated underscores (_)
        if "__" in name:
            return False

    @staticmethod
    def assert_valid(name: str) -> None:
        # Empty
        assert name != "", (
            "Namespace cannot be empty"
        )
        # Allowed characters
        allowed = re.compile("[a-z|0-9|_|/|~]", re.IGNORECASE)
        assert all(allowed.match(c) for c in name), ("\n".join([
            "Namespace can only contain:",
            " - [A-Z|a-z|0-9]",
            " - underscores (_)",
            " - forward slahes (/)",
            " - leading tilde (~)"
        ]))
        # Leading Tilde (~)
        if name[0] == "~":
            assert name[1] == "/", (
                "Namespace starting with (~) must be followed by (/)"
            )
        # Leading Digit
        assert not str(name[0]).isdigit(), (
            "Namespace may not start with a digit"
        )
        # Ending Forward Slash (/)
        assert len(name) == 1 or name[-1] != "/", (
            "Namespace may not end with a forward slash (/)"
        )
        # Repeated Forward Slash (/)
        assert "//" not in name, (
            "Namespace may not contain repeated forward slashes (/)"
        )
        # Repeated Underscores (/)
        assert "__" not in name, (
            "Namespace may not contain repeated underscores (_)"
        )

    @staticmethod
    def clean(name: str) -> str:
        # Swap dashes to underscores
        clean = name.replace("-", "_")
        # Remove repeated forward slashes
        while "//" in clean:
            clean = clean.replace("//", "/")
        # Remove repeated underscores
        while "__" in clean:
            clean = clean.replace("__", "_")
        return clean
