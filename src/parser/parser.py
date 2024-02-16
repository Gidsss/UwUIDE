from typing import Callable
from enum import Enum

from src.lexer.token import Token, TokenType, UniqueTokenType
from src.parser.productions import *

class Precedence(Enum):
    '''
    To keep track of the precedence of each token.

    idents:                 LOWEST
    ==, !=, <, >, <=, >=:   EQUALS
    +, -:                   SUM
    *, /, %:                PRODUCT
    - (as in negative):     PREFIX
    ident():                FN_CALL
    '''
    LOWEST = 0
    EQUALS = 1
    LESS_GREATER = 2
    SUM = 3
    PRODUCT = 4
    PREFIX = 5
    FN_CALL = 6

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = [token for token in tokens if token.token != TokenType.WHITESPACE]
        self.tokens.append(Token("", TokenType.EOF, (0, 0), (0, 0)))
        self.errors: list = []

        # to keep track of tokens
        self.pos = 0
        self.curr_tok = self.tokens[self.pos]
        self.peek_tok = self.tokens[self.pos + 1]

        # to associate prefix and infix parsing functions for certain token types
        # key : val == TokenType : ParsingFunction
        self.prefix_parse_fns: dict = {}
        self.infix_parse_fns: dict = {}
        self.register_init()

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

    def register_init(self):
        '''
        Put here the functions for parsing prefix and infix expressions for
        certain token types
        '''
        # prefixes
        self.register_prefix("IDENTIFIER", self.parse_identifier)
        self.register_prefix(TokenType.INT_LITERAL, self.parse_int_lit)
        self.register_prefix(TokenType.DASH, self.parse_prefix_expression)

        # infixes

    def parse_program(self) -> Program:
        '''
        parse the entire program
        '''
        p = Program()
        while self.curr_tok.token != TokenType.EOF:
            statement = self.parse_global_statement()
            if statement:
                p.statements.append(statement)
            self.advance()
        return p

    def parse_global_statement(self):
        '''
        parse global function/class/variable/constant declarations
        '''
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
        '''
        parse declarations of variables/constants, whether global or local

        eg.
        `aqua-chan = 5~`
        `shion-chan~`
        `ojou-chan-dono = 5~`
        `lap-chan = another_ident~`
        '''
        d = Declaration()

        if not self.expect_peek_as_identifier():
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
            self.advance()
            d.value = self.parse_expression_statement()
            return d

        # variable declaration without value
        if self.expect_peek(TokenType.TERMINATOR):
            return d

        # variable declaration with value
        if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
            return None
        self.advance()
        d.value = self.parse_expression_statement()

        return d

    def parse_expression_statement(self):
        '''
        parse an expression statement
        Expressions can be:
        - literal
        - prefix expression
        - infix expression
        '''
        es = ExpressionStatement()
        tmp = self.parse_expression(Precedence.LOWEST)
        es.expression = tmp
        if self.peek_tok_is(TokenType.TERMINATOR):
            self.advance()
        return es

    def parse_expression(self, precedence: Precedence):
        '''
        parse expressions.
        Expressions can be:
        - literal
        - prefix expression
        - infix expression
        '''
        if isinstance(self.curr_tok.token, UniqueTokenType):
            prefix = self.prefix_parse_fns["IDENTIFIER"]
        else:
            prefix = self.prefix_parse_fns[self.curr_tok.token]

        if prefix is None:
            self.no_prefix_parse_fn_error(self.curr_tok.token)
            return None
        left_exp = prefix()
        return left_exp

    def parse_identifier(self):
        'returns the current token'
        return self.curr_tok
    def parse_int_lit(self):
        'returns the current token'
        return self.curr_tok

    def parse_prefix_expression(self):
        '''
        parse prefix expressions.
        Only prefix expression in UwU++ that is parsed here are negative idents.
        This is because negative int/float literals are tokenized
        '''
        pe = PrefixExpression()
        pe.prefix_tok = self.curr_tok
        pe.op = self.curr_tok.token
        self.advance()
        pe.right = self.parse_expression(Precedence.PREFIX)
        return pe
        

    def parse_function(self):
        pass
    def parse_class(self):
        pass

    ### helper methods
    # registering prefix and infix functions to parse certain token types
    def register_prefix(self, token_type: str | TokenType, fn: Callable):
        self.prefix_parse_fns[token_type] = fn
    def register_infix(self, token_type: str, fn: Callable):
        self.infix_parse_fns[token_type] = fn

    # keeping track of tokens
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
    def expect_peek_as_identifier(self) -> bool:
        if self.peek_tok.token.token.startswith("IDENTIFIER"):
            self.advance()
            return True
        else:
            return False

    # error functions
    def no_prefix_parse_fn_error(self, token_type):
        self.errors.append(f"no prefix parsing function found for {token_type}")
