from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc as parErrorSrc
from src.analyzer import MemberAnalyzer, TypeChecker
from src.analyzer.error_handler import ErrorSrc
from .compiler import Compiler

if __name__ == "__main__":
    sc = """
    fwunc mainuwu-san() [[
        num-chan = inpwt("Enter number to be squared: ")~
        times-chan = inpwt("Enter number of times to square: ")~
        iwf (num > 0) [[
            fow(i-chan = 0~ i < times~ i + 1) [[
                pwint(num)~
                num = square(num)~
            ]]
        ]] ewse [[
            pwint("Enter a positive number. '| num |' is not a positive number.")~
        ]]
    ]]
    fwunc square-chan(num-chan) [[
        wetuwn(num*num)~
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

    c = Compiler(p.program.python_string())
