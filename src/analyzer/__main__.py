from .type_checker import TypeChecker
from .error_handler import ErrorSrc
from .analyzer import MemberAnalyzer
from .class_analyzer import ClassAnalyzer
from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc as parErrorSrc

if __name__ == "__main__":
    sc = """
    gwobaw areallylongname-kun-dono = 3.14~
    cwass Hololive2(a-chan) [[
        b-chan~
        fwunc init-chan(c-chan) [[
            b = inpwt(sum[1].a() + a || b || "hello | b | world")~
            sum(a, b)~
        ]]
    ]]
    cwass Hololive(a-chan) [[
        b-chan = sum(1)~
        c-senpai = ""~
        fwunc init-chan(d-chan) [[
            j-senpai[]~
            c = j.len()~
            c = j[1].has(1,2,3)~
            e-Hololive2 = Hololive2("2")~
        ]]
    ]]
    fwunc mainuwu-san() [[
        j-senpai[]~
        wetuwn(nuww)~
    ]]
    fwunc sum-Hololive[](a-chan) [[
        wetuwn({Hololive(1)})~
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
        ca = ClassAnalyzer(cwass, ma.global_names)
        if ca.errors:
            for err in ca.errors:
                print(err)
            exit(1)

    tc = TypeChecker(p.program)
    if tc.errors:
        for err in tc.errors:
            print(err)
        exit(1)
