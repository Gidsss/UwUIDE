from constants.path import ANALYZER_SOURCE
from .type_checker import TypeChecker
from .error_handler import ErrorSrc
from .analyzer import MemberAnalyzer
from src.lexer import Lexer
from src.parser import Parser
from src.parser.error_handler import ErrorSrc as parErrorSrc

if __name__ == "__main__":
    source: list[str] = [
        line if line else "\n" for line in open(ANALYZER_SOURCE, "r").readlines()
    ]
    max_digit_length = len(str(len(source)))
    max_width = max(len(line) for line in source) + max_digit_length + 3
    print("\nsample text file")
    print("-" * max_width)
    for i, line in enumerate(source):
        line = line if line != "\n" else ""
        print(f"{i + 1:{max_digit_length}} | {line}")
    print("-" * max_width)
    print("end of file\n")

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
