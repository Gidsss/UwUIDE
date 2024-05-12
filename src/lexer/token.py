import re
from constants.constants import DELIMS
from enum import Enum
from copy import deepcopy

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
    def python_string(self, indent = 1, cwass=False):
        'should only be used for dtypes'
        match self:
            case TokenType.CHAN:
                return "Int"
            case TokenType.CHAN_ARR:
                return "Array"
            case TokenType.KUN:
                return "Float"
            case TokenType.KUN_ARR:
                return "Array"
            case TokenType.SAMA:
                return "Bool"
            case TokenType.SAMA_ARR:
                return "Array"
            case TokenType.SAN:
                return "NoneType"
            case TokenType.SAN_ARR:
                return "Array"
            case TokenType.SENPAI:
                return "String"
            case TokenType.SENPAI_ARR:
                return "Array"
            case _:
                raise ValueError(f"Unknown token: {self}")

    def header(self):
        return self.token

    def __format__(self, format_spec):
        return str.__format__(str(self), format_spec)

    def is_arr_type(self):
        match self:
            case (TokenType.CHAN_ARR
                | TokenType.KUN_ARR
                | TokenType.SAMA_ARR
                | TokenType.SAN_ARR
                | TokenType.SENPAI_ARR
            ): return True
            case _: return False

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

    def is_unique_type(self):
        return False
    def exists(self) -> bool:
        return self != TokenType.EOF
    def is_arrayable(self):
        match self:
            case (TokenType.CHAN
                | TokenType.KUN
                | TokenType.SAMA
                | TokenType.SAN
                | TokenType.SENPAI
                | TokenType.CHAN_ARR
                | TokenType.KUN_ARR
                | TokenType.SAMA_ARR
                | TokenType.SAN_ARR
                | TokenType.SENPAI_ARR
            ): return True
            case _: return False

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

    # for `append()` type checking
    ARRAY_ELEMENT = ("elem", "all")
    # for `extend()` type checking
    GEN_ARRAY = ("gen_arr", "all")
    # for `pow()` type checking
    NUMBER = ("num", "all")

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

    def __init__(self, lexeme: str = '', token: str = 'ID'):
        self._token = lexeme
        if token == self.ID:
            self._type = self.identifier_dict.setdefault(lexeme, f"IDENTIFIER_{len(self.identifier_dict) + 1}")
            self._delim_id = "id"
        elif token == self.CWASS:
            self._type = self.cwass_dict.setdefault(lexeme, f"CWASS_{len(self.cwass_dict) + 1}")
            self._delim_id = "cwass"
        self._expected_delims = DELIMS[self._delim_id]

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
    def python_string(self, indent = 1, cwass=False):
        return self.__str__()

    def header(self):
        return self.__str__()
    def __repr__(self):
        return self.token

    def to_arr_type(self):
        tmp = deepcopy(self)
        tmp._token += "[]" if not tmp._token.endswith("[]") else ""
        return tmp
    def to_unit_type(self):
        tmp = deepcopy(self)
        tmp._token = tmp._token.replace("[]", "")
        return tmp
    def is_arr_type(self):
        return self.token.find("[") != -1
    def is_unique_type(self):
        return True
    def exists(self) -> bool:
        return True
    def is_arrayable(self):
        return True

