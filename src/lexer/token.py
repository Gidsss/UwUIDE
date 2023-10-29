class Token:
    'A class for representing tokens in a lexer'

    def __init__(self, lexeme: str, token: str, position: tuple[int, int], end_position: tuple[int, int]):
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
    def position(self) -> tuple[int,int]:
        return self._position
    
    @position.setter
    def position(self, position: tuple[int,int]):
        self._position = position
    
    @property
    def end_position(self) -> tuple[int,int]:
        return self._end_position
    
    @position.setter
    def end_position(self, end_position: tuple[int,int]):
        self._end_position = end_position