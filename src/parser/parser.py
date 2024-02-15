from src.lexer.token import Token, TokenType
from src.parser.productions import *

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = [token for token in tokens if token.token != TokenType.WHITESPACE]
        self.tokens.append(Token("", TokenType.EOF, (0, 0), (0, 0)))


        self.pos = 0
        self.curr_tok = self.tokens[self.pos]
        self.peek_tok = self.tokens[self.pos + 1]

        program = self.parse_program()
        program.print()

    def advance(self):
        if self.curr_tok.token == TokenType.EOF:
            return

        if self.peek_tok.token == TokenType.EOF:
            self.curr_tok = self.peek_tok
            self.pos += 1
            return

        self.pos += 1
        self.curr_tok = self.peek_tok
        self.peek_tok = self.tokens[self.pos + 1]

    def parse_program(self) -> Program:
        p = Program()

        while self.curr_tok.token != TokenType.EOF:
            p.statements.append(self.curr_tok)
            self.advance()

        return p
