from enum import Enum
from src.parser.productions import ClassAccessor, FnCall, IndexedIdentifier, Value
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
