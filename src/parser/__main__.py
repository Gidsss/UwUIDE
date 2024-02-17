from .parser import *
from ..lexer import print_lex

if __name__ == "__main__":
    sc = """
    gwobaw aqua-chan[3] = {1+1*1, (2+2)*2}~
    gwobaw shion-chan = 1+-aqua~
        gwobaw ojou-chan = -5- -1~
        gwobaw sora-senpai = "tokino '| nickname |' sora"~
    """

    source: list[str] = [line if line else '\n' for line in sc.split("\n")]
    l = print_lex(source)
    if l.errors:
        exit(1)
    p = Parser(l.tokens)
    for err in p.errors:
        print(err)
