from .parser import *
from ..lexer import Lexer

if __name__ == "__main__":
    sc = """
    fwunc shion-chan() [[

    ]]

    fwunc shion-chan() [[

    ]]

    fwunc shion-chan() [[

    ]]

    """
    source: list[str] = [line if line else '\n' for line in sc.split("\n")]
    max_digit_length = len(str(len(source)))
    max_width = max(len(line) for line in source) + max_digit_length + 3

    print("-" * (max_width) )
    for i, line in enumerate(source):
        line = line if line != '\n' else ''
        print(f"{i+1:<{max_digit_length}} | {line}")
    print("-" * (max_width) )

    l = Lexer(source)
    if len(l.errors) > 0:
        print(l.print_error_logs())
        exit(1)

    p = Parser(l.tokens)