# for keeping track of class properties
class_properties: set[str] = set()
class Token:
    'A class for representing tokens in a lexer'

    def __init__(self, lexeme: str = "", token: TokenType | UniqueTokenType = TokenType.EOF, position: tuple[int, int] = (0, 0), end_position: tuple[int, int] = (0, 0)):
        self._lexeme = lexeme
        self._token = token
        self._position = position
        self._end_position = end_position

    def __repr__(self):
        return self._lexeme
    def __str__(self):
        return self._lexeme
    def __eq__(self, other) -> bool:
        if not isinstance(other, Token): return False
        return self._lexeme == other._lexeme


    ### For Production interface
    def string(self, indent = 1) -> str:
        return self._lexeme
    def flat_string(self) -> str:
        return self._lexeme
    def python_string(self, indent = 1, cwass=False) -> str:
        match self.token:
            # for possibly class members
            case UniqueTokenType():
                global class_properties
                res = ""
                if self.token.is_arr_type(): return "Array"
                if cwass and f"_{self.lexeme}" in class_properties:
                    res = "self."
                res += f"_{self.lexeme}"
                return res
            # no python equivalent
            case (TokenType.GWOBAW
                | TokenType.DONO
                | TokenType.DOUBLE_OPEN_BRACKET
                | TokenType.DOUBLE_CLOSE_BRACKET
                | TokenType.TERMINATOR
            ):
                return ""
            # transpile literally
            case (TokenType.ASSIGNMENT_OPERATOR
                | TokenType.ADDITION_SIGN
                | TokenType.DASH
                | TokenType.MULTIPLICATION_SIGN
                | TokenType.DIVISION_SIGN
                | TokenType.MODULO_SIGN
                | TokenType.GREATER_THAN_SIGN
                | TokenType.LESS_THAN_SIGN
                | TokenType.GREATER_THAN_OR_EQUAL_SIGN
                | TokenType.LESS_THAN_OR_EQUAL_SIGN
                | TokenType.EQUALITY_OPERATOR
                | TokenType.INEQUALITY_OPERATOR
                | TokenType.OPEN_PAREN
                | TokenType.CLOSE_PAREN
                | TokenType.OPEN_BRACKET
                | TokenType.CLOSE_BRACKET
                | TokenType.COMMA
                | TokenType.DOT_OP
            ):
                return self.lexeme
            case TokenType.INT_LITERAL:
                return f"Int({self.lexeme})"
            case TokenType.FLOAT_LITERAL:
                return f"Float({self.lexeme})"
            case TokenType.STRING_LITERAL:
                return f"String({self.lexeme})"
            case TokenType.MAINUWU:
                return "main"
            case TokenType.FWUNC:
                return "def"
            case TokenType.CWASS:
                return "class"
            case TokenType.INPWT:
                return "input"
            case TokenType.PWINT:
                return "print"
            case TokenType.WETUWN:
                return "return"
            case TokenType.FOW:
                return "for"
            case TokenType.WHIWE | TokenType.DO_WHIWE:
                return "while"
            case TokenType.IWF:
                return "if"
            case TokenType.EWSE:
                return "else"
            case TokenType.EWSE_IWF:
                return "elif"
            case TokenType.BWEAK:
                return "break"
            case TokenType.CHAN:
                return "Int"
            case TokenType.KUN:
                return "Float"
            case TokenType.SAMA:
                return "Bool"
            case TokenType.SAN:
                return "NoneType"
            case TokenType.SENPAI:
                return "String"
            case (TokenType.CHAN_ARR
                | TokenType.KUN_ARR
                | TokenType.SAMA_ARR
                | TokenType.SAN_ARR
                | TokenType.SENPAI_ARR
            ):
                return "Array"
            case TokenType.NUWW:
                return "None"
            case TokenType.STRING_PART_START:
                return f'String(f{self.lexeme[:-1]}{{'
            case TokenType.STRING_PART_MID:
                return f'}}{self.lexeme[1:-1]}{{'
            case TokenType.STRING_PART_END:
                return f'}}{self.lexeme[1:]})'
            case TokenType.FAX:
                return "Bool(True)"
            case TokenType.CAP:
                return "Bool(False)"
            case TokenType.AND_OPERATOR:
                return "and"
            case TokenType.OR_OPERATOR:
                return "or"
            case TokenType.INCREMENT_OPERATOR:
                return "+1"
            case TokenType.DECREMENT_OPERATOR:
                return "-1"
            case TokenType.CONCATENATION_OPERATOR:
                return "+"
            case TokenType.OPEN_BRACE:
                return "["
            case TokenType.CLOSE_BRACE:
                return "]"
            case _:
                return self.lexeme

    def formatted_string(self, indent=0) -> str:
        return self.lexeme

    def header(self):
        return self._lexeme

    def to_arr(self, dimension: int = 1):
        'modifies the underlying token'
        pattern = r".+\[[\d]*\]"  # Matches strings that have [] or [x] in the end
        matched = re.search(pattern, self._lexeme)
        dimension = max(1, dimension)  # Defaults to 1 for dims < 1
        self._lexeme += f"[{dimension}]" if not matched else ""
        self._token = self.token.to_arr_type() if not matched else self.token

    def is_arr_type(self):
        return self.token.is_arr_type()
    def dimension(self):
        matched = self.lexeme.split("[")
        matched = matched[1].split("]") if len(matched) > 1 else []
        return int(matched[0] if matched[0] else 1) if len(matched) > 1 else 0

    def to_unit_type(self, times = 1) -> "Token":
        'returns a copy'
        if not self.is_arrayable(): return self
        ret = deepcopy(self)
        matched = ret.lexeme.split("[")
        matched = matched[1].split("]") if len(matched) > 1 else []
        dimension = int(matched[0] if matched[0] else 1) if len(matched) > 1 else 0
        for _ in range(times):
            if dimension == 0: return ret
            if dimension == 1:
                ret._lexeme = re.sub(r"\[\d*\]", "", ret._lexeme)
                ret._token = ret._token.to_unit_type()
            else:
                dimension -= 1
                ret._lexeme = re.sub(r"\[\d*\]", f"[{dimension}]", ret._lexeme)
        return ret
    
    def to_arr_type(self, times = 1) -> "Token":
        'returns a copy'
        if not self.is_arrayable(): return self
        ret = deepcopy(self)
        matched = ret.lexeme.split("[")
        matched = matched[1].split("]") if len(matched) > 1 else []
        dimension = int(matched[0] if matched[0] else 1) if len(matched) > 1 else 0
        for _ in range(times):
            if dimension == 0:
                ret._lexeme += "[1]"
                ret._token = ret._token.to_arr_type()
            else:
                dimension += 1
                ret._lexeme = re.sub(r"\[\d*\]", f"[{dimension}]", ret._lexeme)
        return ret

    def is_unique_type(self):
        return self.token.is_unique_type()
    def exists(self) -> bool:
        return self.token.exists()
    def is_arrayable(self) -> bool:
        return self.token.is_arrayable()
    def type_is(self, token_type: TokenType|UniqueTokenType) -> bool:
        return self.token == token_type

    @property
    def lexeme(self) -> str:
        return self._lexeme

    @lexeme.setter
    def lexeme(self, lexeme: str):
        self._lexeme = lexeme

    @property
    def token(self) -> TokenType | UniqueTokenType:
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

    @staticmethod
    def arr_type(token_type: TokenType|UniqueTokenType, dimension: int = 1) -> "Token":
        dimension = max(1, dimension)
        if (not isinstance(token_type, TokenType)
            and not isinstance(token_type, UniqueTokenType))\
            or not token_type.is_arrayable():
            return Token()


        if dimension == 1:
            return (Token(lexeme=re.sub(r"\[\d*\]", "[1]", token_type.token), token=token_type)
                if token_type.is_arr_type()
                else Token(lexeme=f"{token_type.token}[1]", token=token_type.to_arr_type())
            )
        else:
            return (Token(lexeme=f"{token_type.token}[{dimension}]", token=token_type.to_arr_type())
                if not token_type.is_arr_type()
                else Token(lexeme=re.sub(r"\d+", f"{dimension}", token_type.token), token=token_type)
            )
    @staticmethod
    def from_type(token_type: TokenType | UniqueTokenType) -> "Token":
        return Token(lexeme=token_type.token, token=token_type)
