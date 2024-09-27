# Entry point for lexer package
from constants.path import LEXER_SOURCE
from .lexer import *

if __name__ == "__main__":
    source: list[str] = [
        line if line else "\n" for line in open(LEXER_SOURCE, "r").readlines()
    ]
    input(source)
    print_lex(source)
