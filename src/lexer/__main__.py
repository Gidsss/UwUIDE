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
        'fow',
        'gwobaw',
        'inpwt(',
        'float-kun = 10.5~',
        'mainuwu-',
        'nuww,',
        'san~',
        'sama ',
        'senpai~',
        'staart!',
        'whiwe (',
        'wetuwn('
    ]
    print_lex(source_code)