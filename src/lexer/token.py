from constants.constants import DELIMS
from enum import Enum
from copy import copy, deepcopy

class TokenType(Enum):
    def __init__(self, token: str, delim_id: str):
        self._token = token
        self._delim_id = delim_id
        self._expected_delims = DELIMS[self.delim_id]

    @property
    def token(self):
        return self._token
    @property
    def unique_type(self):
        return self._token

    @property
    def delim_id(self):
        return self._delim_id

    @property
    def expected_delims(self):
        return self._expected_delims

    def __str__(self):
        return self.token
    def string(self, indent = 1):
        return self.__str__()
    def flat_string(self, indent = 1):
        return self.__str__()
    def python_string(self, indent = 1):
        return self.__str__()
    def header(self):
        return self.token

    def __format__(self, format_spec):
        return str.__format__(str(self), format_spec)

    def to_arr_type(self) -> "TokenType":
        match self:
            case TokenType.CHAN:
                return TokenType.CHAN_ARR
            case TokenType.KUN:
                return TokenType.KUN_ARR
            case TokenType.SAMA:
                return TokenType.SAMA_ARR
            case TokenType.SAN:
                return TokenType.SAN_ARR
            case TokenType.SENPAI:
                return TokenType.SENPAI_ARR
            case _:
                return self
    def is_arr_type(self):
        match self:
            case TokenType.CHAN_ARR | TokenType.KUN_ARR | TokenType.SAMA_ARR | TokenType.SAN_ARR | TokenType.SENPAI_ARR:
                return True
            case _:
                return False

    def to_unit_type(self) -> "TokenType":
        match self:
            case TokenType.CHAN_ARR:
                return TokenType.CHAN
            case TokenType.KUN_ARR:
                return TokenType.KUN
            case TokenType.SAMA_ARR:
                return TokenType.SAMA
            case TokenType.SAN_ARR:
                return TokenType.SAN
            case TokenType.SENPAI_ARR:
                return TokenType.SENPAI
            case _:
                return self

    # GENERAL KEYWORDS
    MAINUWU = ("mainuwu", "mainuwu")
    FWUNC = ("fwunc", "whitespace")
    CWASS = ("cwass", "whitespace")
    GWOBAW = ("gwobaw", "whitespace")
    INPWT = ("inpwt", "io")
    PWINT = ("pwint", "io")
    WETUWN = ("wetuwn", "io")

    # CONTROL STRUCTURE KEYWORDS
    FOW = ("fow", "conditional")
    WHIWE = ("whiwe", "conditional")
    DO_WHIWE = ("do whiwe", "conditional")
    IWF = ("iwf", "conditional")
    EWSE = ("ewse", "conditional")
    EWSE_IWF = ("ewse iwf", "conditional")
    BWEAK = ("bweak", "end")

    # DATA TYPES
    DATA_TYPE = ("GENERAL_DATA_TYPE", "data_type")  # only for dev
    CHAN = ("chan", "data_type")  # int
    KUN = ("kun", "data_type")  # float
    SAMA = ("sama", "data_type")  # boolean
    SENPAI = ("senpai", "data_type")  # string
    SAN = ("san", "data_type")  # void
    DONO = ("dono", "dono")  # constant
    CHAN_ARR = ("chan[]", "data_type")  # int[]
    KUN_ARR = ("kun[]", "data_type")  # float[]
    SAMA_ARR = ("sama[]", "data_type")  # boolean[]
    SENPAI_ARR = ("senpai[]", "data_type")  # string[]
    SAN_ARR = ("san[]", "data_type")  # void[]

    # LITERALS
    NUWW = ("nuww", "nuww")
    INT_LITERAL = ("INT_LITERAL", "int_float")
    FLOAT_LITERAL = ("FLOAT_LITERAL", "int_float")
    STRING_LITERAL = ("STRING_LITERAL", "string")
    STRING_PART_START = ("STRING_PART_START", "string_parts") # "|
    STRING_PART_MID = ("STRING_PART_MID", "string_parts") # ||
    STRING_PART_END = ("STRING_PART_END", "string") # |"
    FAX = ("fax", "bool")
    CAP = ("cap", "bool")

    # OPERATORS
    ASSIGNMENT_OPERATOR = ("=", "assign_delim")
    ADDITION_SIGN = ("+", "operator_delim")
    DASH = ("-", "operator_delim")
    MULTIPLICATION_SIGN = ("*", "operator_delim")
    DIVISION_SIGN = ("/", "operator_delim")
    MODULO_SIGN = ("%", "operator_delim")
    GREATER_THAN_SIGN = (">", "operator_delim")
    LESS_THAN_SIGN = ("<", "operator_delim")
    GREATER_THAN_OR_EQUAL_SIGN = (">=", "operator_delim")
    LESS_THAN_OR_EQUAL_SIGN = ("<=", "operator_delim")
    EQUALITY_OPERATOR = ("==", "logical_delim")
    INEQUALITY_OPERATOR = ("!=", "logical_delim")
    AND_OPERATOR = ("&&", "logical_delim")
    OR_OPERATOR = ("||", "logical_delim")
    INCREMENT_OPERATOR = ("++", "unary")
    DECREMENT_OPERATOR = ("--", "unary")
    CONCATENATION_OPERATOR = ("&", "concat")  # &

    # GROUPING SYMBOLS
    OPEN_BRACE = ("{", "open_brace")  # {
    CLOSE_BRACE = ("}", "close_brace")  # }
    OPEN_PAREN = ("(", "open_parenthesis")  # (
    CLOSE_PAREN = (")", "close_parenthesis")  # )
    OPEN_BRACKET = ("[", "open_bracket")  # [
    CLOSE_BRACKET = ("]", "close_bracket")  # ]
    DOUBLE_OPEN_BRACKET = ("[[", "double_open_bracket")  # [[
    DOUBLE_CLOSE_BRACKET = ("]]", "double_close_bracket")  # ]]

    # OTHER SYMBOLS
    TERMINATOR = ("~", "line")  # ~
    COMMA = (",", "comma")  # ,
    DOT_OP = (".", "dot_op")  # .

    # OTHER
    GEN_IDENTIFIER = ("IDENTIFIER", "id")
    GEN_CWASS_NAME = ("CWASS_NAME", "cwass")
    SINGLE_LINE_COMMENT = ("COMMENT", "single_line_comment")
    MULTI_LINE_COMMENT = ("MULTI LINE COMMENT", "line")
    WHITESPACE = ("WHITESPACE", "all")
    EOF = ("EOF", "all")

    MIXED_ARRAY = ("MIXED_ARRAY", "all")

