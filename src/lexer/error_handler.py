from .token import TokenType
from enum import Enum

class Error(Enum):
    def __init__(self, error_type: str, message: str):
        self._error_type = error_type
        self._message = message

    @property
    def error_type(self):
        return self._error_type

    @property
    def message(self):
        return self._message
    
    OPEN_PAREN_FUNC = ("MISSING PARENTHESIS",
                       "No opening parenthesis was found on function declaration")

    DATA_TYPE_FUNC = ("MISSING DATATYPE",
                      "No data type was indicated on function declaration")
    
    INVALID_FUNC_DECLARE = ("INVALID FUNCTION NAME DECLARATION",
                            "Function name is missing a data type/parenthesis")
    
class CustomError:
    def __init__(self, error_type: Error, position: tuple[int,int], end_position: tuple[int,int] = None):
        self._error_type = error_type
        self._position = position
        self._end_position = end_position

    @property
    def error_type(self):
        return self._error_type.error_type

    @property
    def message(self):
        return self._error_type.message
    
    @property
    def position(self):
        return self._position

    @property
    def end_position(self):
        return self._end_position

    def __str__(self):
        log = ''
        log += f"[{self.error_type}] Error on line {self._position[0]}"
        if self.end_position:
            log += f" from column {self._position[1]} to {self._end_position[1]}"
        log += ':\n'
        log += f"\t{self.message}\n"
        return log

class DelimError:
    def __init__(self, token_type: TokenType, position: tuple[int] = None, temp_id: str = None, actual_delim: str = None,
                 fatal: bool = False):
        self.token_type = token_type
        self.position = position
        self.temp_id = temp_id
        self.actual_delim = actual_delim if actual_delim != '\n' else 'NEWLINE'

        self.error_type = f"UNTERMINATED {self.token_type.token.replace('_', ' ')}" if not fatal else 'FATAL'
        self.expected_delims = token_type.expected_delims

    def __str__(self):
        log = ""

        log += f"[{self.error_type}] Error on line {self.position[0]} column {self.position[1]}:\n"
        log += f"\texpected any of these characters: "

        for delim in self.expected_delims:
            delim = delim if delim != " " else "WHITESPACE"
            log += f"{delim} "
        log += f"\n\tafter {self.temp_id} but got {self.actual_delim} instead\n"

        return log
