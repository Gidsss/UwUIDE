from .parser import *
from ..lexer import Lexer

if __name__ == "__main__":
#     fwunc mainuwu-san() [[
#     iwf (fax) [[
#     sora-senpai = "tokino '| nickname |' sora"~
#         a-chan = 2~
# ]]
#     wetuwn(a)~
# ]]
#     fwunc sum-san() [[
#     iwf (fax) [[
#         sora-senpai = "tokino '| nickname |' sora"~
#             a-chan = 2~
#     ]]
#     wetuwn(a)~
# ]]
# cwass Hololive(name-senpai, age-chan)
# [[
#     aqua-chan = 3~
#         shion-chan = 3~
#         fwunc sum-chan(number1-chan[], number2-chan)
#             [[
#                 sum-chan = number1 + number2~
#                     wetuwn(sum)~
#             ]]
#         ojou-chan = 3~
#         aqua = 4~
#         shion = 4~
#         ojou = 4~
#         iwf (1 == 2) [[
#             aqua = 5~
#         ]] ewse iwf (3 == 4) [[
#             shion = 5~
#         ]] ewse [[
#             ojou = 5~
#         ]]
# ]]
    sc = """
    gwobaw aqua-chan[] = { {
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
    gwobaw ojou-chan = shion(1, 2, aqua(3+4*5), lap("hello |-name--| world"))~
    gwobaw shion-chan = 1+- (1-2) -- == 5 -3-- *-5 ~
    gwobaw lap-chan[]-dono = {1,2,3,4,5,6,7,8,9,10}~
    gwobaw suba-chan[] = {2+2, (3+3)*3}~
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
    p = Parser(l.tokens)
    for err in p.errors:
        print(err)

    print("--- Printing Whole Program ---")
    print(p.program)
    print("\n--- Printing only Main Function ---")
    print(p.program.main())
    print("\n--- Printing only Global Declarations ---")
    print(p.program.globs())
    print("\n--- Printing only Functions ---")
    print(p.program.funcs())
    print("\n--- Printing only Classes ---")
    print(p.program._classes())
