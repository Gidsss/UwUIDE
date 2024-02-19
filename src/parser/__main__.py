from .parser import *
from ..lexer import print_lex

if __name__ == "__main__":
    sc = """
    pwint(1, 1.5, -2----3, 4+4*4, "test", "test| 0 |ing", fax, cap != 3>5)~
    inpwt({})~
    """
#     ewse iwf (4 == 5) [[
#         aqua-sama = 6~
#             shion-sama = 6~
#             ojou-sama = 6~
#     ]] ewse iwf (7 == 8) [[
#             aqua-sama = 9~
#                 shion-sama = 9~
#                 ojou-sama = 9~
#         ]] ewse iwf (10 == 11) [[
#         aqua-sama = 12~
#             shion-sama = 12~
#             ojou-sama = 12~
#     ]] ewse [[
#     iwf (1 == 2) [[
#         sora-senpai = "nested!"~
#     ]] ewse [[
#             sora-senpai = "if statements!"~
#         ]]
# ]]
    # >//<
    # shape of this should be [3, 2, 1]
    # 3 elements on aqua
    # 2 elements in aqua[1]
    # 1 elements in aqua[0][0]
    # >//<
    #     gwobaw ojou-chan = shion(1, 2, aqua(3+4*5), lap("hello |-name--| world"))~
    #     gwobaw shion-chan = 1+- (1-2) -- == 5 -3-- *-5 ~
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
    if p.errors:
        exit(1)
    p.program.print()
