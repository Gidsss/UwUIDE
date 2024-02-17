from .parser import *
from ..lexer import Lexer, print_lex

if __name__ == "__main__":
    sc = """
    gwobaw shion-chan = 1+1~
    gwobaw aqua-chan[] = {1+1, 2+-2, 3+3*3, 4/4-4}~
    """
    # gwobaw sora-senpai = "tokino '| -nickname |' sora"~
    # gwobaw ojou-chan-dono = -5----1~

    source: list[str] = [line if line else '\n' for line in sc.split("\n")]
    max_digit_length = len(str(len(source)))
    max_width = max(len(line) for line in source) + max_digit_length + 3

    print("-" * (max_width) )
    for i, line in enumerate(source):
        line = line if line != '\n' else ''
        print(f"{i+1:<{max_digit_length}} | {line}")
    print("-" * (max_width) )

    l = print_lex(source)

    p = Parser(l.tokens)
    for err in p.errors:
        print(err)
