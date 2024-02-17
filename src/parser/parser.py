'''
OVERVIEW: 

Headers are prepended by '###' so just search for that

1. Statements: can be declarations, expressions, or block statements

2. Declarations are simply global/local function/class/variable/constant declarations
    - on a global scope, only declarations are allowed

3. Expressions can be:
    - literal int, string, float, bool
    - function call
    - return statements
    - prefix expression (int, string, float, bool)
        - negative idents
    - infix expression (int, string, float, bool)
        - math operations
        - comparisons
        - equality checks

4. block statements are statements with bodies:
    - if statements
    - while and do while statements
    - for statements
'''

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

        self.program = self.parse_program()
        print(self.program)

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
        self.register_prefix(TokenType.OPEN_BRACE, self.parse_array)
        self.register_prefix(TokenType.STRING_LITERAL, self.parse_string_lit)
        self.register_prefix(TokenType.STRING_PART_START, self.parse_string_parts)

        # infixes

    def parse_program(self) -> Program:
        '''
        parse the entire program
        '''
        p = Program()
        while not self.curr_tok_is(TokenType.EOF):
            match self.curr_tok.token:
                case TokenType.FWUNC:
                    p.functions.append(self.parse_function())
                case TokenType.CWASS:
                    p.classes.append(self.parse_class())
                case TokenType.GWOBAW:
                    p.globals.append(self.parse_declaration())
                case _:
                    self.errors.append(f"Expected global function/class/variable/constant declaration, got {self.curr_tok.lexeme}")
                    self.advance()
        return p

    def parse_declaration(self):
        '''
        parse declarations of variables/constants, whether global or local.
        if encountered brackets, the parsed declaration is an array declaration.

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

            # constant variable
            if self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
                self.advance()
                d.value = self.parse_expression(Precedence.LOWEST)
                if not self.expect_peek(TokenType.TERMINATOR):
                    return None
                self.advance()
                return d

            # constant array declaration
            elif self.expect_peek(TokenType.OPEN_BRACKET):
                ad = ArrayDeclaration()
                ad.id, ad.dtype, ad.value, ad.is_const = d.id, d.dtype, d.value, d.is_const
                if self.expect_peek(TokenType.INT_LITERAL) or self.expect_peek_as_identifier():
                    ad.size = self.curr_tok
                if not self.expect_peek(TokenType.CLOSE_BRACKET):
                    return None
                if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
                    return None
                self.advance()
                ad.value = self.parse_expression(Precedence.LOWEST)
                ad.length = len(ad.value.elements)
                if not self.expect_peek(TokenType.TERMINATOR):
                    return None
                self.advance()
                return ad
            else:
                return None

        # variable declaration without value
        if self.expect_peek(TokenType.TERMINATOR):
            return d

        # variable array declaration
        if self.expect_peek(TokenType.OPEN_BRACKET):
            ad = ArrayDeclaration()
            ad.id, ad.dtype, ad.value, ad.is_const = d.id, d.dtype, d.value, d.is_const
            if self.expect_peek(TokenType.INT_LITERAL) or self.expect_peek_as_identifier():
                ad.size = self.curr_tok
            if not self.expect_peek(TokenType.CLOSE_BRACKET):
                return None
            if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
                return None
            self.advance()
            ad.value = self.parse_expression(Precedence.LOWEST)
            if ad.value:
                ad.length = len(ad.value.elements)
            if not self.expect_peek(TokenType.TERMINATOR):
                return None
            self.advance()
            return ad

        # variable declaration with value
        elif not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
            return None
        self.advance()
        d.value = self.parse_expression(Precedence.LOWEST)
        if not self.expect_peek(TokenType.TERMINATOR):
            return None
        self.advance()
        return d

    def parse_expression(self, precedence: Precedence):
        '''
        parse expressions.
        Expressions can be:
            - literal int, string, float, bool
            - function call
            - return statements
            - prefix expression (int, string, float, bool)
                - negative idents
            - infix expression (int, string, float, bool)
                - math operations
                - comparisons
                - equality checks
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

    ### block statement parsers
    def parse_function(self):
        pass
    def parse_class(self):
        pass
    def parse_if_statement(self):
        pass
    def parse_while_statement(self):
        'this includes do while block statements'
        pass
    def parse_for_statement(self):
        pass

    ### atomic parsers
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
    def parse_array(self):
        al = ArrayLiteral()
        self.advance() # consume the opening brace
        while not self.curr_tok_is_in([TokenType.CLOSE_BRACE, TokenType.TERMINATOR, TokenType.EOF]):
            al.elements.append(self.parse_expression(Precedence.LOWEST))
            if not self.expect_peek(TokenType.COMMA):
                break
            self.advance()

        if not self.expect_peek(TokenType.CLOSE_BRACE):
            return None
        return al
    def parse_string_parts(self):
        sf = StringFmt()
        sf.start = self.curr_tok

        # append middle parts if any
        while not self.expect_peek(TokenType.STRING_PART_END):
            # no expression after string_mid
            if self.peek_tok_is(TokenType.STRING_PART_MID):
                sf.exprs.append(Token("", TokenType.STRING_LITERAL, (0, 0), (0, 0)))
                self.advance()
            # expressions
            else:
                self.advance()
                sf.exprs.append(self.parse_expression(Precedence.LOWEST))

            if self.expect_peek(TokenType.STRING_PART_MID):
                sf.mid.append(self.curr_tok)

        sf.end = self.curr_tok
        return sf


    def parse_string_lit(self):
        'returns the current token'
        return self.curr_tok
    def parse_float_lit(self):
        'returns the current token'
        return self.curr_tok
    def parse_identifier(self):
        'returns the current token'
        return self.curr_tok
    def parse_int_lit(self):
        'returns the current token'
        return self.curr_tok

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
    def curr_tok_is_in(self, token_types: list[TokenType]) -> bool:
        return self.curr_tok.token in token_types
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

    ### error methods
    def no_prefix_parse_fn_error(self, token_type):
        self.errors.append(f"no prefix parsing function found for {token_type}")
