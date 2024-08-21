class TarotNotFoundError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message


class InvalidDateTimeError(Exception):
    def __init__(self, message: str) -> None:
        self.message: str = message



