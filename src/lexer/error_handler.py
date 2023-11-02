from .token import TokenType


class Error:
    def __init__(self, token_type: TokenType, position: tuple[int], temp_id: str, actual_delim: str,
                 fatal=False):
        self.token_type = token_type
        self.position = position
        self.temp_id = temp_id
        self.actual_delim = actual_delim

        self.error_type = f"UNTERMINATED {self.token_type.token.replace('_', ' ')}" if not fatal else "FATAL"
        self.expected_delims = token_type.expected_delims

    def __str__(self):
        log = ""

        log += f"[{self.error_type}] Error on line {self.position[0]} column {self.position[1]}:\n"
        log += f"\texpected any of these characters: "

        for delim in self.expected_delims:
            delim = delim if delim != " " else "WHITESPACE"
            log += f"{delim} "
        log += f"\n\tafter {self.temp_id} but got {self.actual_delim if self.actual_delim != ' ' else 'WHITESPACE'} instead\n"

        return log