class UniqueTokenType:
    """
    A class for generating unique token types.
    Will have a unique token_type for every new lexeme read.
    """

    identifier_dict = {}
    cwass_dict = {}

    # Unique Token Types
    ID = "ID"
    CWASS = "CWASS"

    def __init__(self, lexeme: str, token: str):
        self._token = lexeme
        if token == self.ID:
            self._type = self.identifier_dict.setdefault(lexeme, f"IDENTIFIER_{len(self.identifier_dict) + 1}")
            self._delim_id = "id"
        elif token == self.CWASS:
            self._type = self.cwass_dict.setdefault(lexeme, f"CWASS_{len(self.cwass_dict) + 1}")
            self._delim_id = "cwass"
        self._expected_delims = DELIMS[self.delim_id]

    @classmethod
    def clear(cls):
        cls.identifier_dict.clear()
        cls.cwass_dict.clear()

    @property
    def token(self):
        return self._token

    @property
    def unique_type(self):
        """The lexeme property."""
        return self._type

    @property
    def delim_id(self):
        return self._delim_id

    @property
    def expected_delims(self):
        return self._expected_delims

    def __str__(self):
        return self.token
    
    def __format__(self, format_spec):
        return str.__format__(str(self), format_spec)

    def string(self, indent = 1):
        return self.__str__()
    def flat_string(self):
        return self.__str__()
    def python_string(self):
        return self.__str__()
    def header(self):
        return self.__str__()
    def __repr__(self):
        return self.token

    def to_arr_type(self):
        self._token += "[]"
        return self
    def to_unit_type(self):
        self._token = self._token[:-2] if self._token.endswith("[]") else self._token
        return self
    def is_arr_type(self):
        return self.token.endswith("[]")


class Token:
    'A class for representing tokens in a lexer'

    def __init__(self, lexeme: str = "", token: TokenType = TokenType.EOF, position: tuple[int, int] = (0, 0), end_position: tuple[int, int] = (0, 0)):
        self._lexeme = lexeme
        self._token = token
        self._position = position
        self._end_position = end_position

    def __repr__(self):
        return self._lexeme
    def __str__(self):
        return self._lexeme

    ### For Production interface
    def string(self, indent = 1) -> str:
        return self._lexeme
    def flat_string(self) -> str:
        return self._lexeme
    def python_string(self, indent = 1) -> str:
        return self._lexeme
    def header(self):
        return self._lexeme

    def to_arr(self):
        self._lexeme += "[]" if not self._lexeme.endswith("[]") else ""
        match self.token:
            case TokenType.CHAN:
                self._token = TokenType.CHAN_ARR
            case TokenType.KUN:
                self._token = TokenType.KUN_ARR
            case TokenType.SAMA:
                self._token = TokenType.SAMA_ARR
            case TokenType.SAN:
                self._token = TokenType.SAN_ARR
            case TokenType.SENPAI:
                self._token = TokenType.SENPAI_ARR
            case UniqueTokenType():
                self._token = self.token.to_arr_type()

    def is_arr_type(self):
        return self.token.is_arr_type()

    def to_unit_type(self):
        ret = deepcopy(self)
        ret._lexeme = self._lexeme[:-2] if self._lexeme.endswith("[]") else self._lexeme
        match ret.token:
            case TokenType.CHAN_ARR:
                ret._token = TokenType.CHAN
            case TokenType.KUN_ARR:
                ret._token = TokenType.KUN
            case TokenType.SAMA_ARR:
                ret._token = TokenType.SAMA
            case TokenType.SAN_ARR:
                ret._token = TokenType.SAN
            case TokenType.SENPAI_ARR:
                ret._token = TokenType.SENPAI
            case UniqueTokenType():
                ret._token = ret._token.to_unit_type()
        return ret

    @property
    def lexeme(self) -> str:
        return self._lexeme

    @lexeme.setter
    def lexeme(self, lexeme: str):
        self._lexeme = lexeme

    @property
    def token(self) -> TokenType:
        return self._token

    @token.setter
    def token(self, token: TokenType):
        self._token = token

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, position: tuple[int, int]):
        self._position = position

    @property
    def end_position(self) -> tuple[int, int]:
        return self._end_position

    @end_position.setter
    def end_position(self, end_position: tuple[int, int]):
        self._end_position = end_position
