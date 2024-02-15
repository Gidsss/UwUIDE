from src.lexer.token import Token, TokenType
from src.parser.productions import *

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = [token for token in tokens if token.token != TokenType.WHITESPACE]
        self.tokens.append(Token("", TokenType.EOF, (0, 0), (0, 0)))
        self.errors: list = []


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
            statement = self.parse_statement()
            if statement:
                p.statements.append(statement)
            self.advance()
        return p

    def parse_statement(self):
        while not self.curr_tok_is(TokenType.EOF):
            match self.curr_tok.token:
                case TokenType.FWUNC:
                    return self.parse_function()
                case TokenType.CWASS:
                    return self.parse_class()
                case TokenType.GWOBAW:
                    return self.parse_declaration()
                case _:
                    self.errors.append(f"Expected global function/class/variable/constant declaration, got {self.curr_tok.lexeme}")
                    self.advance()
    
    def parse_declaration(self):
        d = Declaration()

        if not self.expect_peek_identifier():
            return None
        d.id = self.curr_tok

        if not self.expect_peek(TokenType.DASH):
            return None
        data_types = [
            TokenType.CHAN,
            TokenType.KUN,
            TokenType.SAMA,
            TokenType.SENPAI,
            TokenType.SAN
        ]
        if not self.expect_peek_in(data_types):
            return None
        d.dtype = self.curr_tok

        # -dono if constant
        if self.expect_peek(TokenType.DASH):
            if not self.expect_peek(TokenType.DONO):
                return None
            d.is_const = True

            if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
                return None
            # TODO: parse expressions
            self.advance()
            d.value = self.curr_tok
            return d

        # variable declaration without value
        if self.expect_peek(TokenType.TERMINATOR):
            return d

        # variable declaration with value
        if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
            return None
        # TODO: parse expressions
        self.advance()
        d.value = self.curr_tok

        return d


    def parse_function(self):
        pass
    def parse_class(self):
        pass

    # helper methods
    def curr_tok_is(self, token_type: TokenType) -> bool:
        return self.curr_tok.token == token_type
    def peek_tok_is(self, token_type: TokenType) -> bool:
        return self.peek_tok.token == token_type
    def expect_peek(self, token_type: TokenType) -> bool:
        if self.peek_tok_is(token_type):
            self.advance()
            return True
        else:
            return False
    def peek_tok_is_in(self, token_types: list[TokenType]) -> bool:
        return self.peek_tok.token in token_types
    def expect_peek_in(self, token_types: list[TokenType]) -> bool:
        if self.peek_tok_is_in(token_types):
            self.advance()
            return True
        else:
            return False
    def expect_peek_identifier(self) -> bool:
        if self.peek_tok.token.token.startswith("IDENTIFIER"):
            self.advance()
            return True
        else:
            return False

