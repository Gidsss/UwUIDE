from .parser import *
from ..lexer import print_lex

if __name__ == "__main__":
    sc = """
    fwunc mainuwu-san() [[
        iwf (fax) [[
            sora-senpai = "tokino '| nickname |' sora"~
            a-chan = 2~
        ]]
        wetuwn(a)~
    ]]
    cwass Hololive(name-senpai, age-chan)
    [[
        aqua-chan = 3~
        shion-chan = 3~
        fwunc sum-chan(number1-chan[], number2-chan)
        [[
            sum-chan = number1 + number2~
            wetuwn(sum)~
        ]]
        ojou-chan = 3~
        fwunc sum-chan(number1-chan[], number2-chan)
        [[
            sum-chan = number1 + number2~
            wetuwn(sum)~
        ]]
        aqua = 4~
        shion = 4~
        ojou = 4~
        iwf (1 == 2) [[
            aqua = 5~
        ]] ewse iwf (3 == 4) [[
            shion = 5~
        ]] ewse [[
            ojou = 5~
        ]]
        whiwe (aqua != shion) [[
            aqua = aqua++~
        ]]
        do whiwe (aqua != ojou) [[
            ojou = ojou--~
        ]]
        fow (aqua~ shion>aqua~ shion--) [[
            pwint(ojou, aqua, shion)~
        ]]
    ]]
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
    # gwobaw aqua-chan[] = {
    #     {
    #         {
    #             (2+2)*2,
    #         }
    #     },
    #     {
    #         3+3*3,
    #         (4+4)*4,
    #     },
    #     1,
    # }~
    #     gwobaw ojou-chan = shion(1, 2, aqua(3+4*5), lap("hello |-name--| world"))~
    #     gwobaw shion-chan = 1+- (1-2) -- == 5 -3-- *-5 ~
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
    # p.program.print()
    print(p.program)
