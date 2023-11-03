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
    
    # function errors
    FWUNC_OPEN_PAREN = ("MISSING PARENTHESIS",
                       "No opening parenthesis was found on function declaration")
    FWUNC_DATA_TYPE = ("MISSING DATATYPE",
                      "No data type was indicated on function declaration")
    INVALID_FUNC_DECLARE = ("INVALID FUNCTION NAME DECLARATION",
                            "Function name is missing a data type/parenthesis")
    MISSING_FWUNC = ("MISSING FWUNC KEYWORD",
                     "Function declarations need to have a 'fwunc' before to indicate it is a function")
    FWUNC_UPPERCASE = ("INVALID FUNCTION NAME",
                      'Function names should only start with a lowercase letter')
    
    # class errors
    CWASS_OPEN_PAREN = ("MISSING PARENTHESIS",
                       "No opening parenthesis was found on class declaration")
    CWASS_DATA_TYPE = ("MISSING DATATYPE",
                      "No data type was indicated on class declaration")
    INVALID_CWASS_DECLARE = ("INVALID CLASS NAME DECLARATION",
                            "class name is missing a data type/parenthesis")
    MISSING_CWASS = ("MISSING CWASS KEYWORD",
                     "Class declarations need to have a 'cwass' before to indicate it is a class")
    CWASS_LOWERCASE = ("INVALID CLASS NAME",
                      'Class names should only start with an uppercase letter')

    # string errors    
    UNCLOSED_STRING = ("UNCLOSED STRING",
                       'String literals should be closed with "')
    
    # int/float errors
    OUT_OF_BOUNDS_INT_FLOAT = ("OUT OF BOUNDS",
                               'chan and kun literals can only have up to 10 digits before and after the decimal (kun can have a max of 20 digits total)')
    MULTIPLE_DECIMAL_POINT = ('MULTIPLE DECIMAL POINT',
                              "kun literals can only have 1 decimal point")
    
    # identifier errors
    IDEN_INVALID_START = ("INVALID START OF IDENTIFIER",
                          'identifiers can only start with lowercase/uppercase letters')
    IDEN_INVALID_NAME = ("INVALID IDENTIFIER NAME",
                         'identifiers can only have alphanumeric characters')
    
    
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
    
    LEADING_ZEROES_INT = ("LEADING ZEROES",
                      'chan literals should not have leading zeroes',)
        
    LEADING_ZEROES_FLOAT = ("LEADING ZEROES",
                      "kun literals can have ONE leading zero before the decimal point ONLY IF it's the only digit present (0.1)")
    
    TRAILING_ZEROES_FLOAT = ("TRAILING ZEROES",
                      "kun literals can have ONE trailing zero after the decimal point ONLY IF it's the only digit present (1.0)")
    
    MISSING_TRAILING_ZERO_FLOAT = ("MISSING TRAILING ZERO",
                                   "kun literals should have digit/s present after the decimal point")
    
class GenericError:
    def __init__(self, error_type: Error, position: tuple[int,int], end_position: tuple[int,int] = None, context: str = None):
        self._error_type = error_type
        self._position = position
        self._end_position = end_position
        self._context = context

    def __str__(self):
        log = ''
        log += f"[{self.error_type}] Error on line {self._position[0]}"
        if self.end_position:
            log += f" from column {self._position[1]} to {self._end_position[1]}"
        log += ':\n'
        log += f"\t{self.message}\n"
        if self.context:
            log += f'\t{self.context}\n'
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

        log += f"[{self.warn_type}] Warning on line {self._position[0]}"

        if self.end_position:
            log += f" from column {self._position[1]} to {self._end_position[1]}"

        log += ':\n'
        log += f"\t{self.message}\n"
        if self.context:
            log += f'\t{self.context}\n'
        else:
            log += f"\tvalue = '{self.temp_num}' --> corrected value = '{self.corrected_value}'\n"
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