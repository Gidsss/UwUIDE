from constants.constants import DELIMS
from enum import Enum


class TokenType(Enum):
    def __init__(self, token: str, delim_id: str):
        self._token = token
        self._delim_id = delim_id
        self._expected_delims = DELIMS[self.delim_id]

    @property
    def token(self):
        return self._token

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

    # GENERAL KEYWORDS
    START = ("staart!", "start_done")
    DONE = ("donee~", "start_done")
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
        if token == self.ID:
            self._token = self.identifier_dict.setdefault(lexeme, f"IDENTIFIER_{len(self.identifier_dict) + 1}")
            self._delim_id = "id"
        elif token == self.CWASS:
            self._token = self.cwass_dict.setdefault(lexeme, f"CWASS_{len(self.cwass_dict) + 1}")
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
    def delim_id(self):
        return self._delim_id

    @property
    def expected_delims(self):
        return self._expected_delims

    def __str__(self):
        return self.token
    
    def __format__(self, format_spec):
        return str.__format__(str(self), format_spec)


class Token:
    'A class for representing tokens in a lexer'

    def __init__(self, lexeme: str, token: TokenType, position: tuple[int, int], end_position: tuple[int, int]):
        self._lexeme = lexeme
        self._token = token
        self._position = position
        self._end_position = end_position

    def __repr__(self):
        return f"Token(lexeme='{self.lexeme}', token='{self.token}', position={self.position}, end_position={self.end_position})"

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
