from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc

if __name__ == "__main__":
    sc = """
    gwobaw pi-kun-dono = 3.14~
    gwobaw pi-kun-dono = 3.14~
    cwass Hololive() [[
        fwunc init-san() [[
            wetuwn(1)~
        ]]
    ]]
    fwunc mainuwu-san() [[
        a = 1~
        b-senpai = 10~
        c-chan = 100~
    ]]
    fwunc pi-chan() [[
        wetuwn("unimplemented")~
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
    if p.errors:
        for err in p.errors:
            print(err)
        exit(1)
