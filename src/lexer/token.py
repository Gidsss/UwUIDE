from constants.constants import DELIMS


class TokenTypes():
    class TokenType:
        def __init__(self, token: str, delim_id: str, error_type: str = None):
            self.token = token
            self.delim_id = delim_id
            self.error_type = f"UNTERMINATED {self.token.replace('_', ' ')}" if error_type is None else error_type

            self.expected_delims = DELIMS[self.delim_id]

        def __str__(self):
            return self.token

    # GENERAL KEYWORDS
    START = TokenType("START_KEYWORD", "start_done")
    DONE = TokenType("DONE_KEYWORD", "start_done")
    MAINUWU = TokenType("MAINUWU_KEYWORD", "mainuwu")
    FWUNC = TokenType("FWUNC_KEYWORD", "whitespace")
    CWASS = TokenType("CWASS_KEYWORD", "whitespace")
    GWOBAW = TokenType("GWOBAW_KEYWORD", "whitespace")
    INPUT = TokenType("I-INPUT_KEYWORD", "function")
    PWINT = TokenType("P-PWINT_KEYWORD", "function")
    WETUWN = TokenType("WETUWN_KEYWORD", "function")

    # CONTROL STRUCTURE KEYWORDS
    FOW = TokenType("FOW_KEYWORD", "conditional")
    WHIWE = TokenType("WHIWE_KEYWORD", "conditional")
    DO_WHIWE = TokenType("DO_WHIWE_KEYWORD", "conditional")
    IWF = TokenType("IWF_KEYWORD", "conditional")
    EWSE = TokenType("EWSE_KEYWORD", "conditional")
    EWSE_IF = TokenType("EWSE_IF_KEYWORD", "conditional")
    BWEAK = TokenType("BWEAK_KEYWORD", "end")

    # DATA TYPES
    CHAN = TokenType("CHAN_DATA_TYPE", "data_type")  # int
    KUN = TokenType("KUN_DATA_TYPE", "data_type")  # float
    SAMA = TokenType("SAMA_DATA_TYPE", "data_type")  # boolean
    SENPAI = TokenType("SENPAI_DATA_TYPE", "data_type")  # string
    SAN = TokenType("SAN_DATA_TYPE", "data_type")  # void
    DONO = TokenType("DONO_DATA_TYPE", "data_type")  # constant

    # LITERALS
    NUWW = TokenType("NUWW_LITERAL", "nuww")
    INT_LITERAL = TokenType("INT_LITERAL", "int_float")
    FLOAT_LITERAL = TokenType("FLOAT_LITERAL", "int_float")
    STRING_LITERAL = TokenType("STRING_LITERAL", "string")
    BOOL_LITERAL = TokenType("BOOLEAN_LITERAL", "bool")     # fax, cap

    # OPERATORS
    ASSIGN = TokenType("ASSIGNMENT_OPERATOR", "assign_delim")  # =
    ARITHMETIC = TokenType("ARITHMETIC_OPERATOR", "operator_delim")  # + - * / %
    RELATIONAL = TokenType("RELATIONAL_OPERATOR", "operator_delim")  # > < >= <= == !=
    LOGIC = TokenType("LOGICAL_OPERATOR", "logical_delim")  # && ||
    UNARY = TokenType("UNARY_OPERATOR", "unary")  # ++ --
    CONCAT = TokenType("CONCATENATION_OPERATOR", "concat")  # &

    # GROUPING SYMBOLS
    OPEN_BRACE = TokenType("OPEN_BRACE", "open_brace")
    CLOSE_BRACE = TokenType("CLOSE_BRACE", "close_brace")
    OPEN_PAREN = TokenType("OPEN_PARENTHESIS", "open_parenthesis")
    CLOSE_PAREN = TokenType("CLOSE_PARENTHESIS", "close_parenthesis")
    OPEN_BRACKET = TokenType("OPEN_BRACKET", "open_bracket")
    CLOSE_BRACKET = TokenType("CLOSE_BRACKET", "close_bracket")
    DOUBLE_OPEN_BRACKET = TokenType("DOUBLE_OPEN_BRACKET", "double_open_bracket")
    DOUBLE_CLOSE_BRACKET = TokenType("DOUBLE_CLOSE_BRACKET", "double_close_bracket")

    # OTHER SYMBOLS
    TERMINATOR = TokenType("TERMINATOR", "line")
    COMMA = TokenType("COMMA", "comma")
    DOT_OP = TokenType("DOT_OPERATOR", "dot_op")

    # OTHER
    IDENTIFIER = TokenType("IDENTIFIER", "id")

class Token:
    'A class for representing tokens in a lexer'

    def __init__(self, lexeme: str, token: TokenTypes, position: tuple[int, int], end_position: tuple[int, int]):
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
