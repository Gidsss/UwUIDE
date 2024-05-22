'''
    Tokyo Night Theme
        bg_dark = "#1f2335",
        bg = "#24283b",
        bg_highlight = "#292e42",
        terminal_black = "#414868",
        fg = "#c0caf5",
        fg_dark = "#a9b1d6",
        fg_gutter = "#3b4261",
        dark3 = "#545c7e",
        comment = "#565f89",
        dark5 = "#737aa2",
        blue0 = "#3d59a1",
        blue = "#7aa2f7",
        cyan = "#7dcfff",
        blue1 = "#2ac3de",
        blue2 = "#0db9d7",
        blue5 = "#89ddff",
        blue6 = "#b4f9f8",
        blue7 = "#394b70",
        magenta = "#bb9af7",
        magenta2 = "#ff007c",
        purple = "#9d7cd8",
        orange = "#ff9e64",
        yellow = "#e0af68",
        green = "#9ece6a",
        green1 = "#73daca",
        green2 = "#41a6b5",
        teal = "#1abc9c",
        red = "#f7768e",
        red1 = "#db4b4b" 
'''

from .config import *

colors = {
    "MAIN": '#9d7cd8',
    "GLOBAL": '#7aa2f7',
    "KEYWORD": '#7dcfff',
    "IDENTIFIER": '#c0caf5',
    "CWASS": '#0db9d7',
    "METHOD": '#7aa2f7',
    "CONTROL_STRUCTURE": '#bb9af7',
    "CONSTANT_TYPE": '#ff9e64',
    "TYPE": '#2ac3de',
    "COMMENT": '#565f89',
    "GROUPING": '#c0caf5',
    "NUMBER": '#ff9e64',
    "BOOL": '#e0af68',
    "STRING": '#9ece6a',
    "NUWW": '#e0af68',
    "ARITHMETIC_OPERATOR": '#c0caf5',
    "LOGICAL_OPERATOR": '#89ddff',
    "UNARY_OPERATOR": '#89ddff',
    "OTHER_SYMBOL": '#c0caf5',
    "TERMINATOR": '#c0caf5',
    "DEFAULT": '#c0caf5',
}

tc = ThemeColors(colors=colors)
tokyo = ThemeConfig(theme_colors=tc)
