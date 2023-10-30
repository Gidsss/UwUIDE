from constants.constants import DELIMS


class TokenTypes():
    class TokenType:
        def __init__(self, token: str, delim_id: str, error_type=None):
            self.token = token
            self.delim_id = delim_id
            self.error_type = f"UNTERMINATED {self.token.replace('_', ' ')}" if error_type is None else error_type

            self.expected_delims = DELIMS[self.delim_id]

        def __str__(self):
            return self.token

    BWEAK = TokenType("BWEAK_KEYWORD", "end")

    CHAN = TokenType("CHAN_DATA_TYPE", "data_type")

    BOOL_LITERAL = TokenType("BOOLEAN_LITERAL", "bool")

    UNARY_OPERATOR = TokenType("UNARY_OPERATOR", "unary")

    IDENTIFIER = TokenType("IDENTIFIER", "id")


class Token:
    'A class for representing tokens in a lexer'

    def __init__(self, lexeme: str, token: TokenTypes, position: tuple[int, int], end_position: tuple[int, int]):
        self._lexeme = lexeme
        self._token = token
        self._position = position
        self._end_position = end_position

    def __repr__(self):
        return f"Token(lexeme='{self.lexeme}', token='{self.token}', position={self.position}, end_position={self.end_position})"

    @property
    def lexeme(self) -> str:
        return self._lexeme

    @lexeme.setter
    def lexeme(self, lexeme: str):
        self._lexeme = lexeme

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    @property
    def position(self) -> tuple[int, int]:
        return self._position

    @position.setter
    def position(self, position: tuple[int, int]):
        self._position = position

    @property
    def end_position(self) -> tuple[int, int]:
        return self._end_position

    @end_position.setter
    def end_position(self, end_position: tuple[int, int]):
        self._end_position = end_position
