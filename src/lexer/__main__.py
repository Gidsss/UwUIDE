# Entry point for lexer package
from .lexer import *

if __name__ == "__main__":
    # temporary test source code
    source_code = [
        'bweak~',
        ' aqua-chan',
        'cwass ',
        'aqua-chan = cap~',
        'cwass~ bweak',
        'dono ',
        'do whiwe(',
        'donee~',
        'ewse iwf(',
        'ewse(',
        'iwf(',
        'minato-chan~ojou~',
        'pwint (',
        'fwunc',
        'fax,',
        

    ]
    print_lex(source_code)