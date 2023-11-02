# Entry point for lexer package
from .lexer import *

if __name__ == "__main__":
    # temporary test source code
    source_code = [
        "a  fwunc aqua-chan()~",
        'fwunc aqua2chan(',
        'fwunc aqua3-chan',
        'aqua4(args)~',
        ' aqua5-chan()~',
        'aqua6',
        'aqua7-chan = cap~',
        'bweak~ bweak',
    ]
    print_lex(source_code)