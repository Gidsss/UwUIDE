from enum import Enum


class ErrorType(Enum):
    UNTERMINATED_ID = "UNTERMINATED IDENTIFIER"
    UNTERMINATED_OPERATOR = "UNTERMINATED OPERATOR"
    UNTERMINATED_KEYWORD = "UNTERMINATED KEYWORD"


class Error:
    def __init__(self, error_type: str, position: tuple[int], temp_id: str,
                 expected_delims: list[str], actual_delim: str):
        self.error_type = error_type if error_type else "FATAL"
        self.position = position
        self.temp_id = temp_id
        self.expected_delims = expected_delims
        self.actual_delim = actual_delim

    def __str__(self):
        log = ""

        log += f"[{self.error_type}] Error on line {self.position[0]} column {self.position[1]}:\n"
        log += f"\texpected any of these characters: "

        for delim in self.expected_delims:
            delim = delim if delim != " " else "WHITESPACE"
            log += f"{delim} "
        log += f"\n\tafter {self.temp_id} but got {self.actual_delim} instead\n"

        return log

