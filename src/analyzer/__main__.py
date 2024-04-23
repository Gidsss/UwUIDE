from .type_checker import TypeChecker
from .error_handler import ErrorSrc
from .analyzer import MemberAnalyzer
from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc as parErrorSrc

if __name__ == "__main__":
    sc = """
    cwass Hololive() [[ a-san~ ]]
    fwunc mainuwu-san() [[
        a-chan[] = {nuww}~
        a = {nuww}~
        b-chan[] = {}~
        b = {}~
        c-Hololive[] = {nuww}~
        c = {nuww}~
        d-Hololive[] = {}~
        d = {}~
        z-chan~
        y-chan[] = {z}~
        sum({})~
        sum({nuww})~
    ]]
    fwunc sum-chan[](num-chan[]) [[
        wetuwn({nuww})~
    ]]
    fwunc sum2-chan[](num-chan[]) [[
        wetuwn({})~
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
    parErrorSrc.src = source
    p = Parser(l.tokens)
    if p.errors:
        for err in p.errors:
            print(err)
        exit(1)

    ErrorSrc.src = source
    ma = MemberAnalyzer(p.program)
    if ma.errors:
        for err in ma.errors:
            print(err)
        exit(1)
    assert p.program

    tc = TypeChecker(p.program)
    if tc.errors:
        for err in tc.errors:
            print(err)
        exit(1)

    print(p.program.python_string())
