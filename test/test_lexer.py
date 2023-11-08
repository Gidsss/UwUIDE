from pytest import *

from src.lexer import Lexer
from .test_cases.lexer import LexerTestCase

def compare_tokens(tc: LexerTestCase, lx: Lexer) -> str:
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
        tc = LexerTestCase.GENERAL_KEYWORDS
        lx = Lexer(tc.source_code)

        result = compare_tokens(tc, lx)
        print(result)

    def test_source_code_one_tokens(self):
        tc = LexerTestCase.SC1
        lx = Lexer(tc.source_code)

        result = compare_tokens(tc, lx)
        print(result)