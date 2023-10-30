from enum import Enum
from enum import Enum
from enum import Enum


class TokenTypes(Enum):
    class TokenType:
        def __init__(self, lexeme: str, token: str, delim_id: str, error_type: str):
            self.lexeme = lexeme
            self.token = token
            self.delim_id = delim_id
            self.error_type = error_type

    BWEAK = TokenType(
        "bweak",
        "BWEAK KEYWORD",
        "end",
        "UNTERMINATED BWEAK"
    )


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