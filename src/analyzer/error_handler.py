from enum import Enum
from src.parser.productions import ClassAccessor, FnCall, IndexedIdentifier, ReturnStatement, Value
from src.lexer.token import Token, TokenType
from src.style import AnsiColor, Styled

class GlobalType(Enum):
    def __init__(self, name):
        self._name = name
    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name
    IDENTIFIER = "IDENTIFIER"
    FUNCTION = "FUNCTION"
    CLASS = "CLASS"
    CLASS_PROPERTY = "CLASS_PROPERTY"
    CLASS_METHOD = "CLASS_METHOD"
    LOCAL_CLASS_ID = "LOCAL_CLASS_ID"

class ErrorSrc:
    src = [""]

class DuplicateDefinitionError:
    def __init__(self, original: Token, original_type: GlobalType, duplicate: Token, duplicate_type: GlobalType):
        self.original = original
        self.duplicate = duplicate
        self.original_type = original_type
        self.duplicate_type = duplicate_type

    def __str__(self):
        index_str = str(self.original.position[0] + 1)
        dupe_index = str(self.duplicate.position[0] + 1)
        max_pad = max(len(index_str), len(dupe_index))
        border = f"\t{'_' * (len(ErrorSrc.src[self.original.position[0]]) + len(str(self.original.position[0] + 1)) + max_pad)}\n"
        og_range = 1 if self.original.end_position is None else self.original.end_position[1] - self.original.position[1] + 1
        error_range = 1 if self.duplicate.end_position is None else self.duplicate.end_position[1] - self.duplicate.position[1] + 1

        msg = f"Duplicate {self.original_type}: {self.duplicate}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            f'Original {self.original_type} definition',
            color=AnsiColor.RED)
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            f'tried to redefine as', ('another ' if self.duplicate_type == self.original_type else '') + self.duplicate_type.name,
            color=AnsiColor.RED)
        msg += f"\t{dupe_index} | |{ErrorSrc.src[self.duplicate.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.duplicate.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.duplicate.position[1])}|\n"
        msg += border

        return msg

class UndefinedError:
    def __init__(self, token: Token, gtype: GlobalType) -> None:
        self.token = token
        self.gtype = gtype

    def __str__(self):
        index_str = str(self.token.position[0] + 1)
        max_pad = len(index_str)
        border = f"\t{'_' * (len(ErrorSrc.src[self.token.position[0]]) + len(str(self.token.position[0] + 1)) + max_pad)}\n"
        error_range = 1 if self.token.end_position is None else self.token.end_position[1] - self.token.position[1] + 1

        msg = f"Undefined {self.gtype}: {self.token}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            'Undefined identifier',
            color=AnsiColor.RED)
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.token.position[1]}{'^' * (error_range)}\n"
        msg += border
        return msg

class GenericTwoTokenError:
    'errors that include two tokens'
    def __init__(self, token: Token, defined_token: Token,
                 header: str, token_msg: str, defined_msg: str):
        self.token = token
        self.defined_token = defined_token
        self.header = header
        self.msg = token_msg
        self.defined_msg = defined_msg

    def __str__(self):
        index_str = str(self.token.position[0] + 1)
        defined_index = str(self.defined_token.position[0] + 1)
        max_pad = max(len(index_str), len(defined_index))
        border = f"\t{'_' * (len(ErrorSrc.src[self.token.position[0]]) + len(str(self.token.position[0] + 1)) + max_pad)}\n"
        defined_range = 1 if self.defined_token.end_position is None else self.defined_token.end_position[1] - self.defined_token.position[1] + 1
        error_range = 1 if self.token.end_position is None else self.token.end_position[1] - self.token.position[1] + 1

        msg = f"{self.header}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            self.defined_msg,
            color=AnsiColor.RED
        )
        msg += f"\t{defined_index:{max_pad}} | {ErrorSrc.src[self.defined_token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.defined_token.position[1]}{'^' * (defined_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.defined_token.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            self.msg,
            color=AnsiColor.RED
        )
        msg += f"\t{index_str:{max_pad}} | |{ErrorSrc.src[self.token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.token.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.token.position[1])}|\n"
        msg += border

        return msg

class ReturnTypeMismatchError:
    def __init__(self, expected: Token, return_stmt: ReturnStatement, actual_type: TokenType, expected_msg: str) -> None:
        self.expected = expected
        self.return_stmt = return_stmt
        self.actual_type = actual_type
        self.expected_msg = expected_msg

    def __str__(self):
        expected_index = str(self.expected.position[0] + 1)
        max_pad = max(len(expected_index), 3)
        expected_pad = len(ErrorSrc.src[self.expected.position[0]]) + max_pad + 3
        actual_pad = 17 + len(self.return_stmt.expr.flat_string()) + max_pad
        border = f"\t{'_' * max(expected_pad, actual_pad)}\n"

        msg = f"Return Type Mismatch: expected '{self.expected.flat_string()}' but got '{self.actual_type.flat_string()}'\n"
        msg += border

        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            self.expected_msg,
            color=AnsiColor.RED
        )
        msg += f"\t{expected_index:{max_pad}} | {ErrorSrc.src[self.expected.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.expected.position[1]}{'^' * (len(self.expected.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.expected.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            f"Value below evaluates to type: '{self.actual_type.flat_string()}'",
            color=AnsiColor.RED
        )
        msg += f"\t{'ret':{max_pad}} | |    wetuwn({self.return_stmt.expr.flat_string()})~\n"
        msg += f"\t{' ' * max_pad} | |{' ' * 11}{'^' * (len(self.return_stmt.expr.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * 11}|\n"

        msg += border
        return msg
