from enum import Enum

class ThemeColors():
    def __init__(self, colors: dict[str, str]):
        self.colors = colors
        self._assign_colors()

    def _assign_colors(self):
        for key, value in self.colors.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.colors)

    MAIN = "MAIN"
    GLOBAL = "GLOBAL"
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    CWASS = "CWASS"
    METHOD = "METHOD"
    CONTROL_STRUCTURE = "CONTROL_STRUCTURE"
    CONSTANT_TYPE = "CONSTANT_TYPE"
    TYPE = "TYPE"
    COMMENT = "COMMENT"
    GROUPING = "GROUPING"
    NUMBER = "NUMBER"
    BOOL = "BOOL"
    STRING = "STRING"
    NUWW = "NUWW"
    ARITHMETIC_OPERATOR = "ARITHMETIC_OPERATOR"
    LOGICAL_OPERATOR = "LOGICAL_OPERATOR"
    UNARY_OPERATOR = "UNARY_OPERATOR"
    OTHER_SYMBOL = "OTHER_SYMBOL"
    TERMINATOR = "TERMINATOR"
    DEFAULT = "DEFAULT"

class ThemeConfig():
    def __init__(self, theme_colors: ThemeColors):
        self.theme_colors = theme_colors
        
    @property
    def config(self) -> dict[str, ThemeColors]:
        return {
        # main
        'mainuwu' : self.theme_colors.MAIN,

        # globals and keywords
        'fwunc' : self.theme_colors.GLOBAL,
        'gwobaw' : self.theme_colors.GLOBAL,
        'cwass' : self.theme_colors.GLOBAL,
        'inpwt' : self.theme_colors.KEYWORD,
        'pwint' : self.theme_colors.KEYWORD,
        'wetuwn' : self.theme_colors.KEYWORD,
        
        # identifiers
        'IDENTIFIER' : self.theme_colors.IDENTIFIER,
        'CWASS' : self.theme_colors.CWASS,

        # types
        'chan' : self.theme_colors.TYPE,
        'kun' : self.theme_colors.TYPE,
        'sama' : self.theme_colors.TYPE,
        'senpai' : self.theme_colors.TYPE,
        'san' : self.theme_colors.TYPE,
        'dono' : self.theme_colors.CONSTANT_TYPE,

        # arith operators
        "=" : self.theme_colors.ARITHMETIC_OPERATOR,
        "+" : self.theme_colors.ARITHMETIC_OPERATOR,
        "-" : self.theme_colors.ARITHMETIC_OPERATOR,
        "*" : self.theme_colors.ARITHMETIC_OPERATOR,
        "/" : self.theme_colors.ARITHMETIC_OPERATOR,
        "%" : self.theme_colors.ARITHMETIC_OPERATOR,

        # logical, unary opt
        ">" : self.theme_colors.LOGICAL_OPERATOR,
        "<" : self.theme_colors.LOGICAL_OPERATOR,
        ">=" : self.theme_colors.LOGICAL_OPERATOR,
        "<=" : self.theme_colors.LOGICAL_OPERATOR,
        "==" : self.theme_colors.LOGICAL_OPERATOR,
        "!=" : self.theme_colors.LOGICAL_OPERATOR,
        "&&" : self.theme_colors.LOGICAL_OPERATOR,
        "||" : self.theme_colors.LOGICAL_OPERATOR,
        "++" : self.theme_colors.UNARY_OPERATOR,
        "--" : self.theme_colors.UNARY_OPERATOR,

        # control structure
        'fow' : self.theme_colors.CONTROL_STRUCTURE,
        'whiwe' : self.theme_colors.CONTROL_STRUCTURE,
        'do whiwe' : self.theme_colors.CONTROL_STRUCTURE,
        'iwf' : self.theme_colors.CONTROL_STRUCTURE,
        'ewse' : self.theme_colors.CONTROL_STRUCTURE,
        'ewse iwf' : self.theme_colors.CONTROL_STRUCTURE,
        'bweak' : self.theme_colors.CONTROL_STRUCTURE,

        # grouping symbols
        "[[" : self.theme_colors.GROUPING,
        "]]" : self.theme_colors.GROUPING,
        "[" : self.theme_colors.GROUPING,
        "]" : self.theme_colors.GROUPING,
        "{" : self.theme_colors.GROUPING,
        "}" : self.theme_colors.GROUPING,
        "(" : self.theme_colors.GROUPING,
        ")" : self.theme_colors.GROUPING,

        # literals
        'INT_LITERAL' : self.theme_colors.NUMBER,
        'FLOAT_LITERAL' : self.theme_colors.NUMBER,
        'STRING_LITERAL' : self.theme_colors.STRING,
        'STRING_PART_START' : self.theme_colors.STRING,
        'STRING_PART_MID' : self.theme_colors.STRING,
        'STRING_PART_END' : self.theme_colors.STRING,
        'fax' : self.theme_colors.BOOL,
        'cap' : self.theme_colors.BOOL,
        'nuww' : self.theme_colors.NUWW,

        # others
        "&" : self.theme_colors.OTHER_SYMBOL,
        "," : self.theme_colors.OTHER_SYMBOL,
        "." : self.theme_colors.OTHER_SYMBOL,

        # comments
        'COMMENT' : self.theme_colors.COMMENT,
        'MULTI LINE COMMENT' : self.theme_colors.COMMENT,

        # methods
        'METHOD' : self.theme_colors.METHOD,

        # terminator
        "~" : self.theme_colors.TERMINATOR,

        # default
        'default' : self.theme_colors.DEFAULT
    }
