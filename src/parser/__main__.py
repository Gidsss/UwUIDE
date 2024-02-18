from .parser import *
from ..lexer import print_lex

if __name__ == "__main__":
    sc = """
    >.< shape of this should be [3, 2, 1]
    >.< 2 elements on aqua
    >.< 2 elements in aqua[1]
    >.< 2 elements in aqua[0][0]
    gwobaw aqua-chan[2][-shion] = {
        {
            {
                (2+2)*2,
            }
        }, 
        {
            3+3*3,
            (4+4)*4,
        },
        1,
    }~
    """
    # gwobaw shion-chan = 1+-aqua~
    # gwobaw ojou-chan = -5- -1~
    # gwobaw sora-senpai = "tokino '| -nickname |' sora"~
    # gwobaw lap-chan[5]-dono = {1,2,3,4,5,6,7,8,9,10}~
    # gwobaw suba-chan[5] = {2+2, (3+3)*3}~

    source: list[str] = [line if line else '\n' for line in sc.split("\n")]
    l = print_lex(source)
    if l.errors:
        exit(1)
    p = Parser(l.tokens)
    for err in p.errors:
        print(err)
