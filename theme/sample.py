from .config import *

colors = {
    "MAIN": '',
    "GLOBAL": '',
    "KEYWORD": '',
    "IDENTIFIER": '',
    "CWASS": '',
    "METHOD": '',
    "CONTROL_STRUCTURE": '',
    "CONSTANT_TYPE": '',
    "TYPE": '',
    "COMMENT": '',
    "GROUPING": '',
    "NUMBER": '',
    "BOOL": '',
    "STRING": '',
    "NUWW": '',
    "ARITHMETIC_OPERATOR": '',
    "LOGICAL_OPERATOR": '',
    "UNARY_OPERATOR": '',
    "OTHER_SYMBOL": '',
    "TERMINATOR": '',
    "DEFAULT": '',
}

tc = ThemeColors(colors=colors)
sample = ThemeConfig(theme_colors=tc)