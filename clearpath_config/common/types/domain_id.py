class DomainID:
    def __init__(self, id: int = 0) -> None:
        self.assert_valid(id)
        self.id = id

    def __int__(self) -> int:
        return self.id

    @staticmethod
    def is_valid(id: int) -> bool:
        # Check Type
        if not isinstance(id, int):
            return False
        # 0-101 Range
        if not (0 <= id <= 101):
            return False
        return True

    @staticmethod
    def assert_valid(id: int) -> None:
        # Check Type
        assert isinstance(id, int), (
            "Domain ID must be an integer"
        )
        # 0 - 101 Range
        assert 0 <= id <= 101, (
            "Domain ID must be in range 0 - 101"
        )
        return
