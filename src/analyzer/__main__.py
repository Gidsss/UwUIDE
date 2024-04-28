import re
from .type_checker import TypeChecker
from .error_handler import ErrorSrc
from .analyzer import MemberAnalyzer
from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc as parErrorSrc

if __name__ == "__main__":
    sc = """
    cwass Hololive() [[
        b-chan~
    ]]
    fwunc mainuwu-san() [[
        a-Hololive[] = {}~
        a.append(Hololive())~
        a.append(1)~
        a.has(Hololive())~
        a.has(1)~
        z-chan[] = {1,2,3}~
        z.append(10)~
        z.has(10)~
        z.append("")~
        z.has("")~
        x-senpai[] = {}~
        x.append(10)~
        x.has(10)~
        x.append("")~
        x.has("")~
    ]]
    """
    sc = re.sub(r"[\0\1]", "", sc)
    source: list[str] = [line if line else '\n' for line in sc.split("\n")]
    max_digit_length = len(str(len(source)))
    max_width = max(len(line) for line in source) + max_digit_length + 3
    print('\nsample text file')
    print("-"*max_width)
    for i, line in enumerate(source):
        line = line if line != '\n' else ''
        print(f"{i+1:{max_digit_length}} | {line}")
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

    print(p.errors)
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
