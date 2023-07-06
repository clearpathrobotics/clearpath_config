import re


# Username
class Username:
    def __init__(self, username: str = "administrator") -> None:
        self.assert_valid(username)
        self.username = username

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.username == other
        elif isinstance(other, Username):
            return self.username == other.username
        return False

    def __str__(self) -> str:
        return self.username

    @staticmethod
    def is_valid(username: str):
        # Check Type
        if not isinstance(username, str):
            return False
        # Max 255 Characters
        if len(username) > 255:
            return False
        # Convention
        # - [a-z] lowercase characters
        # - [0-9] numbers
        # - underscores
        # - dashes
        # - may end in $
        allowed = re.compile(r"[-a-z0-9_]")
        return all(allowed.match(c) for c in username)

    @staticmethod
    def assert_valid(username: str):
        # Check Type
        assert isinstance(username, str), (
            "Username '%s' must of type 'str'" % username
        )
        # Max 255 Characters
        assert len(username) < 256, (
            "Username '%s' exceeds 255 ASCII character limit." % username
        )
        # Regex Convention
        allowed = re.compile(r"[-a-z0-9_]")
        assert all(allowed.match(c) for c in username), (
            "Username '%s' cannot contain characters other than: %s, %s, %s, %s" % (
                username,
                "lowercase letters",
                "digits",
                "underscores",
                "dashes"
            )
        )
