from enum import Enum


class ErrorType(Enum):
    ID = "UNTERMINATED IDENTIFIER"
    OPERATOR = "UNTERMINATED OPERATOR"
    KEYWORD = "UNTERMINATED KEYWORD"
    BWEAK = "UNTERMINATED BWEAK"
    DATA_TYPE = "UNTERMINATED DATA TYPE"
    BOOL = "UNTERMINATED BOOL VALUE"
    UNARY = "UNTERMINATED UNARY OPERATOR"


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

        log += f"[{self.error_type.value}] Error on line {self.position[0]} column {self.position[1]}:\n"
        log += f"\texpected any of these characters: "

        for delim in self.expected_delims:
            delim = delim if delim != " " else "WHITESPACE"
            log += f"{delim} "
        log += f"\n\tafter {self.temp_id} but got {self.actual_delim} instead\n"

        return log

