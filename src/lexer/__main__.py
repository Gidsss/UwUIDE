# Entry point for lexer package
from .lexer import *

if __name__ == "__main__":
    # temporary test source code
    source_code = [
        # "fwunc aqua-chan()~",
        # 'fwunc aqua1chan(',
        # 'fwunc aqua2-chan',
        # 'aqua3(args)~',
        # 'aqua4-chan()~',
        # 'fwunc aqua5',

        # 'aqua6-chan = "AKUA AISHITEEE!"~',
        # '"im an unterminated string"',
        # '"unclosed string',
        # '|what am I|',
        # r'"hello |world| hello\|world"~ "hello\world|what|is this\|\|\|"~',
        # 'manji-senpai = "foo |aqua7 + shion| foo |ojou| boo"~',

        '0~',
        '0.1~',
        '0.0~',
        '0.~',
        '1~',
        '20~',
        '0300~',
        '40'
        '5.0~',
        '6.0',
        '7.~',
        '8.00~',
        '9.01~',
    ]
    print_lex(source_code)