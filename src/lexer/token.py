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

    # GENERAL KEYWORDS
    START = ("START_KEYWORD", "start_done")
    DONE = ("DONE_KEYWORD", "start_done")
    MAINUWU = ("MAINUWU_KEYWORD", "mainuwu")
    FWUNC = ("FWUNC_KEYWORD", "whitespace")
    CWASS = ("CWASS_KEYWORD", "whitespace")
    GWOBAW = ("GWOBAW_KEYWORD", "whitespace")
    INPWT = ("INPWT_KEYWORD", "function")
    PWINT = ("PWINT_KEYWORD", "function")
    WETUWN = ("WETUWN_KEYWORD", "function")

    # CONTROL STRUCTURE KEYWORDS
    FOW = ("FOW_KEYWORD", "conditional")
    WHIWE = ("WHIWE_KEYWORD", "conditional")
    DO_WHIWE = ("DO_WHIWE_KEYWORD", "conditional")
    IWF = ("IWF_KEYWORD", "conditional")
    EWSE = ("EWSE_KEYWORD", "conditional")
    EWSE_IF = ("EWSE_IF_KEYWORD", "conditional")
    BWEAK = ("BWEAK_KEYWORD", "end")

    # DATA TYPES
    DATA_TYPE = ("GENERAL_DATA_TYPE", "data_type")  # only for dev
    CHAN = ("CHAN_DATA_TYPE", "data_type")  # int
    KUN = ("KUN_DATA_TYPE", "data_type")  # float
    SAMA = ("SAMA_DATA_TYPE", "data_type")  # boolean
    SENPAI = ("SENPAI_DATA_TYPE", "data_type")  # string
    SAN = ("SAN_DATA_TYPE", "data_type")  # void
    DONO = ("DONO_DATA_TYPE", "data_type")  # constant

    # LITERALS
    NUWW = ("NUWW_LITERAL", "nuww")
    INT_LITERAL = ("INT_LITERAL", "int_float")
    FLOAT_LITERAL = ("FLOAT_LITERAL", "int_float")
    STRING_LITERAL = ("STRING_LITERAL", "string")
    BOOL_LITERAL = ("BOOLEAN_LITERAL", "bool")  # fax, cap

    # OPERATORS
    ASSIGN = ("ASSIGNMENT_OPERATOR", "assign_delim")  # =
    ARITHMETIC = ("ARITHMETIC_OPERATOR", "operator_delim")  # + - * / %
    RELATIONAL = ("RELATIONAL_OPERATOR", "operator_delim")  # > < >= <=
    EQUALITY = ("EQUALITY_OPERATOR", "logical_delim")  # == !=
    LOGIC = ("LOGICAL_OPERATOR", "logical_delim")  # && ||
    UNARY = ("UNARY_OPERATOR", "unary")  # ++ --
    CONCAT = ("CONCATENATION_OPERATOR", "concat")  # &

    # GROUPING SYMBOLS
    OPEN_BRACE = ("OPEN_BRACE", "open_brace")  # {
    CLOSE_BRACE = ("CLOSE_BRACE", "close_brace")  # }
    OPEN_PAREN = ("OPEN_PARENTHESIS", "open_parenthesis")  # (
    CLOSE_PAREN = ("CLOSE_PARENTHESIS", "close_parenthesis")  # )
    OPEN_BRACKET = ("OPEN_BRACKET", "open_bracket")  # [
    CLOSE_BRACKET = ("CLOSE_BRACKET", "close_bracket")  # ]
    DOUBLE_OPEN_BRACKET = ("DOUBLE_OPEN_BRACKET", "double_open_bracket")  # [[
    DOUBLE_CLOSE_BRACKET = ("DOUBLE_CLOSE_BRACKET", "double_close_bracket")  # ]]

    # OTHER SYMBOLS
    TERMINATOR = ("TERMINATOR", "line")  # ~
    COMMA = ("COMMA", "comma")  # ,
    DOT_OP = ("DOT_OPERATOR", "dot_op")  # .
    NEGATIVE = ("NEGATIVE_SIGN", "negative_delim")  # -

    # OTHER
    IDENTIFIER = ("IDENTIFIER", "id")


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
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str):
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
