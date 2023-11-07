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
    INPWT = ("INPWT_KEYWORD", "io")
    PWINT = ("PWINT_KEYWORD", "io")
    WETUWN = ("WETUWN_KEYWORD", "io")

    # CONTROL STRUCTURE KEYWORDS
    FOW = ("FOW_KEYWORD", "conditional")
    WHIWE = ("WHIWE_KEYWORD", "conditional")
    DO_WHIWE = ("DO_WHIWE_KEYWORD", "conditional")
    IWF = ("IWF_KEYWORD", "conditional")
    EWSE = ("EWSE_KEYWORD", "conditional")
    EWSE_IWF = ("EWSE_IWF_KEYWORD", "conditional")
    BWEAK = ("BWEAK_KEYWORD", "end")

    # DATA TYPES
    DATA_TYPE = ("GENERAL_DATA_TYPE", "data_type")  # only for dev
    CHAN = ("CHAN_DATA_TYPE", "data_type")  # int
    KUN = ("KUN_DATA_TYPE", "data_type")  # float
    SAMA = ("SAMA_DATA_TYPE", "data_type")  # boolean
    SENPAI = ("SENPAI_DATA_TYPE", "data_type")  # string
    SAN = ("SAN_DATA_TYPE", "data_type")  # void
    DONO = ("DONO_DATA_TYPE", "dono")  # constant

    # LITERALS
    NUWW = ("NUWW_LITERAL", "nuww")
    INT_LITERAL = ("INT_LITERAL", "int_float")
    FLOAT_LITERAL = ("FLOAT_LITERAL", "int_float")
    STRING_LITERAL = ("STRING_LITERAL", "string")
    STRING_PART_START = ("STRING_PART_START", "string_parts") # "|
    STRING_PART_MID = ("STRING_PART_MID", "string_parts") # ||
    STRING_PART_END = ("STRING_PART_END", "string") # |"
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
    GEN_IDENTIFIER = ("IDENTIFIER", "id")
    GEN_FUNC_NAME = ("FUNCTION_NAME", "function")
    GEN_CWASS_NAME = ("CWASS_NAME", "cwass")
    CWASS_TYPE = ("CWASS_TYPE", "cwass_type")
    SINGLE_LINE_COMMENT = ("COMMENT", "single_line_comment")
    MULTI_LINE_COMMENT = ("MULTI LINE COMMENT", "line")
    TYPE_INDICATOR = ("TYPE INDICATOR", 'type_indicator')


class UniqueTokenType:
    """
    A class for generating unique token types.
    Will have a unique token_type for every new lexeme read.
    """

    identifier_dict = {}
    fwunc_dict = {}
    cwass_dict = {}

    # Unique Token Types
    ID = "ID"
    FWUNC = "FWUNC"
    CWASS = "CWASS"
    CWASS_TYPE = "CWASS_TYPE"

    def __init__(self, lexeme: str, token: str):
        if token == self.ID:
            self._token = self.identifier_dict.setdefault(lexeme, f"IDENTIFIER_{len(self.identifier_dict) + 1}")
            self._delim_id = "id"
        elif token == self.FWUNC:
            self._token = self.fwunc_dict.setdefault(lexeme, f"FWUNC_{len(self.fwunc_dict) + 1}")
            self._delim_id = "function"
            print(self.fwunc_dict)
        elif token == self.CWASS:
            self._token = self.cwass_dict.setdefault(lexeme, f"CWASS_{len(self.cwass_dict) + 1}")
            self._delim_id = "cwass"
        elif token == self.CWASS_TYPE:
            if lexeme in self.cwass_dict:
                self._token = self.cwass_dict[lexeme]+"_TYPE"
                self._delim_id = "cwass_type"
            else:
                self._token = None
                return
        self._expected_delims = DELIMS[self.delim_id]

    @classmethod
    def clear(cls):
        cls.identifier_dict.clear()
        cls.fwunc_dict.clear()
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
