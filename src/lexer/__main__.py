# Entry point for lexer package
from .lexer import *

if __name__ == "__main__":
    # temporary test source code
    source_code = [
        # 'aqua6-chan = "AKUA AISHITEEE!"~',
        # '"im an unterminated string"',
        # '"unclosed string',
        # '|what am I|',
        # r'"hello |world| hello\|world"~ "hello\world|what|is this\|\|\|"~',
        # 'manji-senpai = "foo |aqua7 + shion| foo |ojou| boo"~',

        # '00010000000000000 + 5~',
        # '1.1.1~',
        # '1.111111111111110000000~',
        # '1111111111111111.1~',
        # '0.00~',
        # '1.~',
        # '6.0',
        # '8.00~',
        # '9.01~',
        'fwunc aqua-chan() ',
        'fwunc aqua() ',
        'fwunc aqua-chan ',
        'aqua-chan() ',
        'aqua()',
        'fwunc Shion-chan() ',
        'fwunc Shion() ',
        'fwunc Shion-chan ',
        'Shion-chan() ',
        'Shion()',
        'cwass Shion-chan() ',
        'cwass Shion() ',
        'cwass Shion-chan ',
        'Shion-chan() ',
        'Shion()',
        'cwass shion-chan() ',
        'cwass shion() ',
        'cwass shion-chan ',
        'shion-chan() ',
        'shion()',
    ]
    print_lex(source_code)