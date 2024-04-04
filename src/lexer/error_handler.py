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
    
    # string errors    
    UNCLOSED_STRING = ("UNCLOSED STRING",
                       'String literals should be closed with "')
    
    # int/float errors
    OUT_OF_BOUNDS_INT_FLOAT = ("OUT OF BOUNDS",
                               'chan and kun literals can only have up to 10 digits before and after the decimal (kun can have a max of 20 digits total)')
    MULTIPLE_DECIMAL_POINT = ('MULTIPLE DECIMAL POINT',
                              "kun literals can only have 1 decimal point")
    MISSING_TRAILING_ZERO_FLOAT = ("MISSING TRAILING ZERO",
                                   "kun literals should have digit/s present after the decimal point")
    # ints/floats
    LEADING_ZEROES_INT = ("LEADING ZEROES",
                      'chan literals should not have leading zeroes',)
    LEADING_ZEROES_FLOAT = ("LEADING ZEROES",
                      "kun literals can have ONE leading zero before the decimal point ONLY IF it's the only digit present (0.1)")
    TRAILING_ZEROES_FLOAT = ("TRAILING ZEROES",
                      "kun literals can have ONE trailing zero after the decimal point ONLY IF it's the only digit present (1.0)")

    # symbol errors
    UNEXPECTED_SYMBOL = ("UNEXPECTED SYMBOL",
                         "Lexeme does not map to an appropriate token type")
    
    
class Warn(Enum):
    def __init__(self, warn_type: str, message: str):
        self._warn_type = warn_type
        self._message = message

    @property
    def warn_type(self):
        return self._warn_type

    @property
    def message(self):
        return self._message
    
    # multi line comment
    UNCLOSED_MULTI_LINE_COMMENT = ("UNCLOSED MULTI LINE COMMENT",
                                   "All code after the opening indicator >//< will be treated as a comment")
    
class GenericError:
    def __init__(self, error_type: Error, position: tuple[int,int], end_position: tuple[int,int] = None, context: str = None):
        self._error_type = error_type
        self._position = position
        self._end_position = end_position if position != end_position else None
        self._context = context

    def __str__(self):
        log = ''
        log += f"[{self.error_type}] Error on line {self._position[0] + 1}"
        if self.end_position:
            log += f" from column {self._position[1]} to {self._end_position[1]}"
        else:
            log += f" column {self._position[1]}"
        log += ':\n'
        log += f"\t{self.message}\n"
        if self.context:
            log += f'\t{self.context}\n'

        # Error preview
        error_range = 1 if self.end_position is None else self.end_position[1] - self.position[1] + 1
        index_str = str(self.position[0] + 1)
        border = f"\t{'_' * (len(ErrorSrc.src[self.position[0]]) + len(index_str) + 3)}\n"
        log += border
        log += f"\t{index_str} | {ErrorSrc.src[self.position[0]]}\n"
        log += f"\t{' ' * len(index_str)} | {' '*self.position[1]}{'^'*error_range}\n"
        log += border
        return log
    
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
    
    @property
    def context(self):
        return self._context


class DelimError:
    def __init__(self, token_type: TokenType, position: tuple[int], temp_id: str, actual_delim: str,
                 fatal: bool = False):
        self.token_type = token_type
        self.position = position
        self.temp_id = temp_id
        self.actual_delim = actual_delim if actual_delim != '\n' else 'NEWLINE'

        self.error_type = f"UNDELIMITED {self.token_type.token.replace('_', ' ')}" if not fatal else 'FATAL'
        self.expected_delims = token_type.expected_delims

    def __str__(self):
        log = ""

        log += f"[{self.error_type}] Error on line {self.position[0] + 1} column {self.position[1]}:\n"
        log += f"\texpected any of these characters: "

        for delim in self.expected_delims:
            delim = delim if delim != " " else "WHITESPACE"
            delim = delim if delim != "\n" else "NEWLINE"
            log += f"{delim} "
        log += f"\n\tafter {self.temp_id} but got {self.actual_delim if self.actual_delim != ' ' else 'WHITESPACE'} instead\n"

        # Error preview
        index_str = str(self.position[0] + 1)
        border = f"\t{'_' * (len(ErrorSrc.src[self.position[0]]) + len(index_str) + 3)}\n"
        log += border
        log += f"\t{index_str} | {ErrorSrc.src[self.position[0]]}\n"
        log += f"\t{' ' * len(index_str)} | {' ' * self.position[1]}{'^'}\n"
        log += border

        return log

