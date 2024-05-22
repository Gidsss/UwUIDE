'''
    This file contains compiler theme configurations and color schemes.
    
'''
from enum import Enum

class ThemeColors(Enum):
    def __init__(self, hexcode: str):
        self._color = hexcode

    def __str__(self):
        return self._color

    MAIN = ('#9d7cd8')
    GLOBAL = ('#7aa2f7')
    KEYWORD = ('#7dcfff')
    IDENTIFIER = ('#c0caf5')
    CWASS = ('#0db9d7')
    METHOD = ('#7aa2f7')

    CONTROL_STRUCTURE = ('#bb9af7')
    CONSTANT_TYPE = ('#ff9e64')
    TYPE = ('#2ac3de')
    COMMENT = ('#565f89')
    GROUPING = ('#c0caf5')

    NUMBER = ('#ff9e64')
    BOOL = ('#e0af68')
    STRING = ('#9ece6a')
    NUWW = ('#e0af68')

    ARITHMETIC_OPERATOR = ('#c0caf5')
    LOGICAL_OPERATOR = ('#89ddff')
    UNARY_OPERATOR = ('#89ddff')

    OTHER_SYMBOL = ('#c0caf5')
    TERMINATOR = ('#c0caf5')
    DEFAULT = ('#c0caf5')

UWU_COMPILER_THEME = {
    # main
    'mainuwu' : ThemeColors.MAIN,

    # globals and keywords
    'fwunc' : ThemeColors.GLOBAL,
    'gwobaw' : ThemeColors.GLOBAL,
    'cwass' : ThemeColors.GLOBAL,
    'inpwt' : ThemeColors.KEYWORD,
    'pwint' : ThemeColors.KEYWORD,
    'wetuwn' : ThemeColors.KEYWORD,
    
    # identifiers
    'IDENTIFIER' : ThemeColors.IDENTIFIER,
    'CWASS' : ThemeColors.CWASS,

    # types
    'chan' : ThemeColors.TYPE,
    'kun' : ThemeColors.TYPE,
    'sama' : ThemeColors.TYPE,
    'senpai' : ThemeColors.TYPE,
    'san' : ThemeColors.TYPE,
    'dono' : ThemeColors.CONSTANT_TYPE,

    # arith operators
    "=" : ThemeColors.ARITHMETIC_OPERATOR,
    "+" : ThemeColors.ARITHMETIC_OPERATOR,
    "-" : ThemeColors.ARITHMETIC_OPERATOR,
    "*" : ThemeColors.ARITHMETIC_OPERATOR,
    "/" : ThemeColors.ARITHMETIC_OPERATOR,
    "%" : ThemeColors.ARITHMETIC_OPERATOR,

    # logical, unary opt
    ">" : ThemeColors.LOGICAL_OPERATOR,
    "<" : ThemeColors.LOGICAL_OPERATOR,
    ">=" : ThemeColors.LOGICAL_OPERATOR,
    "<=" : ThemeColors.LOGICAL_OPERATOR,
    "==" : ThemeColors.LOGICAL_OPERATOR,
    "!=" : ThemeColors.LOGICAL_OPERATOR,
    "&&" : ThemeColors.LOGICAL_OPERATOR,
    "||" : ThemeColors.LOGICAL_OPERATOR,
    "++" : ThemeColors.UNARY_OPERATOR,
    "--" : ThemeColors.UNARY_OPERATOR,

    # control structure
    'fow' : ThemeColors.CONTROL_STRUCTURE,
    'whiwe' : ThemeColors.CONTROL_STRUCTURE,
    'do whiwe' : ThemeColors.CONTROL_STRUCTURE,
    'iwf' : ThemeColors.CONTROL_STRUCTURE,
    'ewse' : ThemeColors.CONTROL_STRUCTURE,
    'ewse iwf' : ThemeColors.CONTROL_STRUCTURE,
    'bweak' : ThemeColors.CONTROL_STRUCTURE,

    # grouping symbols
    "[[" : ThemeColors.GROUPING,
    "]]" : ThemeColors.GROUPING,
    "[" : ThemeColors.GROUPING,
    "]" : ThemeColors.GROUPING,
    "{" : ThemeColors.GROUPING,
    "}" : ThemeColors.GROUPING,
    "(" : ThemeColors.GROUPING,
    ")" : ThemeColors.GROUPING,

    # literals
    'INT_LITERAL' : ThemeColors.NUMBER,
    'FLOAT_LITERAL' : ThemeColors.NUMBER,
    'STRING_LITERAL' : ThemeColors.STRING,
    'STRING_PART_START' : ThemeColors.STRING,
    'STRING_PART_END' : ThemeColors.STRING,
    'fax' : ThemeColors.BOOL,
    'cap' : ThemeColors.BOOL,
    'nuww' : ThemeColors.NUWW,

    # others
    "&" : ThemeColors.OTHER_SYMBOL,
    "," : ThemeColors.OTHER_SYMBOL,
    "." : ThemeColors.OTHER_SYMBOL,

    # comments
    'COMMENT' : ThemeColors.COMMENT,
    'MULTI LINE COMMENT' : ThemeColors.COMMENT,

    # methods
    'METHOD' : ThemeColors.METHOD,

    # terminator
    "~" : ThemeColors.TERMINATOR,

    # default
    'default' : ThemeColors.DEFAULT
}