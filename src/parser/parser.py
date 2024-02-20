'''
PLEASE READ!
Headers are prepended by '###' so just search for that

Overview:
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

from src.lexer.token import Token, TokenType, UniqueTokenType
from src.parser.productions import *

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

precedence_map = {
    TokenType.EQUALITY_OPERATOR: EQUALS,
    TokenType.INEQUALITY_OPERATOR: EQUALS,
    TokenType.LESS_THAN_SIGN: LESS_GREATER,
    TokenType.LESS_THAN_OR_EQUAL_SIGN: LESS_GREATER,
    TokenType.GREATER_THAN_SIGN: LESS_GREATER,
    TokenType.GREATER_THAN_OR_EQUAL_SIGN: LESS_GREATER,
    TokenType.ADDITION_SIGN: SUM,
    TokenType.DASH: SUM,
    TokenType.MULTIPLICATION_SIGN: PRODUCT,
    TokenType.DIVISION_SIGN: PRODUCT,
    TokenType.MODULO_SIGN: PRODUCT,
}

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = [token for token in tokens if token.token not in [TokenType.WHITESPACE, TokenType.SINGLE_LINE_COMMENT, TokenType.MULTI_LINE_COMMENT]]
        self.tokens.append(Token("EOF", TokenType.EOF, (0, 0), (0, 0)))
        self.errors: list = []

        # to keep track of tokens
        self.pos = 0
        self.curr_tok = self.tokens[self.pos]
        self.peek_tok = self.tokens[self.pos + 1]

        # to associate prefix and infix parsing functions for certain token types
        # key : val == TokenType : ParsingFunction
        self.prefix_parse_fns: dict = {}
        self.infix_parse_fns: dict = {}
        self.postfix_parse_fns: dict = {}
        self.in_block_parse_fns: dict = {}
        self.register_init()

        self.program = self.parse_program()

    def advance(self, inc: int = 1):
        'advance the current and peek tokens based on the increment. default is 1'
        if inc <= 0 :
            return
        for _ in range(inc):
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
        Register token types to parsing functions here
        - prefix parsing functions are used to parse expressions that come after a
            certain token. The certain token does not necessarily need to be a prefix
            operator like '-'. It can be an opening parenthesis for grouped expressions,
            or even literals which in that case would just return the literal. All that
            matters is that the prefix parsing function returns a possible left hand
            side expression, be it a literal, array, grouped expression, etc.

        - infix parsing functions on the other hand need to be used to parse
            expressions that come after the left hand side expression using infix
            operators.

        - postfix parsing functions are used to parse tokens that can be followed by a
            postfix operator.

        - in block parsing functions are used to parse tokens inside a block statement
        '''
        # prefixes
        self.register_prefix(TokenType.DASH, self.parse_prefix_expression)
        self.register_prefix(TokenType.OPEN_BRACE, self.parse_array)
        self.register_prefix(TokenType.STRING_PART_START, self.parse_string_parts)
        self.register_prefix(TokenType.OPEN_PAREN, self.parse_grouped_expressions)
        self.register_prefix(TokenType.IWF, self.parse_if_statement)

        # literals (just returns curr_tok)
        self.register_prefix("IDENTIFIER", self.parse_ident)
        self.register_prefix(TokenType.INT_LITERAL, self.parse_literal)
        self.register_prefix(TokenType.STRING_LITERAL, self.parse_literal)
        self.register_prefix(TokenType.FLOAT_LITERAL, self.parse_literal)
        self.register_prefix(TokenType.FAX, self.parse_literal)
        self.register_prefix(TokenType.CAP, self.parse_literal)
        self.register_prefix(TokenType.NUWW, self.parse_literal)

        # infixes
        self.register_infix(TokenType.EQUALITY_OPERATOR, self.parse_infix_expression)
        self.register_infix(TokenType.INEQUALITY_OPERATOR, self.parse_infix_expression)
        self.register_infix(TokenType.LESS_THAN_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.LESS_THAN_OR_EQUAL_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.GREATER_THAN_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.GREATER_THAN_OR_EQUAL_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.ADDITION_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.DASH, self.parse_infix_expression)
        self.register_infix(TokenType.MULTIPLICATION_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.DIVISION_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.MODULO_SIGN, self.parse_infix_expression)

        # postfixes
        self.register_postfix("IDENTIFIER", self.parse_postfix_expression)
        self.register_postfix(TokenType.INT_LITERAL, self.parse_postfix_expression)
        self.register_postfix(TokenType.FLOAT_LITERAL, self.parse_postfix_expression)
        self.register_postfix(TokenType.CLOSE_PAREN, self.parse_postfix_expression)

        # in blocks
        self.register_in_block("IDENTIFIER", self.parse_ident_statement)
        self.register_in_block(TokenType.IWF, self.parse_if_statement)
        self.register_in_block(TokenType.WETUWN, self.parse_return_statement)
        self.register_in_block(TokenType.WHIWE, self.parse_while_statement)
        self.register_in_block(TokenType.DO_WHIWE, self.parse_while_statement)
        self.register_in_block(TokenType.FOW, self.parse_for_statement)

    def parse_program(self) -> Program:
        '''
        parse the entire program
        '''
        p = Program()
        while not self.curr_tok_is(TokenType.EOF):
            match self.curr_tok.token:
                case TokenType.FWUNC:
                    if self.peek_tok_is(TokenType.MAINUWU):
                        if p.mainuwu is not None:
                            self.multiple_mainuwu_error()
                            self.advance(2)
                            continue
                        p.mainuwu = self.parse_function()
                    else:
                        p.functions.append(self.parse_function())
                case TokenType.CWASS:
                    p.classes.append(self.parse_class())
                case TokenType.GWOBAW:
                    p.globals.append(self.parse_declaration())
                case TokenType.TERMINATOR | TokenType.DOUBLE_CLOSE_BRACKET:
                    self.advance()
                case _:
                    self.invalid_global_declaration_error(self.curr_tok)
                    self.advance()
        return p

    def parse_declaration(self, ident = None):
        '''
        parse declarations of variables/constants, whether global or local.
        if encountered brackets, the parsed declaration is an array declaration.

        eg.
        `aqua-chan = 5~`
        `shion-chan~`
        `ojou-chan-dono = 5~`
        `lap-chan = another_ident~`

        NOTE: peek_tok should be the ident, not the curr_tok, when calling this
        '''
        d = Declaration()

        # if coming from other parsers, the ident is already set
        if ident:
            d.id = ident
        else:
            if not self.expect_peek_is_identifier():
                self.no_ident_in_declaration_error(self.peek_tok)
                self.advance(2)
                return None
            d.id = self.curr_tok

        if not self.expect_peek(TokenType.DASH):
            self.no_data_type_indicator_error(self.peek_tok)
            self.advance(2)
            return None

        data_types = [
            TokenType.CHAN,
            TokenType.KUN,
            TokenType.SAMA,
            TokenType.SENPAI,
        ]
        if not self.expect_peek_in(data_types):
            self.no_data_type_error(self.peek_tok)
            self.advance(2)
            return None
        d.dtype = self.curr_tok

        # array declaration
        if self.expect_peek(TokenType.OPEN_BRACKET):
            ad = ArrayDeclaration()
            ad.id, ad.dtype = d.id, d.dtype
            d = ad
            d.dtype.lexeme += "[]"
            if not self.expect_peek(TokenType.CLOSE_BRACKET):
                self.unclosed_bracket_error(self.peek_tok)
                self.advance(2)
                return None

        # -dono to indicate constant
        if self.expect_peek(TokenType.DASH):
            if not self.expect_peek(TokenType.DONO):
                self.no_dono_error(self.peek_tok)
                self.advance(2)
                return None
            d.is_const = True

        # uninitialized
        if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
            # disallow uninitialized for constants
            if d.is_const:
                self.uninitialized_constant_error(self.peek_tok)
                self.advance(2)
                return None
            # allow uninitialized for variables
            if not self.expect_peek(TokenType.TERMINATOR):
                self.unterminated_error(self.peek_tok)
                self.advance(2)
                return None
            return d

        # initialized
        self.advance()
        if self.curr_tok_is(TokenType.TERMINATOR):
            self.uninitialized_assignment_error(self.peek_tok)
            return None
        d.value = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.TERMINATOR):
            self.unterminated_error(self.peek_tok)
            self.advance(2)
            return None
        return d

    ### statement parsers
    def parse_return_statement(self):
        'parse return statements'
        rs = ReturnStatement()
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None
        self.advance() # consume the open paren
        rs.expr = self.parse_expression(LOWEST)

        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.advance()
            self.unclosed_paren_error(self.curr_tok)
            return None
        if not self.expect_peek(TokenType.TERMINATOR):
            self.advance()
            self.unterminated_error(self.curr_tok)
            return None
        return rs

    # block statements
    def parse_function(self):
        func = Function()

        if not self.expect_peek_is_identifier() and not self.expect_peek(TokenType.MAINUWU):
            self.no_ident_in_func_declaration_error(self.peek_tok)
            self.advance(2)
            return None
        func.id = self.curr_tok

        if not self.expect_peek(TokenType.DASH):
            self.no_data_type_indicator_error(self.peek_tok)
            self.advance(2)
            return None

        data_types = [
            TokenType.CHAN,
            TokenType.KUN,
            TokenType.SAMA,
            TokenType.SENPAI,
            TokenType.SAN
        ]

        if not self.expect_peek_in(data_types):
            self.no_data_type_error(self.peek_tok)
            self.advance(2)
            return None
        func.rtype = self.curr_tok
        func.params = self.parse_params()
        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None
        func.body = self.parse_block_statement()
        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.advance()
            self.unclosed_bracket_error(self.curr_tok)
            return None

        return func

    def parse_class(self):
        'parse classes'
        c = Class()
        if not self.expect_peek_is_class_name():
            self.no_ident_in_class_declaration_error(self.peek_tok)
            self.advance(2)
            return None
        c.id = self.curr_tok
        c.params = self.parse_params()
        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None
        self.advance()
        c.body = BlockStatement()
        stop_conditions = [TokenType.DOUBLE_CLOSE_BRACKET, TokenType.EOF]
        while not self.curr_tok_is_in(stop_conditions):
            match self.curr_tok.token:
                case TokenType.FWUNC:
                    c.methods.append(self.parse_function())
                    self.advance() # consume the double close bracket
                case _:
                    inner_stop_conditions = stop_conditions + [TokenType.FWUNC]
                    while not self.curr_tok_is_in(inner_stop_conditions):
                        if self.curr_tok_is(TokenType.WETUWN):
                            self.return_in_class_error()
                            self.advance()
                            continue
                        elif isinstance(self.curr_tok.token, UniqueTokenType):
                            parser = self.get_in_block_parse_fn("IDENTIFIER")
                        else:
                            parser = self.get_in_block_parse_fn(self.curr_tok.token)
                        if parser is None:
                            self.no_in_block_parse_fn_error(self.curr_tok.token)
                            self.advance()
                            continue
                        statement = parser()
                        c.body.statements.append(statement)
                        self.advance()
        if not self.curr_tok_is(TokenType.DOUBLE_CLOSE_BRACKET):
            self.unclosed_bracket_error(self.curr_tok)
            return None
        return c

    def parse_params(self):
        'note that this must start with ( in peek_tok'
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None

        if not self.expect_peek(TokenType.CLOSE_PAREN):
            parameters: list[Parameter] = []
            while True:
                param = Parameter()
                if not self.expect_peek_is_identifier():
                    self.no_ident_in_param_error(self.peek_tok)
                    self.advance(2)
                    return None
                param.id = self.curr_tok

                if not self.expect_peek(TokenType.DASH):
                    self.no_data_type_indicator_error(self.peek_tok)
                    self.advance(2)
                    return None

                data_types = [
                    TokenType.CHAN,
                    TokenType.KUN,
                    TokenType.SAMA,
                    TokenType.SENPAI,
                ]

                if not self.expect_peek_in(data_types):
                    self.no_data_type_error(self.peek_tok)
                    self.advance(2)
                    return None
                param.dtype = self.curr_tok
                parameters.append(param)

                if self.expect_peek(TokenType.OPEN_BRACKET):
                    ad = ArrayDeclaration()
                    ad.id, ad.dtype = param.id, param.dtype
                    param = ad
                    param.dtype.lexeme += "[]"
                    if not self.expect_peek(TokenType.CLOSE_BRACKET):
                        self.unclosed_bracket_error(self.peek_tok)
                        self.advance(2)
                        return None

                if self.expect_peek(TokenType.COMMA):
                    continue
                elif self.expect_peek(TokenType.CLOSE_PAREN):
                    break
                else:
                    self.invalid_parameter(self.peek_tok)
                    self.advance(2)
                    return None

            return parameters

    def  parse_if_statement(self):
        ie = IfExpression()
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None
        self.advance()
        ie.condition = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.advance()
            self.unclosed_paren_error(self.curr_tok)
            return None
        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None
        ie.then = self.parse_block_statement()
        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.advance()
            self.unclosed_bracket_error(self.curr_tok)
            return None

        while self.expect_peek(TokenType.EWSE_IWF):
            eie = ElseIfExpression()
            if not self.expect_peek(TokenType.OPEN_PAREN):
                self.peek_error(TokenType.OPEN_PAREN)
                self.advance()
                return None
            self.advance()
            eie.condition = self.parse_expression(LOWEST)
            if not self.expect_peek(TokenType.CLOSE_PAREN):
                self.advance()
                self.unclosed_paren_error(self.curr_tok)
                return None
            if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
                self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
                self.advance()
                return None
            eie.then = self.parse_block_statement()
            if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
                self.advance()
                self.unclosed_bracket_error(self.curr_tok)
                return None
            ie.else_if.append(eie)

        if self.expect_peek(TokenType.EWSE):
            if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
                self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
                self.advance()
                return None
            ie.else_block = self.parse_block_statement()
            if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
                self.advance()
                self.unclosed_bracket_error(self.curr_tok)
                return None
        return ie

    def parse_block_statement(self):
        'take note that this starts with the open bracket as the current token'
        bs = BlockStatement()
        self.advance() # consume the open bracket
        stop_condition = [TokenType.DOUBLE_CLOSE_BRACKET, TokenType.EOF]
        while not self.peek_tok_is_in(stop_condition):
            if isinstance(self.curr_tok.token, UniqueTokenType):
                parser = self.get_in_block_parse_fn("IDENTIFIER")
            else:
                parser = self.get_in_block_parse_fn(self.curr_tok.token)
            if parser is None:
                self.no_in_block_parse_fn_error(self.curr_tok.token)
                self.advance()
                continue
            statement = parser()
            bs.statements.append(statement)
            if self.peek_tok_is_in(stop_condition):
                break
            self.advance()

        return bs

    def parse_ident_statement(self):
        'identifier statements are declarations and assignments'
        ident = self.curr_tok
        # is a declaration
        if self.peek_tok_is(TokenType.DASH):
            return self.parse_declaration(ident)
        # is an assignment
        a = Assignment()
        a.id = ident
        if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
            self.peek_error(self.peek_tok)
            self.advance()
            return None
        self.advance()
        a.value = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.TERMINATOR):
            self.advance()
            self.unterminated_error(self.curr_tok)
            return None
        return a

    def parse_while_statement(self):
        'this includes do while block statements'
        wl = WhileLoop()
        if self.curr_tok_is(TokenType.DO_WHIWE):
            wl.is_do = True
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None
        self.advance()
        wl.condition = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.advance()
            self.unclosed_paren_error(self.curr_tok)
            return None
        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None
        wl.body = self.parse_block_statement()
        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.advance()
            self.unclosed_bracket_error(self.curr_tok)
            return None
        return wl

    def parse_for_statement(self):
        fl = ForLoop()
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None
        self.advance()

        # just an identifier without initialization or assignment
        if self.peek_tok_is(TokenType.TERMINATOR):
            fl.init = self.parse_literal()
            self.advance()
        # is either a declaration or an assignment
        else:
            fl.init = self.parse_ident_statement()

        if not self.curr_tok_is(TokenType.TERMINATOR):
            self.peek_error(TokenType.TERMINATOR)
            self.advance()
            return None
        self.advance()
        fl.condition = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.TERMINATOR):
            self.peek_error(TokenType.TERMINATOR)
            self.advance()
            return None
        self.advance()
        fl.update = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.advance()
            self.unclosed_paren_error(self.curr_tok)
            return None
        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None
        fl.body = self.parse_block_statement()
        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.advance()
            self.unclosed_bracket_error(self.curr_tok)
            return None
        return fl

    def parse_print(self):
        p = Print()
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None
        self.advance()
        stop_conditions = [TokenType.CLOSE_PAREN, TokenType.TERMINATOR, TokenType.EOF]
        while not self.curr_tok_is_in(stop_conditions):
            p.values.append(self.parse_expression(LOWEST))
            if not self.expect_peek(TokenType.COMMA) and not self.peek_tok_is_in(stop_conditions):
                break
            self.advance()
        if not self.curr_tok_is(TokenType.CLOSE_PAREN):
            self.unclosed_paren_error(self.curr_tok)
            return None
        if not self.expect_peek(TokenType.TERMINATOR):
            self.advance()
            self.unterminated_error(self.curr_tok)
            return None
        return p

    def parse_input(self):
        i = Input()
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None
        self.advance()
        i.value = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.advance()
            self.unclosed_paren_error(self.curr_tok)
            return None
        if not self.expect_peek(TokenType.TERMINATOR):
            self.advance()
            self.unterminated_error(self.curr_tok)
            return None
        return i

    ### expression parsers
    def parse_expression(self, precedence):
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
            prefix = self.get_prefix_parse_fn("IDENTIFIER")
        else:
            prefix = self.get_prefix_parse_fn(self.curr_tok.token)

        if prefix is None:
            self.no_prefix_parse_fn_error(self.curr_tok.token)
            return None

        left_exp = prefix()

        while not self.peek_tok_is_in([TokenType.TERMINATOR, TokenType.EOF]) and precedence < self.peek_precedence():
            infix = self.get_infix_parse_fn(self.peek_tok.token)
            if infix is None:
                return left_exp
            self.advance()
            left_exp = infix(left_exp)

        if isinstance(self.curr_tok.token, UniqueTokenType):
            postfix = self.get_postfix_parse_fn("IDENTIFIER")
        else:
            postfix = self.get_postfix_parse_fn(self.curr_tok.token)
        if postfix is not None:
            left_exp = postfix(left_exp)

        return left_exp
    # PLEASE USE self.parse_expression(precedence)
    # to use the 4 methods below in other parsers.
    # DO NOT USE THESE 4 METHODS DIRECTLY
    def parse_prefix_expression(self):
        '''
        parse prefix expressions.
        Only prefix expression in UwU++ that is parsed here are negative idents.
        This is because negative int/float literals are tokenized
        '''
        pe = PrefixExpression()
        pe.op = self.curr_tok

        self.advance()
        pe.right = self.parse_expression(PREFIX)
        return pe
    def parse_infix_expression(self, left):
        '''
        parse infix expressions.
        eg.
        1 + 2
        1 != 2
        shion + aqua == fax
        '''
        ie = InfixExpression()
        ie.left = left
        ie.op = self.curr_tok.token

        precedence = self.curr_precedence()
        self.advance()
        ie.right = self.parse_expression(precedence)
        return ie
    def parse_postfix_expression(self, left):
        '''
        parse postfix expressions
        eg.
        1
        1++
        1--
        '''
        pe = PostfixExpression()
        pe.left = left
        if not self.expect_peek_in([TokenType.INCREMENT_OPERATOR, TokenType.DECREMENT_OPERATOR]):
            return left
        pe.op = self.curr_tok
        return pe
    def parse_grouped_expressions(self):
        '''
        parse grouped expressions
        eg.
        (1 + 2)
        (shion + aqua) + ojou
        '''
        self.advance()
        expr = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.advance()
            self.unclosed_paren_error(self.curr_tok)
            return None
        return expr


    ### atomic parsers
    # unlike the above 4 expressions parsers,
    # these are made to be used in other parsers
    def parse_ident(self):
        'parse identifiers which can also be function calls'
        if not self.peek_tok_is(TokenType.OPEN_PAREN):
            return self.curr_tok

        fc = FnCall()
        fc.id = self.curr_tok
        self.advance(2)
        stop_conditions = [TokenType.CLOSE_PAREN, TokenType.TERMINATOR, TokenType.EOF]
        while not self.curr_tok_is_in(stop_conditions):
            fc.args.append(self.parse_expression(LOWEST))
            if not self.expect_peek(TokenType.COMMA) and not self.peek_tok_is_in(stop_conditions):
                break
            self.advance()
        if not self.curr_tok_is(TokenType.CLOSE_PAREN):
            self.unclosed_paren_error(self.curr_tok)
            return None
        return fc
    def parse_array(self):
        al = ArrayLiteral()
        self.advance() # consume the opening brace

        stop_conditions = [TokenType.CLOSE_BRACE, TokenType.TERMINATOR, TokenType.EOF]
        while not self.curr_tok_is_in(stop_conditions):
            al.elements.append(self.parse_expression(LOWEST))
            if not self.expect_peek(TokenType.COMMA) and not self.peek_tok_is_in(stop_conditions):
                break
            self.advance()

        if not self.curr_tok_is(TokenType.CLOSE_BRACE):
            self.unclosed_brace_error(self.peek_tok)
            return None
        return al
    def parse_string_parts(self):
        sf = StringFmt()
        sf.start = self.curr_tok
        # append middle parts if any
        while not self.peek_tok_is_in([TokenType.STRING_PART_END, TokenType.TERMINATOR, TokenType.EOF]):
            # no expression after string_mid
            if self.peek_tok_is(TokenType.STRING_PART_MID):
                sf.exprs.append(Token("", TokenType.STRING_LITERAL, (0, 0), (0, 0)))
                self.advance()
            # expressions
            else:
                self.advance()
                sf.exprs.append(self.parse_expression(LOWEST))

            if self.expect_peek(TokenType.STRING_PART_MID):
                sf.mid.append(self.curr_tok)

        if not self.expect_peek(TokenType.STRING_PART_END):
            self.unclosed_string_part_error(sf.start, self.peek_tok)
            return None
        sf.end = self.curr_tok
        return sf
    def parse_literal(self):
        'returns the current token'
        return self.curr_tok

    ### helper methods
    # registering prefix and infix functions to parse certain token types
    def register_prefix(self, token_type: str | TokenType, fn: Callable):
        self.prefix_parse_fns[token_type] = fn
    def register_infix(self, token_type: str | TokenType, fn: Callable):
        self.infix_parse_fns[token_type] = fn
    def register_postfix(self, token_type: str | TokenType, fn: Callable):
        self.postfix_parse_fns[token_type] = fn
    def register_in_block(self, token_type: str | TokenType, fn: Callable):
        self.in_block_parse_fns[token_type] = fn
    # getting prefix and infix functions
    def get_prefix_parse_fn(self, token_type: str | TokenType) -> Callable | None:
        try:
            tmp = self.prefix_parse_fns[token_type]
            return tmp
        except KeyError:
            return None
    def get_infix_parse_fn(self, token_type: str | TokenType) -> Callable | None:
        try:
            tmp = self.infix_parse_fns[token_type]
            return tmp
        except KeyError:
            return None
    def get_postfix_parse_fn(self, token_type: str | TokenType) -> Callable | None:
        try:
            tmp = self.postfix_parse_fns[token_type]
            return tmp
        except KeyError:
            return None
    def get_in_block_parse_fn(self, token_type: str | TokenType) -> Callable | None:
        try:
            tmp = self.in_block_parse_fns[token_type]
            return tmp
        except KeyError:
            return None
    # keeping track of tokens
    def curr_tok_is(self, token_type: TokenType) -> bool:
        return self.curr_tok.token == token_type
    def peek_tok_is(self, token_type: TokenType) -> bool:
        return self.peek_tok.token == token_type
    def expect_peek(self, token_type: TokenType) -> bool:
        '''
        checks if the next token is the given token type.
        advances the cursor if it is.
        cursor won't advance if not.
        '''
        if self.peek_tok_is(token_type):
            self.advance()
            return True
        else:
            return False
    def expect_peek_is_identifier(self) -> bool:
        '''
        checks if the next token is an identifier.
        advances the cursor if it is.
        cursor won't advance if not.
        '''
        if self.peek_tok.token.token.startswith("IDENTIFIER"):
            self.advance()
            return True
        else:
            return False
    def expect_peek_is_class_name(self) -> bool:
        '''
        checks if the next token is a class name.
        advances the cursor if it is.
        cursor won't advance if not.
        '''
        if self.peek_tok.token.token.startswith("CWASS"):
            self.advance()
            return True
        else:
            return False
    def curr_tok_is_in(self, token_types: list[TokenType]) -> bool:
        'checks if the current token is in the list of token types.'
        return self.curr_tok.token in token_types
    def peek_tok_is_in(self, token_types: list[TokenType]) -> bool:
        'checks if the next token is in the list of token types.'
        return self.peek_tok.token in token_types
    def expect_peek_in(self, token_types: list[TokenType]) -> bool:
        '''
        checks if the next token is in the list of token types.
        advances the cursor if it is.
        cursor won't advance if not.
        '''
        if self.peek_tok_is_in(token_types):
            self.advance()
            return True
        else:
            return False
    # to keep track of precedence of tokens
    def curr_precedence(self):
        'returns the precedence of the current token'
        if self.curr_tok.token in precedence_map:
            return precedence_map[self.curr_tok.token]
        else:
            return LOWEST
    def peek_precedence(self):
        'returns the precedence of the next token'
        if self.peek_tok.token in precedence_map:
            return precedence_map[self.peek_tok.token]
        else:
            return LOWEST

    ### error methods
    # general error
    def peek_error(self, token: TokenType):
        self.errors.append(f"expected next token to be '{token}', got '{self.peek_tok}' instead")
    def no_prefix_parse_fn_error(self, token_type):
        self.errors.append(f"no prefix parsing function found for {token_type}")
    def no_in_block_parse_fn_error(self, token_type):
        self.errors.append(f"no parsing function found for {token_type} inside block statements")
    def invalid_global_declaration_error(self, token: Token):
        self.errors.append(f"Expected global function/class/variable/constant declaration, got {token.lexeme}")
    def no_ident_in_declaration_error(self, token: Token):
        self.errors.append(f"Expected identifier in declaration, got {token.lexeme}")
    def no_ident_in_class_declaration_error(self, token: Token):
        self.errors.append(f"Expected identifier in class declaration, got {token.lexeme}")
    def no_ident_in_func_declaration_error(self, token: Token):
        self.errors.append(f"Expected identifier in function declaration, got {token.lexeme}")
    def no_ident_in_param_error(self, token: Token):
        self.errors.append(f"Expected identifier in parameter, got {token.lexeme}")
    def no_data_type_indicator_error(self, token: Token):
        self.errors.append(f"Expected dash before data type, got {token.lexeme}")
    def no_data_type_error(self, token: Token):
        self.errors.append(f"Expected data type, got {token.lexeme}")
    def no_dono_error(self, token: Token):
        self.errors.append(f"Expected 'dono' to denote variable as constant instead, got {token.lexeme}")
    def invalid_parameter(self, token: Token):
        self.errors.append(f"Invalid parameter. Expected ',' or ')', got {token.lexeme}")
    def unterminated_error(self, token: Token):
        self.errors.append(f"Expected '~' to terminate the statement, got {token.lexeme}")
    def unclosed_paren_error(self, token: Token):
        self.errors.append(f"Expected ')' to close the parenthesis, got {token.lexeme}")
    def unclosed_bracket_error(self, token: Token):
        self.errors.append(f"Expected ']' to close the bracket, got {token.lexeme}")
    def unclosed_brace_error(self, token: Token):
        self.errors.append(f"Expected '}}' to close the brace, got {token.lexeme}")
    def uninitialized_constant_error(self, token: Token):
        self.errors.append(f"Constants must be initialized. got '{token.lexeme}'")
    def uninitialized_assignment_error(self, token: Token):
        self.errors.append(f"Assignments must have a value after '='. got '{token.lexeme}'")
    def unclosed_string_part_error(self, string_start, token: Token):
        self.errors.append(f"Unclosed string part. Expected '{string_start.lexeme[:-1]}|' to be closed by something like '|string part end\"'. got '{token.lexeme}'")
    def multiple_mainuwu_error(self):
        self.errors.append("Multiple mainuwu function declaration")
    def return_in_class_error(self):
        self.errors.append("Return statement in class declaration")
    def return_in_func_error(self):
        self.errors.append("Found return statement in class declaration")
