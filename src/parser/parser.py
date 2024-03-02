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
from .error_handler import Error
from src.lexer.token import Token, TokenType, UniqueTokenType
from src.parser.productions import *

'''
To keep track of the precedence of each token.

idents:                 LOWEST
&&, ||                  LOGICAL
==, !=                  EQUALITY
<, >, <=, >=:           LESS_GREATER
&:                      CONCAT
+, -:                   SUM
*, /, %:                PRODUCT
- (as in negative):     PREFIX
ident():                FN_CALL
'''
LOWEST = 0
LOGICAL = 1
EQUALITY = 2
LESS_GREATER = 3
CONCAT = 4
SUM = 5
PRODUCT = 6
PREFIX = 7
FN_CALL = 8

precedence_map = {
    TokenType.AND_OPERATOR: LOGICAL,
    TokenType.OR_OPERATOR: LOGICAL,
    TokenType.EQUALITY_OPERATOR: EQUALITY,
    TokenType.INEQUALITY_OPERATOR: EQUALITY,
    TokenType.LESS_THAN_SIGN: LESS_GREATER,
    TokenType.LESS_THAN_OR_EQUAL_SIGN: LESS_GREATER,
    TokenType.GREATER_THAN_SIGN: LESS_GREATER,
    TokenType.GREATER_THAN_OR_EQUAL_SIGN: LESS_GREATER,
    TokenType.CONCATENATION_OPERATOR: CONCAT,
    TokenType.ADDITION_SIGN: SUM,
    TokenType.DASH: SUM,
    TokenType.MULTIPLICATION_SIGN: PRODUCT,
    TokenType.DIVISION_SIGN: PRODUCT,
    TokenType.MODULO_SIGN: PRODUCT,
}

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = [token for token in tokens if token.token not in [TokenType.WHITESPACE, TokenType.SINGLE_LINE_COMMENT, TokenType.MULTI_LINE_COMMENT]]
        self.errors: list = []

        # to associate prefix and infix parsing functions for certain token types
        # key : val == TokenType : ParsingFunction
        self.prefix_parse_fns: dict = {}
        self.infix_parse_fns: dict = {}
        self.postfix_parse_fns: dict = {}
        self.in_block_parse_fns: dict = {}
        self.register_init()

        if not self.tokens:
            self.missing_mainuwu_error(Token("EOF", TokenType.EOF, (0, 0), (0, 0)))
            self.program = None
            return

        # to keep track of tokens
        self.pos = 0
        self.curr_tok = self.tokens[self.pos]
        self.peek_tok = self.tokens[self.pos + 1]

        eof_pos = (self.tokens[-1].end_position[0], self.tokens[-1].end_position[1] + 1)
        self.tokens.append(Token("EOF", TokenType.EOF, eof_pos, eof_pos))
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

        # literals (just returns curr_tok)
        self.register_prefix("IDENTIFIER", self.parse_ident)
        self.register_prefix("CWASS", self.parse_class_ident)
        self.register_prefix(TokenType.INT_LITERAL, self.parse_literal)
        self.register_prefix(TokenType.STRING_LITERAL, self.parse_literal)
        self.register_prefix(TokenType.FLOAT_LITERAL, self.parse_literal)
        self.register_prefix(TokenType.FAX, self.parse_literal)
        self.register_prefix(TokenType.CAP, self.parse_literal)
        self.register_prefix(TokenType.NUWW, self.parse_literal)
        self.register_prefix(TokenType.INPWT, self.parse_input)

        # infixes
        self.register_infix(TokenType.EQUALITY_OPERATOR, self.parse_infix_expression)
        self.register_infix(TokenType.INEQUALITY_OPERATOR, self.parse_infix_expression)
        self.register_infix(TokenType.AND_OPERATOR, self.parse_infix_expression)
        self.register_infix(TokenType.OR_OPERATOR, self.parse_infix_expression)
        self.register_infix(TokenType.LESS_THAN_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.LESS_THAN_OR_EQUAL_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.GREATER_THAN_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.GREATER_THAN_OR_EQUAL_SIGN, self.parse_infix_expression)
        self.register_infix(TokenType.CONCATENATION_OPERATOR, self.parse_infix_expression)
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
        self.register_in_block("CWASS", self.parse_class_ident_statement)
        self.register_in_block(TokenType.IWF, self.parse_if_statement)
        self.register_in_block(TokenType.WETUWN, self.parse_return_statement)
        self.register_in_block(TokenType.WHIWE, self.parse_while_statement)
        self.register_in_block(TokenType.DO_WHIWE, self.parse_while_statement)
        self.register_in_block(TokenType.FOW, self.parse_for_statement)
        self.register_in_block(TokenType.PWINT, self.parse_print)
        # self.register_in_block(TokenType.INPWT, self.parse_input)

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
                            self.multiple_mainuwu_error(self.peek_tok)
                            self.advance(2)
                        else:
                            if res := self.parse_function(main=True):
                                p.mainuwu = res
                    else:
                        if res := self.parse_function():
                            p.functions.append(res)
                case TokenType.CWASS:
                    if res := self.parse_class():
                        p.classes.append(res)
                case TokenType.GWOBAW:
                    if res := self.parse_declaration():
                        p.globals.append(res)
                case TokenType.TERMINATOR | TokenType.DOUBLE_CLOSE_BRACKET:
                    self.advance()
                case _:
                    self.invalid_global_declaration_error(self.curr_tok)
                    self.advance()

        if p.mainuwu is None:
            self.missing_mainuwu_error(self.curr_tok)

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
            TokenType.SAN
        ]
        if not self.expect_peek_in(data_types):
            # Check for class id as data type
            if not self.expect_peek_is_class_name():
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

        if (res := self.parse_expression(LOWEST)) is None:
            return None
        d.value = res
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

        if (res := self.parse_expression(LOWEST)) is None:
            return None
        rs.expr = res

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
    def parse_function(self, main=False):
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

        if main:
            if not self.expect_peek(TokenType.SAN):
                self.invalid_mainuwu_rtype_error(self.peek_tok)
                self.advance(2)
                return None
        else:
            data_types = [
                TokenType.CHAN,
                TokenType.KUN,
                TokenType.SAMA,
                TokenType.SENPAI,
                TokenType.SAN
            ]

            if not self.expect_peek_in(data_types):
                # Check for class id as data type
                if not self.expect_peek_is_class_name():
                    self.no_data_type_error(self.peek_tok)
                    self.advance(2)
                    return None

        func.rtype = self.curr_tok

        # is array return type
        if self.expect_peek(TokenType.OPEN_BRACKET):
            if not self.expect_peek(TokenType.CLOSE_BRACKET):
                self.unclosed_bracket_error(self.peek_tok)
                self.advance(2)
                return None
            func.rtype.lexeme += "[]"

        if res := self.parse_params(main=main):
            func.params = res

        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance(2)
            return None

        if (res := self.parse_block_statement()) is None:
            return None
        func.body = res

        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.advance(2)
            self.unclosed_double_bracket_error(self.curr_tok)
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

        if res := self.parse_params():
            c.params = res

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
                    if (res := self.parse_function()) is None:
                        return None
                    c.methods.append(res)
                    self.advance() # consume the double close bracket
                case _:
                    inner_stop_conditions = stop_conditions + [TokenType.FWUNC]
                    while not self.curr_tok_is_in(inner_stop_conditions):
                        parser = self.get_in_block_parse_fn(self.curr_tok.token)
                        if parser is None:
                            self.no_in_block_parse_fn_error(self.curr_tok.token)
                            self.advance()
                            return None
                        if (statement := parser()) is None:
                            return None
                        c.body.statements.append(statement)
                        self.advance()
        if not self.curr_tok_is(TokenType.DOUBLE_CLOSE_BRACKET):
            self.unclosed_double_bracket_error(self.curr_tok)
            return None
        return c

    def parse_params(self, main=False):
        'note that this must start with ( in peek_tok'
        parameters: list[Parameter] = []
        param = Parameter()

        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None

        if not self.expect_peek(TokenType.CLOSE_PAREN):
            # If parameters are for main function, raise error immediately cuz it can't have params
            if main:
                self.invalid_mainuwu_params_error(self.peek_tok)
                self.advance()
                return None

            while True:
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
                    TokenType.SAN
                ]

                if not self.expect_peek_in(data_types):
                    # Check for class id as data type
                    if not self.expect_peek_is_class_name():
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
                    self.invalid_parameter_error(self.peek_tok)
                    self.advance(2)
                    return None
            return parameters

    def  parse_if_statement(self):
        ie = IfStatement()
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None

        # Check if condition is empty
        if self.peek_tok_is(TokenType.CLOSE_PAREN):
            self.empty_condition_error()
            self.advance()
            return None
        else:
            self.advance()
            if (res := self.parse_expression(LOWEST)) is None:
                return None
            ie.condition = res

            if not self.expect_peek(TokenType.CLOSE_PAREN):
                self.unclosed_paren_error(self.peek_tok)
                self.advance()
                return None

        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None

        if (res := self.parse_block_statement()) is None:
            return None
        ie.then = res

        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.unclosed_double_bracket_error(self.peek_tok)
            self.advance()
            return None

        while self.expect_peek(TokenType.EWSE_IWF):
            eie = ElseIfStatement()
            if not self.expect_peek(TokenType.OPEN_PAREN):
                self.peek_error(TokenType.OPEN_PAREN)
                self.advance()
                return None
            self.advance()
            if (res := self.parse_expression(LOWEST)) is None:
                return None
            eie.condition = res

            if not self.expect_peek(TokenType.CLOSE_PAREN):
                self.advance()
                self.unclosed_paren_error(self.curr_tok)
                return None
            if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
                self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
                self.advance()
                return None

            if (res := self.parse_block_statement()) is None:
                return None
            eie.then = res

            if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
                self.unclosed_double_bracket_error(self.peek_tok)
                self.advance()
                return None
            ie.else_if.append(eie)

        if self.expect_peek(TokenType.EWSE):
            if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
                self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
                self.advance()
                return None

            es = ElseStatement()
            if (res := self.parse_block_statement()) is None:
                return None
            es.body = res
            ie.else_block = es

            if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
                self.unclosed_double_bracket_error(self.peek_tok)
                self.advance()
                return None
        return ie

    def parse_block_statement(self):
        '''
        starts with the open bracket as the current token
        ends with the close bracket in peek token
        '''
        bs = BlockStatement()

        # Check if block is empty
        if self.peek_tok_is(TokenType.DOUBLE_CLOSE_BRACKET):
            self.empty_code_body_error()
            return None

        stop_condition = [TokenType.DOUBLE_CLOSE_BRACKET, TokenType.EOF]
        while not self.peek_tok_is_in(stop_condition):
            self.advance()
            parser = self.get_in_block_parse_fn(self.curr_tok.token)
            if parser is None:
                self.no_in_block_parse_fn_error(self.curr_tok.token)
                self.advance()
                continue
            if (statement := parser()) is None:
                return None
            bs.statements.append(statement)
        return bs

    def parse_ident_statement(self):
        '''
        must start with Unique identifier in curr_tok
        class identifier statements are class declarations and assignments
        '''
        if (res := self.parse_ident()) is None:
            return None
        ident = res

        # is not a declaration or assignment
        if self.expect_peek(TokenType.TERMINATOR):
            id_stm = IdStatement()
            id_stm.id = ident
            return id_stm

        # is a declaration
        if self.peek_tok_is(TokenType.DASH):
            return self.parse_declaration(ident)

        # is an assignment
        a = Assignment()
        a.id = ident
        if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
            self.peek_error(TokenType.ASSIGNMENT_OPERATOR)
            self.advance()
            return None

        self.advance()
        if (res := self.parse_expression(LOWEST)) is None:
            return None
        a.value = res

        if not self.expect_peek(TokenType.TERMINATOR):
            self.advance()
            self.unterminated_error(self.curr_tok)
            return None
        return a

    def parse_class_ident_statement(self):
        '''
        must start with Unique class identifier in curr_tok
        class identifier statements are class declarations and assignments
        '''
        if (res := self.parse_class_ident()) is None:
            return None
        ident = res

        # is not a declaration or assignment
        if self.expect_peek(TokenType.TERMINATOR):
            id_stm = IdStatement()
            id_stm.id = ident
            return id_stm

        # is a declaration
        if self.peek_tok_is(TokenType.DASH):
            return self.parse_declaration(ident)

        # is an assignment
        a = Assignment()
        a.id = ident
        if not self.expect_peek(TokenType.ASSIGNMENT_OPERATOR):
            self.peek_error(TokenType.ASSIGNMENT_OPERATOR)
            self.advance()
            return None

        self.advance()
        if (res := self.parse_expression(LOWEST)) is None:
            return None
        a.value = res

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

        # Check if condition is empty
        if self.peek_tok_is(TokenType.CLOSE_PAREN):
            self.empty_condition_error()
            self.advance()
            return None
        else:
            self.advance()
            if (res := self.parse_expression(LOWEST)) is None:
                return None
            wl.condition = res

            if not self.expect_peek(TokenType.CLOSE_PAREN):
                self.advance()
                self.unclosed_paren_error(self.curr_tok)
                return None

        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None

        if (res := self.parse_block_statement()) is None:
            return None
        wl.body = res

        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.unclosed_double_bracket_error(self.peek_tok)
            self.advance()
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
            if (res := self.parse_literal()) is None:
                return None
            fl.init = res
            self.advance()
        # is either a declaration or an assignment
        else:
            if (res := self.parse_ident_statement()) is None:
                return None
            fl.init = res

        if not self.curr_tok_is(TokenType.TERMINATOR):
            self.peek_error(TokenType.TERMINATOR)
            self.advance()
            return None
        self.advance()

        if (res := self.parse_expression(LOWEST)) is None:
            return None
        fl.condition = res

        if not self.expect_peek(TokenType.TERMINATOR):
            self.peek_error(TokenType.TERMINATOR)
            self.advance()
            return None

        self.advance()
        if (res := self.parse_expression(LOWEST)) is None:
            return None
        fl.update = res

        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.unclosed_paren_error(self.peek_tok)
            self.advance()
            return None
        if not self.expect_peek(TokenType.DOUBLE_OPEN_BRACKET):
            self.peek_error(TokenType.DOUBLE_OPEN_BRACKET)
            self.advance()
            return None

        if (res := self.parse_block_statement()) is None:
            return None
        fl.body = res

        if not self.expect_peek(TokenType.DOUBLE_CLOSE_BRACKET):
            self.unclosed_double_bracket_error(self.peek_tok)
            self.advance()
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
            if (res := self.parse_expression(LOWEST)) is None:
                return None
            p.values.append(res)
            if not self.expect_peek(TokenType.COMMA) and not self.peek_tok_is_in(stop_conditions):
                break
            self.advance()
        if not self.curr_tok_is(TokenType.CLOSE_PAREN):
            self.unclosed_paren_error(self.curr_tok)
            return None
        if not self.expect_peek(TokenType.TERMINATOR):
            self.unterminated_error(self.peek_tok)
            self.advance()
            return None
        return p

    # def parse_input(self):
    #     i = Input()
    #     if not self.expect_peek(TokenType.OPEN_PAREN):
    #         self.peek_error(TokenType.OPEN_PAREN)
    #         self.advance()
    #         return None
    #     self.advance()
    #
    #     if (res := self.parse_ident_statement()) is None:
    #         return None
    #     i.value = res
    #
    #     if not self.expect_peek(TokenType.CLOSE_PAREN):
    #         self.unclosed_paren_error(self.peek_tok)
    #         self.advance()
    #         return None
    #     if not self.expect_peek(TokenType.TERMINATOR):
    #         self.unterminated_error(self.peek_tok)
    #         self.advance()
    #         return None
    #     return i

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
        prefix = self.get_prefix_parse_fn(self.curr_tok.token)
        if prefix is None:
            self.no_prefix_parse_fn_error(self.curr_tok.token)
            self.advance()
            return None

        left_exp = prefix()
        postfix = self.get_postfix_parse_fn(self.curr_tok.token)
        if postfix is not None:
            left_exp = postfix(left_exp)

        while not self.peek_tok_is_in([TokenType.TERMINATOR, TokenType.EOF]) and precedence < self.peek_precedence():
            infix = self.get_infix_parse_fn(self.peek_tok.token)
            if infix is None:
                return left_exp
            self.advance()
            left_exp = infix(left_exp)

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
        must start with ( in current token
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
            return expr
        return expr


    ### atomic parsers
    # unlike the above 4 expressions parsers,
    # these are made to be used in other parsers
    def parse_ident(self):
        '''
        must start with curr_tok as IDENTIFIER
        parse identifiers which can also be:
        - function calls
        - array indexing
        - class accessors
        - any combination of the above
        '''
        ident = self.curr_tok

        if not self.peek_tok_is_in([TokenType.OPEN_PAREN, TokenType.DOT_OP, TokenType.OPEN_BRACKET]):
            return ident

        if self.peek_tok_is(TokenType.OPEN_PAREN):
            fc = FnCall()
            fc.id = ident
            ident = fc
            self.advance(2)
            stop_conditions = [TokenType.CLOSE_PAREN, TokenType.TERMINATOR, TokenType.EOF]
            while not self.curr_tok_is_in(stop_conditions):
                if (res := self.parse_expression(LOWEST)) is None:
                    return None
                ident.args.append(res)
                if not self.expect_peek(TokenType.COMMA) and not self.peek_tok_is_in(stop_conditions):
                    break
                self.advance()
            if not self.curr_tok_is(TokenType.CLOSE_PAREN):
                self.unclosed_paren_error(self.curr_tok)
                return None

        # array indexing, keep looping until curr tok is not close bracket
        if self.expect_peek(TokenType.OPEN_BRACKET):
            self.advance()
            tmp = IndexedIdentifier()
            tmp.id = ident
            ident = tmp
            if (idx := self.parse_expression(LOWEST)) is None:
                return None
            if not self.expect_peek(TokenType.CLOSE_BRACKET):
                self.unclosed_bracket_error(self.curr_tok)
                return None
            ident.index.append(idx)
            # if more indexing exists
            while self.expect_peek(TokenType.OPEN_BRACKET):
                self.advance()
                if (idx := self.parse_expression(LOWEST)) is None:
                    return None
                if not self.expect_peek(TokenType.CLOSE_BRACKET):
                    self.unclosed_bracket_error(self.peek_tok)
                    return None
                ident.index.append(idx)

        # dot operations, keep recursing parse_ident until peek tok is not dot op
        if self.expect_peek(TokenType.DOT_OP):
            tmp = ClassAccessor()
            tmp.id = ident
            ident = tmp
            if not self.expect_peek_is_identifier():
                self.invalid_dot_op_error(self.peek_tok)
                self.advance()
                return None
            if (res := self.parse_ident()) is None:
                return None
            ident.accessed = res
            # if more dot ops exist
            while self.peek_tok_is(TokenType.DOT_OP):
                tmp = ClassAccessor()
                tmp.id = ident.accessed
                if (accessed := self.parse_ident()) is None:
                    return None
                tmp.accessed = accessed
                ident.accessed = tmp
        return ident

    def parse_class_ident(self):
        ident = ClassAccessor()
        ident.id = self.curr_tok
        if not self.expect_peek(TokenType.DOT_OP):
            self.peek_error(TokenType.DOT_OP)
            self.advance()
            return None
        if not self.expect_peek_is_identifier():
            self.invalid_dot_op_error(self.peek_tok)
            self.advance()
            return None
        if (res := self.parse_ident()) is None:
            return None
        ident.accessed = res
        return ident

    def parse_array(self):
        al = ArrayLiteral()
        self.advance() # consume the opening brace

        stop_conditions = [TokenType.CLOSE_BRACE, TokenType.TERMINATOR, TokenType.EOF]
        while not self.curr_tok_is_in(stop_conditions):
            if (res := self.parse_expression(LOWEST)) is None:
                return None
            al.elements.append(res)
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
                if (res := self.parse_expression(LOWEST)) is None:
                    return None
                sf.exprs.append(res)

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

    def parse_input(self):
        inp = Input()
        if not self.expect_peek(TokenType.OPEN_PAREN):
            self.peek_error(TokenType.OPEN_PAREN)
            self.advance()
            return None
        self.advance() # consume the open paren

        if (res := self.parse_expression(LOWEST)) is None:
            return None
        inp.expr = res
        if not self.expect_peek(TokenType.CLOSE_PAREN):
            self.advance()
            self.unclosed_paren_error(self.curr_tok)
            return None
        return inp

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
        if isinstance(token_type, UniqueTokenType):
            token_type = "IDENTIFIER" if token_type.token.startswith("IDENTIFIER") else "CWASS"
        try:
            tmp = self.prefix_parse_fns[token_type]
            return tmp
        except KeyError:
            return None
    def get_infix_parse_fn(self, token_type: str | TokenType) -> Callable | None:
        if isinstance(token_type, UniqueTokenType):
            token_type = "IDENTIFIER" if token_type.token.startswith("IDENTIFIER") else "CWASS"
        try:
            tmp = self.infix_parse_fns[token_type]
            return tmp
        except KeyError:
            return None
    def get_postfix_parse_fn(self, token_type: str | TokenType) -> Callable | None:
        if isinstance(token_type, UniqueTokenType):
            token_type = "IDENTIFIER" if token_type.token.startswith("IDENTIFIER") else "CWASS"
        try:
            tmp = self.postfix_parse_fns[token_type]
            return tmp
        except KeyError:
            return None
    def get_in_block_parse_fn(self, token_type: str | TokenType) -> Callable | None:
        if isinstance(token_type, UniqueTokenType):
            token_type = "IDENTIFIER" if token_type.token.startswith("IDENTIFIER") else "CWASS"
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
        self.errors.append(Error(
            "UNEXPECTED TOKEN",
            f"Expected next token to be {token}, got '{self.peek_tok}' instead",
            self.peek_tok.position,
            self.peek_tok.end_position
        ))
    def no_prefix_parse_fn_error(self, token_type):
        self.errors.append(Error(
            "INVALID EXPRESSION TOKEN",
            f"'{token_type}' is not a valid starting token for an expression"
            f"\n\tHint: use identifiers, numbers, strings, booleans, parenthesis enclosed expressions, arrays, or 'nuww'",
            self.curr_tok.position,
            self.curr_tok.end_position
        ))
    def no_in_block_parse_fn_error(self, token_type):
        self.errors.append(Error(
            "INVALID IN-BLOCK STATEMENT TOKEN",
            f"'{token_type}' is not a valid starting token for an in-block/body statement."
            f"\n\tHint: use identifiers, 'inpwt', 'pwint', 'wetuwn', 'iwf', 'whiwe', 'do whiwe', or 'fow'",
            self.curr_tok.position,
            self.curr_tok.end_position
        ))
    def invalid_global_declaration_error(self, token: Token):
        self.errors.append(Error(
            "INVALID GLOBAL DECLARATION",
            f"Only functions, classes, and global variable declarations are allowed in the global scope."
            f"\n\t'{token.lexeme}' is an invalid starting token for global declarations."
            f"\n\tHint: use 'gwobaw', 'fwunc' or 'cwass'",
            token.position,
            token.end_position
        ))
    def no_ident_in_declaration_error(self, token: Token):
        self.errors.append(Error(
            "MISSING IDENTIFIER",
            f"Expected identifier in declaration, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def no_ident_in_class_declaration_error(self, token: Token):
        self.errors.append(Error(
            "MISSING IDENTIFIER",
            f"Expected identifier in class declaration, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def no_ident_in_func_declaration_error(self, token: Token):
        self.errors.append(Error(
            "MISSING IDENTIFIER",
            f"Expected identifier in function declaration, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def no_ident_in_param_error(self, token: Token):
        self.errors.append(Error(
            "MISSING IDENTIFIER",
            f"Expected identifier in parameter, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def no_data_type_indicator_error(self, token: Token):
        self.errors.append(Error(
            "MISSING DASH DATA TYPE",
            f"Expected dash before data type, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def no_data_type_error(self, token: Token):
        self.errors.append(Error(
            "MISSING DATA TYPE",
            f"Expected data type, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def no_dono_error(self, token: Token):
        self.errors.append(Error(
            "MISSING DONO",
            f"Expected 'dono' to denote variable as constant, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def invalid_parameter_error(self, token: Token):
        self.errors.append(Error(
            "INVALID PARAMETER",
            f"Invalid parameter. Expected ',' or ')', got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def invalid_dot_op_error(self, token: Token):
        self.errors.append(Error(
            "INVALID DOT OPERATION",
            f"Invalid dot operation. Expected identifier, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def unterminated_error(self, token: Token):
        self.errors.append(Error(
            "UNTERMINATED STATEMENT",
            f"Expected '~' to terminate the statement, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def unclosed_paren_error(self, token: Token):
        self.errors.append(Error(
            "UNCLOSED PARENTHESIS",
            f"Expected ')' to close the parenthesis, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def unclosed_double_bracket_error(self, token: Token):
        self.errors.append(Error(
            "UNCLOSED DOUBLE BRACKET",
            f"Expected ']]' to close the double bracket, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def unclosed_bracket_error(self, token: Token):
        self.errors.append(Error(
            "UNCLOSED BRACKET",
            f"Expected ']' to close the bracket, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def unclosed_brace_error(self, token: Token):
        self.errors.append(Error(
            "UNCLOSED BRACE",
            f"Expected '}}' to close the brace, got {token.lexeme}.",
            token.position,
            token.end_position
        ))
    def empty_condition_error(self):
        self.errors.append(Error(
            "EMPTY CONDITION",
            f"Conditions cannot be empty.",
            self.curr_tok.position,
            self.curr_tok.end_position
        ))
    def empty_code_body_error(self):
        self.errors.append(Error(
            "EMPTY CODE BODY",
            f"Code bodies must contain at least one or more statement.",
            self.curr_tok.position,
            self.curr_tok.end_position
        ))
    def uninitialized_assignment_error(self, token: Token):
        self.errors.append(Error(
            "MISSING VALUE ASSIGNMENT",
            f"Assignments must have a value after '='. got '{token.lexeme}'.",
            token.position,
            token.end_position
        ))
    def unclosed_string_part_error(self, string_start, token: Token):
        self.errors.append(Error(
            "UNCLOSED FORMAT STRING",
            f"Unclosed string part. . Expected '{string_start.lexeme[:-1]}|' to be enclosed, got '{token.lexeme}'.",
            token.position,
            token.end_position
        ))
    def invalid_mainuwu_rtype_error(self, token: Token):
        self.errors.append(Error(
            "INVALID MAINUWU FUNCTION",
            f"The mainuwu function's return type must only be 'san', got '{token}'.",
            token.position,
            token.end_position
        ))
    def invalid_mainuwu_params_error(self, token: Token):
        self.errors.append(Error(
            "INVALID MAINUWU FUNCTION",
            f"Expected ')', got '{token}'.\n\tThe mainuwu function cannot accept any parameters.",
            token.position,
            token.end_position
        ))
    def multiple_mainuwu_error(self, token: Token):
        self.errors.append(Error(
            "MULTIPLE MAINUWU FUNCTION",
            f"The program must only have one mainuwu function. Got 'mainuwu'",
            token.position,
            token.end_position
        ))
    def missing_mainuwu_error(self, token: Token):
        self.errors.append(Error(
            "MISSING MAINUWU FUNCTION",
            f"The program must have at least one mainuwu function. Got 'EOF'",
            token.position,
            token.end_position
        ))
