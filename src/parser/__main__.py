from .parser import *
from ..lexer import Lexer
from ..lexer import print_lex

if __name__ == "__main__":
    sc = """
    gwobaw wetuwn 10~
    fwunc mainuwu-san() [[
        iwf () [[
            a-san = 20~
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
