from .parser import *
from ..lexer import Lexer
from ..lexer import print_lex
from .error_handler import ErrorSrc

if __name__ == "__main__":
    sc = """
    cwass Ojou()[[
        ojou = shion.aqua().shion.aqua().shion().aqua~
        aqua-chan = (1+1*ojou())
    ]]
    fwunc mainuwu-san() [[
        a-san[] = 20~
        >.< a[1] = 10~
    ]]
    """

    source: list[str] = [line if line else '\n' for line in sc.split("\n")]
    max_digit_length = len(str(len(source)))
    max_width = max(len(line) for line in source) + max_digit_length + 3
    print('\nsample text file')
    print("-"*max_width)
    for i, line in enumerate(source):
        line = line if line != '\n' else ''
        print(f"{i+1} | {line}")
    print("-"*max_width)
    print('end of file\n')

    l = Lexer(source)
    if l.errors:
        exit(1)

    ErrorSrc.src = source
    p = Parser(l.tokens)
    print()
    for err in p.errors:
        print(err)

    print("--- Printing Whole Program ---")
    print(p.program)
    print("\n--- Printing only Main Function ---")
    print(p.program.mainuwu_string())
    print("\n--- Printing only Global Declarations ---")
    print(p.program.globals_string())
    print("\n--- Printing only Functions ---")
    print(p.program.functions_string())
    print("\n--- Printing only Classes ---")
    print(p.program.classes_string())

    if p.errors:
        exit(1)
