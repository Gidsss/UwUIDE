from .parser import *
from ..lexer import Lexer

if __name__ == "__main__":
    sc = """
    fwunc aqua-chan() [[
    ]]
    """
    source: list[str] = [line if line else '\n' for line in sc.split("\n")]
    l = Lexer(source)
    if len(l.errors) > 0:
        print(l.print_error_logs())
        exit(1)

    p = Parser(l.tokens)
