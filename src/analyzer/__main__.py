from .type_checker import TypeChecker
from .error_handler import ErrorSrc
from .analyzer import MemberAnalyzer
from .class_analyzer import ClassAnalyzer
from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc as parErrorSrc

if __name__ == "__main__":
    sc = """
    >.< gwobaw areallylongname-kun-dono = 3.14~
    cwass Hololive(a-chan) [[
        b-chan~
        fwunc init-chan(c-chan) [[
            b = inpwt(a[1].a() + a || b || "hello | b | world")~
        ]]
    ]]
    fwunc mainuwu-san() [[
        a-chan[] = {"1", "2", "f|3+3|", inpwt("4"), "5", {"6", {"1"}}}~
        b-chan[] = {{{{sum()}}}, "2", "f|3+3|", inpwt("4"), "5", {"6", {"1"}}}~
        c-Hololive = sum()~
        >.< c-senpai~
        >.< d-Hololive = Hololive(-a++ + a + c > 10)~
        >.< a(-b++ + b + c > 10)~
    ]]
    fwunc sum-Hololive(a-chan) [[
        b-Hololive = Hololive("1")~
        wetuwn(b)~
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
    for cwass in p.program.classes:
        ca = ClassAnalyzer(cwass)
        if ca.errors:
            for err in ca.errors:
                print(err)
            exit(1)

    tc = TypeChecker(p.program)
    if tc.errors:
        for err in tc.errors:
            print(err)
        exit(1)
