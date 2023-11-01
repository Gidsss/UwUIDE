# Entry point for lexer package
from .lexer import *

if __name__ == "__main__":
    # temporary test source code
    source_code = [
        "a  fwunc aqua-chan()~",
        # 'aqua-chan(args)~',
        ' aqua-chan',
        'aqua',
        'aqua-chan = cap~',
        'bweak~ bweak',
        'shion-chan~ojou~'
    ]
    print_lex(source_code)