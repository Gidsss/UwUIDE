from .error_handler import ErrorSrc
from .analyzer import MemberAnalyzer
from .class_analyzer import ClassAnalyzer
from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc as parErrorSrc

if __name__ == "__main__":
    sc = """
    gwobaw areallylongname-kun-dono = 3.14~
    cwass Hololive(a-chan) [[
        b-chan~
        b-chan~
        fwunc init-chan(a-chan) [[
            b = inpwt(a[1].a() + a || b || "hello | b | world")~
        ]]
        fwunc init-chan(a-chan) [[
            b = inpwt(a[1].a() + a || b || "hello | b | world")~
        ]]
    ]]
    fwunc mainuwu-san() [[
        wetuwn(1)~
    ]]
    fwunc sum-chan(a-chan) [[
        iwf (fax || cap) [[
            a = "a"&"b | b | b"~
        ]] ewse iwf (fax + cap) [[
            b-chan = 1~
            b = 1~
        ]] ewse iwf (fax - cap) [[
            b = 1~
        ]] ewse [[
            d = 1~
        ]]
        fow(i-chan[]=1~i<10~i+1) [[
            pwint(a)~
        ]]
        pwint(i)~
        a.a[1].b[b] = 1~
        wetuwn({b})~
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

    assert p.program
    for cwass in p.program.classes:
        ca = ClassAnalyzer(cwass)
        if ca.errors:
            for err in ca.errors:
                print(err)