class IntFloatWarning:
    def __init__(self, warn_type: Warn, corrected_value: str, temp_num: str, position: tuple[int,int], end_position: tuple[int,int], context: str = None):
        self._warn_type = warn_type
        self._corrected_value = corrected_value
        self._temp_num = temp_num
        self._position = position
        self._end_position = end_position
        self._context = context

    def __str__(self):
        log = ''

        log += f"[{self.warn_type}] Warning on line {self._position[0] + 1}"

        if self.end_position:
            log += f" from column {self._position[1]} to {self._end_position[1]}"

        log += ':\n'
        log += f"\t{self.message}\n"
        if self.context:
            log += f'\t{self.context}\n'
        else:
            log += f"\tvalue = '{self.temp_num}' --> corrected value = '{self.corrected_value}'\n"

        # Error preview
        error_range = 1 if self.end_position is None else self.end_position[1] - self.position[1] + 1
        index_str = str(self.position[0] + 1)
        border = f"\t{'_'*(len(ErrorSrc.src[self.position[0]]) + len(index_str) + 3)}\n"
        log += border
        log += f"\t{index_str} | {ErrorSrc.src[self.position[0]]}\n"
        log += f"\t{' ' * len(index_str)} | {' ' * self.position[1]}{'^' * error_range}\n"
        log += border

        return log

    @property
    def warn_type(self) -> str:
        if isinstance(self._warn_type, Warn):
            return self._warn_type.warn_type
        else:
            return self._warn_type.error_type

    @property
    def message(self):
        return self._warn_type.message

    @property
    def corrected_value(self) -> str:
        return self._corrected_value
    
    @property
    def temp_num(self) -> str:
        return self._temp_num
    
    @property
    def position(self) -> str:
        return self._position

    @property
    def end_position(self) -> str:
        return self._end_position
    
    @property
    def context(self) -> str:
        return self._context
    

class GenericWarning:
    def __init__(self, warn_type: Error, position: tuple[int,int], end_position: tuple[int,int] = None, context: str = None):
        self._warn_type = warn_type
        self._position = position
        self._end_position = end_position
        self._context = context

    def __str__(self):
        log = ''
        log += f"[{self.warn_type}] Warning on line {self._position[0] + 1}"
        if self.end_position:
            log += f" from column {self._position[1]} to {self._end_position[1]}"
        log += ':\n'
        log += f"\t{self.message}\n"
        if self.context:
            log += f'\t{self.context}\n'

        # Error preview
        error_range = 1 if self.end_position is None else self.end_position[1] - self.position[1] + 1
        index_str = str(self.position[0] + 1)
        border = f"\t{'_' * (len(ErrorSrc.src[self.position[0]]) + len(index_str) + 3)}\n"
        log += border
        log += f"\t{index_str} | {ErrorSrc.src[self.position[0]]}\n"
        log += f"\t{' ' * len(index_str)} | {' ' * self.position[1]}{'^' * error_range}\n"
        log += border

        return log
    
    @property
    def warn_type(self):
        return self._warn_type.warn_type

    @property
    def message(self):
        return self._warn_type.message
    
    @property
    def position(self):
        return self._position

    @property
    def end_position(self):
        return self._end_position
    
    @property
    def context(self):
        return self._context


class ErrorSrc:
    src = [""]
