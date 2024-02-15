from src.lexer.token import Token, TokenType
from src.parser.productions import *

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = [token for token in tokens if token.token != TokenType.WHITESPACE]
        self.errors: list[str]
        self.pos: int = 0

        self.parse_program()

    @property
    def curr_tok(self) -> Token:
        'returns TokenType.EOF if no more tokens'
        if self.pos >= len(self.tokens):
            return Token("", TokenType.EOF, (0, 0), (0, 0))
        return self.tokens[self.pos]

    @property
    def peek_tok(self) -> Token:
        'returns TokenType.EOF if no more tokens'
        if self.pos + 1 >= len(self.tokens):
            return Token("", TokenType.EOF, (0, 0), (0, 0))
        return self.tokens[self.pos + 1]

    def advance(self) -> int | None:
        'returns none if can not advance'
        if self.pos >= len(self.tokens):
            return None
        self.pos += 1

    def at_EOF(self) -> bool:
        return self.curr_tok.token == TokenType.EOF

    def parse_program(self) -> Program:
        '''
        parse program production

        on a global scope, only function, classes, and variable/constant
        declarations are allowed. expressions are not allowed
        '''
        p = Program()
        while self.curr_tok.token != TokenType.EOF:
            if self.curr_tok.token == TokenType.FWUNC:
                p.fwuncs.append(self.parse_fwunc())

            elif self.curr_tok.token == TokenType.CWASS:
                p.cwass.append(self.parse_cwass())

            elif self.curr_tok.token == TokenType.GWOBAW:
                p.gwobaws.append(self.parse_gwobaw_dec())

            else:
                # TODO: add error messages for unexpected tokens in global scope
                # up to you if you want to be super specific and provide hints
                # based on the token type encountered
                self.advance()

        p.print()
        return p

    def parse_fwunc(self) -> Fwunc:
        '''
        parse fwunc production

        function declaration example:
            fwunc mainuwu-san(name-senpai) [[
                pwint("hewwo |name|!")~
            ]]

        will early return if found EOF
        '''
        f = Fwunc()
        self.advance()
        if self.at_EOF():
            self.errors.append("expected function declaration, got EOF")
            return f

        if self.curr_tok.token.token.startswith("IDENTIFIER"):
            f.id = self.curr_tok
            self.advance()
            if self.at_EOF():
                self.errors.append(f"expected function declaration for {f.id.lexeme}, got EOF")
                return f
        else:
            self.errors.append(f"functions must have an identifier, got '{self.curr_tok.lexeme}'")

        if self.curr_tok.token == TokenType.DASH:
            self.advance()
            if self.at_EOF():
                self.errors.append(f"expected type after '-' for function declaration, got EOF")
                return f
        else:
            self.errors.append(f"functions must have a dash before a type, got '{self.curr_tok.lexeme}'")

        data_types = [
            TokenType.CHAN,
            TokenType.KUN,
            TokenType.SAMA,
            TokenType.SENPAI,
            TokenType.SAN,
            TokenType.DONO,
        ]
        if self.curr_tok.token in data_types:
            f.dtype = self.curr_tok
            self.advance()
            if self.at_EOF():
                self.errors.append(f"expected open parenthesis for function declaration, got EOF")
                return f
        else:
            self.errors.append(f"functions must have a return type, got '{self.curr_tok.lexeme}'")

        if self.curr_tok.token == TokenType.OPEN_PAREN:
            self.advance()
            if self.at_EOF():
                self.errors.append(f"expected a closing parenthesis for function declaration, got EOF")
                return f
        else:
            self.errors.append(f"functions must have an open parenthesis, got '{self.curr_tok.lexeme}'")

        params = self.parse_params()
        f.params = params

        if self.curr_tok.token == TokenType.CLOSE_PAREN:
            self.advance()
            if self.at_EOF():
                self.errors.append(f"expected a double open bracket for function declaration, got EOF")
                return f
        else:
            self.errors.append(f"functions must have a closing parenthesis, got '{self.curr_tok.lexeme}'")

        if self.curr_tok.token == TokenType.DOUBLE_OPEN_BRACKET:
            self.advance()
            if self.at_EOF():
                self.errors.append(f"expected a body for function declaration, got EOF")
                return f
        else:
            self.errors.append(f"functions must have a double open bracket, got '{self.curr_tok.lexeme}'")

        body = self.parse_body()
        f.body = body

        if self.curr_tok.token == TokenType.DOUBLE_CLOSE_BRACKET:
            self.advance()
            if self.at_EOF():
                return f
        else:
            self.errors.append(f"functions must end with a double close bracket, got '{self.curr_tok.lexeme}'")

        return f

    def parse_cwass(self) -> Cwass:
        c = Cwass()
        return c

    def parse_gwobaw_dec(self) -> GwobawDec:
        g = GwobawDec()
        return g

    def parse_params(self) -> list[Token]:
        pass

    def parse_body(self) -> list[Token]:
        pass
