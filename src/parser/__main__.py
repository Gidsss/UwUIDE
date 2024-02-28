from .parser import *
from ..lexer import Lexer
from .error_handler import ErrorSrc

if __name__ == "__main__":
    sc = """
    cwass Ojou()[[
        aqua-chan = 1~
        Ojou.ojou = Shion.shion[1][2]
            .aqua("hello")[3]
            .shion
            .aqua(arg1, arg2)[4][5]
            .shion(fax)
            .aqua[6][7][8][9][0]~
        shion~

        aqua-chan = (1+1*ojou(fax || shion != 5)[1]/2)~
        iwf (fax) [[
            pwint(fax)~
            whiwe (1+2 != 3) [[
                pwint(1+2)~
            ]]
        ]] ewse iwf(cap) [[
            pwint(cap)~
            do whiwe (fax && cap) [[
                pwint(fax && cap)~
            ]]
        ]] ewse[[
            pwint()~
            fow(i~i>10||i<5~i++) [[
                pwint(test)~
            ]]
        ]]
    ]]
    fwunc mainuwu-san() [[
        b()[1].a 
            .aqua("hello")[3]
            .shion
            .aqua(arg1, arg2)[4][5]
            .shion(fax)
            .aqua[6][7][8][9][0]-chan-dono = 10~
        c[2][1]~
        a-san[]~
    ]]
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
        for err in l.errors:
            print(err)
        exit(1)

    ErrorSrc.src = source
    p = Parser(l.tokens)
    print()

    print("--- Printing Whole Program ---")
    print(p.program)
    print("\n--- Printing only Main Function ---")
    print(p.program.mainuwu_string())
    print("\n--- Printing only Global Declarations ---")
    print(p.program.globals_string())
    print("\n--- Printing only Functions ---")
    print(p.program.functions_string())
    print("\n--- Printing only Classes ---")
    print(p.program.classes_string())

    if p.errors:
        for err in p.errors:
            print(err)
        exit(1)
