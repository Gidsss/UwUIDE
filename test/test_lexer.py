from pytest import *
from enum import Enum
from src.lexer import Lexer, Token, TokenType, DelimError, GenericError

class TestCase(Enum):
    """
    Guide in implementing test cases
        Creating a test case

            Simply follow this format:

            < test case name > = (< source code >, < optional expected tokens >, < optional expected errors >)

        Naming Enums

            Test cases for keywords should be grouped. Use token.py as reference

            e.g. CONTROL_STRUCTURE_KEYWORDS test case should only contain fow, whiwe, do_whiwe, iwf, ewse, ewse iwf, and bweak

            Test cases for sample programs should have the name SC< source code number >

            e.g. SC1, SC2, SC3, SC4, etc 
    """
    
    __test__ = False
    def __init__(self, source_code: list[str], expected_tokens: list[Token] = [], expected_errors: list[DelimError | GenericError] = []):
        self._source_code = source_code
        self._expected_tokens = expected_tokens
        self._expected_errors = expected_errors
    
    @property
    def source_code(self):
        return self._source_code
    
    @property
    def expected_tokens(self):
        return self._expected_tokens
    
    @property
    def expected_errors(self):
        return self._expected_errors
    
    GENERAL_KEYWORDS = (
        ['staart!', 'donee~', 'mainuwu', 'fwunc', 'cwass', 'gwobaw', 'inpwt', 'pwint', 'wetuwn'],
        [
            Token('staart!', TokenType.START, (0,0), (0,6)),
            Token('donee~', TokenType.DONE, (1,0), (1,5)),
            Token('mainuwu', TokenType.MAINUWU, (2,0), (2,6)),
            Token('fwunc', TokenType.FWUNC, (3,0), (3,4)),
            Token('cwass', TokenType.CWASS, (4,0), (4,4)),
            Token('gwobaw', TokenType.INPWT, (5,0),(5,5)),
            Token('inpwt', TokenType.PWINT, (6,0), (6,4)),
            Token('wetuwn', TokenType.WETUWN, (7,0), (7,5))
        ]
    )
    
    SC1 = (
        ['staart!','gwobaw helloworld-senpai~','mainuwu-chan()[[','pwint(helloworld)~',']]','donee~'],
        [
            Token('staart!', TokenType.START, (0,0), (0,6)),
            Token('gwobaw', TokenType.GWOBAW, (1,0), (1,5)),
            Token('helloworld', TokenType.IDENTIFIER, (1,7), (1,16)),
            Token('-', TokenType.TYPE_INDICATOR, (1,17), (1,17)),
            Token('senpai', TokenType.SENPAI, (1,18), (1,23)),
            Token('~', TokenType.TERMINATOR, (1,24), (1,24)),
            Token('mainuwu', TokenType.MAINUWU, (2,0), (2,6)),
            Token('-', TokenType.TYPE_INDICATOR, (2,7), (2,7)),
            Token('chan', TokenType.CHAN, (2,8), (2,11)),
            Token('(', TokenType.OPEN_PAREN, (2,12), (2,12)),
            Token(')', TokenType.CLOSE_PAREN, (2,13), (2,13)),
            Token('[[', TokenType.DOUBLE_OPEN_BRACKET, (2,14), (2,15)),
            Token('pwint', TokenType.PWINT, (3,0), (3,4)),
            Token('(', TokenType.OPEN_PAREN, (3,5), (3,5)),
            Token('helloworld', TokenType.IDENTIFIER, (3,6), (3,15)),
            Token(')', TokenType.CLOSE_PAREN, (3,16), (3,16)),
            Token('~', TokenType.TERMINATOR, (3,17), (3,17)),
            Token(']]', TokenType.DOUBLE_CLOSE_BRACKET, (4, 0), (4, 1)),
            Token('donee~', TokenType.DONE, (5,0), (5,5))  
        ]
    )

def compare_tokens(tc: TestCase, lx: Lexer) -> str:
    expected_tokens = tc.expected_tokens
    received_tokens = lx.tokens

    for i, v in enumerate(received_tokens):
        e_token = expected_tokens[i]

        lexeme, token = v.lexeme, v.token
        line1, start_pos = v.position
        line2, end_pos = v.end_position
        e_line1, e_start_pos = e_token.position
        e_line2, e_end_pos = e_token.end_position
        
        assert lexeme == e_token.lexeme
        assert token == e_token.token
        assert line1 == e_line1
        assert start_pos == e_start_pos
        assert line2 == e_line2
        assert end_pos == e_end_pos
    
    return "\tReceived tokens and expected tokens match"

class TestLexer:
    def test_general_keyword_tokens(self):
        tc = TestCase.GENERAL_KEYWORDS
        lx = Lexer(tc.source_code)

        result = compare_tokens(tc, lx)
        print(result)

    def test_source_code_one_tokens(self):
        tc = TestCase.SC1
        lx = Lexer(tc.source_code)

        result = compare_tokens(tc, lx)
        print(result)