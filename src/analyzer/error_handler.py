from enum import Enum
from src.parser.productions import *
from src.lexer.token import Token, TokenType, UniqueTokenType
from src.style import AnsiColor, Styled

class GlobalType(Enum):
    def __init__(self, name):
        self._name = name
    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name
    IDENTIFIER = "identifier"
    FUNCTION = "function"
    CLASS = "class"
    CLASS_PROPERTY = "class property"
    CLASS_METHOD = "class method"
    LOCAL_CLASS_ID = "local class identifier"

class ErrorSrc:
    src = [""]

# base abstract class for all error types
class SemanticError:
    @abstractmethod
    def __str__(self) -> str: ...
    @abstractmethod
    def position(self) -> tuple[int, int]|None: ...
    @abstractmethod
    def string(self) -> str: ...

class DuplicateDefinitionError(SemanticError):
    def __init__(self, original: Token, original_type: GlobalType, duplicate: Token, duplicate_type: GlobalType):
        self.original = original
        self.duplicate = duplicate
        self.original_type = original_type
        self.duplicate_type = duplicate_type

    def position(self) -> tuple[int, int]|None:
        return self.duplicate.position

    def string(self) -> str:
        index_str = str(self.original.position[0] + 1)
        dupe_index = str(self.duplicate.position[0] + 1)
        max_pad = max(len(index_str), len(dupe_index))
        border = f"\t{'_' * (len(ErrorSrc.src[self.original.position[0]]) + len(str(self.original.position[0] + 1)) + max_pad)}\n"
        og_range = 1 if self.original.end_position is None else self.original.end_position[1] - self.original.position[1] + 1
        error_range = 1 if self.duplicate.end_position is None else self.duplicate.end_position[1] - self.duplicate.position[1] + 1
        msg = f"Duplicate {self.original_type}: {self.duplicate}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += f'Original {self.original_type} definition'
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | |\ttried to redefine as {('another ' if self.duplicate_type == self.original_type else '')} {self.duplicate_type}"
        msg += f"\t{dupe_index:{max_pad}} | |{ErrorSrc.src[self.duplicate.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.duplicate.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.duplicate.position[1])}|\n"
        msg += border
        return msg

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
            color=AnsiColor.GREEN)
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            f"tried to redefine as {('another ' if self.duplicate_type == self.original_type else '')} {self.duplicate_type}",
            color=AnsiColor.RED)
        msg += f"\t{dupe_index:{max_pad}} | |{ErrorSrc.src[self.duplicate.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.duplicate.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.duplicate.position[1])}|\n"
        msg += border

        return msg

class NonFunctionIdCall(SemanticError):
    def __init__(self, original: Token, called: Token):
        self.original = original
        self.called = called

    def position(self) -> tuple[int, int]|None:
        return self.called.position

    def string(self) -> str:
        index_str = str(self.original.position[0] + 1)
        dupe_index = str(self.called.position[0] + 1)
        max_pad = max(len(index_str), len(dupe_index))
        border = f"\t{'_' * (len(ErrorSrc.src[self.original.position[0]]) + len(str(self.original.position[0] + 1)) + max_pad)}\n"
        og_range = 1 if self.original.end_position is None else self.original.end_position[1] - self.original.position[1] + 1
        error_range = 1 if self.called.end_position is None else self.called.end_position[1] - self.called.position[1] + 1
        msg = f"Non Function Called: {self.called}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += f'Original identifier definition'
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | |\t"
        msg += f"Tried to call '{self.called}' as a function"
        msg += f"\t{dupe_index:{max_pad}} | |{ErrorSrc.src[self.called.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.called.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.called.position[1])}|\n"
        msg += border
        return msg

    def __str__(self):
        index_str = str(self.original.position[0] + 1)
        dupe_index = str(self.called.position[0] + 1)
        max_pad = max(len(index_str), len(dupe_index))
        border = f"\t{'_' * (len(ErrorSrc.src[self.original.position[0]]) + len(str(self.original.position[0] + 1)) + max_pad)}\n"
        og_range = 1 if self.original.end_position is None else self.original.end_position[1] - self.original.position[1] + 1
        error_range = 1 if self.called.end_position is None else self.called.end_position[1] - self.called.position[1] + 1

        msg = f"Non Function Called: {self.called}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            f'Original identifier definition',
            color=AnsiColor.GREEN)
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            f"Tried to call '{self.called}' as a function",
            color=AnsiColor.RED)
        msg += f"\t{dupe_index:{max_pad}} | |{ErrorSrc.src[self.called.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.called.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.called.position[1])}|\n"
        msg += border
        return msg

class FunctionAssignmentError(SemanticError):
    def __init__(self, original: Token|None, assignment: Token, class_signature: str|None = None):
        self.original = original
        self.assignment = assignment
        self.class_signature = class_signature

    def position(self) -> tuple[int, int]|None:
        return self.assignment.position

    def string(self) -> str:
        index_str = str(self.original.position[0] + 1) if self.original else ""
        assign_index = str(self.assignment.position[0] + 1)
        max_pad = max(len(index_str), len(assign_index))
        max_len = max((len(ErrorSrc.src[self.original.position[0]] if self.original else ''), len(ErrorSrc.src[self.assignment.position[0]])))
        border = f"\t{'_' * ( max_len + 4 + max_pad)}\n"
        if self.original:
            og_range = 1 if self.original.end_position is None else self.original.end_position[1] - self.original.position[1] + 1
        else:
            og_range = 0
        error_range = 1 if self.assignment.end_position is None else self.assignment.end_position[1] - self.assignment.position[1] + 1
        global_type = 'function' if not self.class_signature else 'method'
        name = f"{self.assignment}()" if not self.class_signature else f"{self.class_signature}()"

        msg = f"Tried to assign a value to a {global_type}: {name}\n"
        msg += border
        if self.original:
            msg += f"\t{' ' * max_pad} | \t"
            msg += f'Original {global_type} definition'
            msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | {'|' if self.original else ''}\t"
        msg += f"'{name}' is a {global_type} and cannot be assigned to"
        msg += f"\t{assign_index:{max_pad}} | {'|' if self.original else ''}{ErrorSrc.src[self.assignment.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {'|' if self.original else ''}{' ' * self.assignment.position[1]}{'^' * (error_range)}\n"
        if self.original:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.assignment.position[1])}|\n"
        msg += border
        return msg

    def __str__(self):
        index_str = str(self.original.position[0] + 1) if self.original else ""
        assign_index = str(self.assignment.position[0] + 1)
        max_pad = max(len(index_str), len(assign_index))
        max_len = max((len(ErrorSrc.src[self.original.position[0]] if self.original else ''), len(ErrorSrc.src[self.assignment.position[0]])))
        border = f"\t{'_' * ( max_len + 4 + max_pad)}\n"
        if self.original:
            og_range = 1 if self.original.end_position is None else self.original.end_position[1] - self.original.position[1] + 1
        else:
            og_range = 0
        error_range = 1 if self.assignment.end_position is None else self.assignment.end_position[1] - self.assignment.position[1] + 1
        global_type = 'function' if not self.class_signature else 'method'
        name = f"{self.assignment}()" if not self.class_signature else f"{self.class_signature}()"

        msg = f"Tried to assign a value to a {global_type}: {name}\n"
        msg += border
        if self.original:
            msg += f"\t{' ' * max_pad} | \t"
            msg += Styled.sprintln(
                f'Original {global_type} definition',
                color=AnsiColor.GREEN)
            msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | {'|' if self.original else ''}\t"
        msg += Styled.sprintln(
            f"'{name}' is a {global_type} and cannot be assigned to",
            color=AnsiColor.RED)
        msg += f"\t{assign_index:{max_pad}} | {'|' if self.original else ''}{ErrorSrc.src[self.assignment.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {'|' if self.original else ''}{' ' * self.assignment.position[1]}{'^' * (error_range)}\n"
        if self.original:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.assignment.position[1])}|\n"
        msg += border
        return msg

class UndefinedError(SemanticError):
    def __init__(self, token: Token, gtype: GlobalType) -> None:
        self.token = token
        self.gtype = gtype

    def position(self) -> tuple[int, int]|None:
        return self.token.position

    def string(self) -> str:
        index_str = str(self.token.position[0] + 1)
        max_pad = len(index_str)
        border = f"\t{'_' * (len(ErrorSrc.src[self.token.position[0]]) + len(str(self.token.position[0] + 1)) + max_pad)}\n"
        error_range = 1 if self.token.end_position is None else self.token.end_position[1] - self.token.position[1] + 1
        msg = f"Undefined {self.gtype}: {self.token}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg +='Undefined identifier'
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.token.position[1]}{'^' * (error_range)}\n"
        msg += border
        return msg

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

class ReassignedConstantError:
    'errors that include two tokens'
    def __init__(self, token: Token, defined_token: Token,
                 header: str, token_msg: str):
        self.token = token
        self.defined_token = defined_token
        self.header = header
        self.msg = token_msg

    def position(self) -> tuple[int, int]|None:
        return self.token.position

    def string(self) -> str:
        index_str = str(self.token.position[0] + 1)
        defined_index = str(self.defined_token.position[0] + 1)
        max_pad = max(len(index_str), len(defined_index))
        max_len = len(max(ErrorSrc.src[self.token.position[0]], ErrorSrc.src[self.defined_token.position[0]], key=len))
        border = f"\t{'_' * (max_len + max_pad + 4)}\n"
        defined_range = 1 if self.defined_token.end_position is None else self.defined_token.end_position[1] - self.defined_token.position[1] + 1
        error_range = 1 if self.token.end_position is None else self.token.end_position[1] - self.token.position[1] + 1
        msg = f"{self.header}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg +="Defined as constant here"
        msg += f"\t{defined_index:{max_pad}} | {ErrorSrc.src[self.defined_token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.defined_token.position[1]}{'^' * (defined_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.defined_token.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | |\t"
        msg += self.msg
        msg += f"\t{index_str:{max_pad}} | |{ErrorSrc.src[self.token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.token.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.token.position[1])}|\n"
        msg += border
        return msg

    def __str__(self):
        index_str = str(self.token.position[0] + 1)
        defined_index = str(self.defined_token.position[0] + 1)
        max_pad = max(len(index_str), len(defined_index))
        max_len = len(max(ErrorSrc.src[self.token.position[0]], ErrorSrc.src[self.defined_token.position[0]], key=len))
        border = f"\t{'_' * (max_len + max_pad + 4)}\n"
        defined_range = 1 if self.defined_token.end_position is None else self.defined_token.end_position[1] - self.defined_token.position[1] + 1
        error_range = 1 if self.token.end_position is None else self.token.end_position[1] - self.token.position[1] + 1

        msg = f"{self.header}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            "Defined as constant here",
            color=AnsiColor.GREEN
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

class ReturnTypeMismatchError(SemanticError):
    def __init__(self, expected: Token, return_stmt: ReturnStatement, actual_type: TokenType) -> None:
        self.expected = expected
        self.return_stmt = return_stmt
        self.actual_type = actual_type

    def position(self) -> tuple[int, int]|None:
        return self.expected.position

    def string(self) -> str:
        expected_index = str(self.expected.position[0] + 1)
        max_pad = max(len(expected_index), 3)
        expected_pad = len(ErrorSrc.src[self.expected.position[0]]) + max_pad + 3
        actual_pad = 17 + len(self.return_stmt.expr.flat_string()) + max_pad
        border = f"\t{'_' * max(expected_pad, actual_pad)}\n"
        msg = f"Return Type Mismatch: expected '{self.expected.flat_string()}' but got '{self.actual_type.flat_string()}'\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += f"Expected return type: '{self.expected}'"
        msg += f"\t{expected_index:{max_pad}} | {ErrorSrc.src[self.expected.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.expected.position[1]}{'^' * (len(self.expected.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.expected.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | |\t"
        msg += f"Value below evaluates to type: '{self.actual_type.flat_string()}'"
        msg += f"\t{'ret':{max_pad}} | |    wetuwn({self.return_stmt.expr.flat_string()})~\n"
        msg += f"\t{' ' * max_pad} | |{' ' * 11}{'^' * (len(self.return_stmt.expr.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * 11}|\n"
        msg += border
        return msg

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
            f"Expected return type: '{self.expected}'",
            color=AnsiColor.GREEN,
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

class TypeMismatchError(SemanticError):
    def __init__(self, expected: Token, actual_val: Value, actual_type: TokenType,
                 context: Assignment|Declaration, title: str) -> None:
        self.expected = expected
        self.actual_val = actual_val
        self.actual_type = actual_type
        self.context = context
        self.title = title # if None, its a declaration, if true, its an assignment

    def position(self) -> tuple[int, int]|None:
        return extract_id(self.context.id).position

    def string(self) -> str:
        index_str = str(self.expected.position[0] + 1)
        assign_index_str = (str(extract_id(self.context.id).position[0] + 1) + '..n') if self.title else 'rhs'
        max_pad = max(len(index_str), len(assign_index_str))
        border = f"\t{'_' * (len(ErrorSrc.src[self.expected.position[0]]) + len(str(self.expected.position[0] + 1)) + max_pad)}\n"
        msg = f"{self.title} Type Mismatch: expected '{self.expected.flat_string()}' but got '{self.actual_type.flat_string()}'\n"
        msg += border
        msg += f"\t{' ' * max_pad} |    "
        msg += f"Expected type defined here"
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.expected.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.expected.position[1]}{'^' * (len(self.expected.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.expected.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |  "
        msg += f"Tried to assign a value that evaluates to type: '{self.actual_type.flat_string()}'"
        ctx_str = f"{self.context.id}{f'-{self.context.dtype}' if self.title == 'Declaration' else ''} = "
        msg += f"\t{assign_index_str:{max_pad}} | |    {ctx_str}{self.actual_val.flat_string()}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * (4 + len(ctx_str))}{'^' * (len(self.actual_val.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (4 + len(ctx_str))}|\n"
        msg += border
        return msg

    def __str__(self):
        index_str = str(self.expected.position[0] + 1)
        assign_index_str = (str(extract_id(self.context.id).position[0] + 1) + '..n') if self.title else 'rhs'
        max_pad = max(len(index_str), len(assign_index_str))
        border = f"\t{'_' * (len(ErrorSrc.src[self.expected.position[0]]) + len(str(self.expected.position[0] + 1)) + max_pad)}\n"

        msg = f"{self.title} Type Mismatch: expected '{self.expected.flat_string()}' but got '{self.actual_type.flat_string()}'\n"
        msg += border

        msg += f"\t{' ' * max_pad} |    "
        msg += Styled.sprintln(
            f"Expected type defined here",
            color=AnsiColor.GREEN,
        )
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.expected.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.expected.position[1]}{'^' * (len(self.expected.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.expected.position[1])}|\n"

        msg += f"\t{' ' * max_pad} | |  "
        msg += Styled.sprintln(
            f"Tried to assign a value that evaluates to type: '{self.actual_type.flat_string()}'",
            color=AnsiColor.RED
        )
        ctx_str = f"{self.context.id}{f'-{self.context.dtype}' if self.title == 'Declaration' else ''} = "
        msg += f"\t{assign_index_str:{max_pad}} | |    {ctx_str}{self.actual_val.flat_string()}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * (4 + len(ctx_str))}{'^' * (len(self.actual_val.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (4 + len(ctx_str))}|\n"

        msg += border
        return msg

class PrePostFixOperandError(SemanticError):
    def __init__(self, op: Token, val: Value, val_definition: Token|None, val_type: TokenType, header: str, postfix=False) -> None:
        self.op = op
        self.val = val
        self.val_definition = val_definition
        self.val_type = val_type
        self.header = header
        self.postfix = postfix

    def position(self) -> tuple[int, int]|None:
        return None

    def string(self) -> str:
        op_index = str(self.op.position[0] + 1)
        def_index = str(self.val_definition.position[0] if self.val_definition else 0 + 1)
        max_pad = max(len(op_index), len(def_index))
        max_len = max(len(ErrorSrc.src[self.val_definition.position[0]]) if self.val_definition else 0 + max_pad + 3, len(self.val.flat_string()) + 7 + max_pad)
        border = f"\t{'_' * max_len}\n"
        msg = f"Non-Math {'Prefix' if not self.postfix else 'Postfix'} Operator: '{self.val.flat_string()}'\n"
        msg += border
        if self.val_definition:
            msg += f"\t{' ' * max_pad} | \t"
            msg += f"Expected type defined here"
            msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.val_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.val_definition.position[1]}{'^' * (len(self.val_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.val_definition.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.val_definition else ''}" "\t"
        msg += f"Value below evaluates to type: '{self.val_type.flat_string()}'"
        msg += f"\t{op_index:{max_pad}} | " f"{'|' if self.val_definition else ''}" f"  {self.op.flat_string() if not self.postfix else ''}{self.val.flat_string()}{self.op.flat_string() if self.postfix else ''}\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.val_definition else ''}" f"{' ' * (3 if not self.postfix else 2)}{'^' * (len(self.val.flat_string()))}\n"
        if self.val_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (3 if not self.postfix else 2)}|\n"
        msg += border
        return msg

    def __str__(self):
        op_index = str(self.op.position[0] + 1)
        def_index = str(self.val_definition.position[0] if self.val_definition else 0 + 1)
        max_pad = max(len(op_index), len(def_index))
        max_len = max(len(ErrorSrc.src[self.val_definition.position[0]]) if self.val_definition else 0 + max_pad + 3, len(self.val.flat_string()) + 7 + max_pad)
        border = f"\t{'_' * max_len}\n"

        msg = f"Non-Math {'Prefix' if not self.postfix else 'Postfix'} Operator: '{self.val.flat_string()}'\n"
        msg += border

        if self.val_definition:
            msg += f"\t{' ' * max_pad} | \t"
            msg += Styled.sprintln(
                f"Expected type defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.val_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.val_definition.position[1]}{'^' * (len(self.val_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.val_definition.position[1])}|\n"

        msg += f"\t{' ' * max_pad} | " f"{'|' if self.val_definition else ''}" "\t"
        msg += Styled.sprintln(
            f"Value below evaluates to type: '{self.val_type.flat_string()}'",
            color=AnsiColor.RED
        )
        msg += f"\t{op_index:{max_pad}} | " f"{'|' if self.val_definition else ''}" f"  {self.op.flat_string() if not self.postfix else ''}{self.val.flat_string()}{self.op.flat_string() if self.postfix else ''}\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.val_definition else ''}" f"{' ' * (3 if not self.postfix else 2)}{'^' * (len(self.val.flat_string()))}\n"
        if self.val_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (3 if not self.postfix else 2)}|\n"
        msg += border
        return msg

class InfixOperandError(SemanticError):
    def __init__(self, op: Token, left: tuple[Value, Token|None], 
                 right: tuple[Value, Token|None],
                 left_type: TokenType|None, right_type: TokenType|None,
                 header: str) -> None:
        self.op = op
        self.left, self.left_definition = left
        self.right, self.right_definition = right
        self.left_type = left_type
        self.right_type = right_type
        self.header = header

    def position(self) -> tuple[int, int]|None:
        return None

    def string(self) -> str:
        op_str = str(self.op.position[0] + 1)
        expr_len = 5 + len(self.left.flat_string()) + len(self.op.flat_string()) + len(self.right.flat_string())
        left_def_len = (3 + len(ErrorSrc.src[self.left_definition.position[0]])) if self.left_definition else 0
        right_def_len = (3 + len(ErrorSrc.src[self.right_definition.position[0]])) if self.right_definition else 0
        max_len = max(expr_len, left_def_len, right_def_len)
        max_pad = max(len(op_str), len(str(self.left_definition.position[0])) if self.left_definition else 0,
                      len(str(self.right_definition.position[0])) if self.right_definition else 0)
        border = f"\t{'_' * (max_len + max_pad)}"
        q = "'" # because f-strings lmao
        msg = (self.header + ': '
               f'{(q + self.left.flat_string() + q + " ") if self.left_type else ""}'
               f'{(q + self.right.flat_string() + q) if self.right_type else ""}'
               "\n")
        msg += border
        if self.left_definition and self.left_type:
            lhs_index = str(self.left_definition.position[0] + 1)
            msg += f"\n\t{' ' * max_pad} | \t"
            msg += f"Left value defined here"
            msg += f"\t{lhs_index:{max_pad}} | {ErrorSrc.src[self.left_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.left_definition.position[1]}{'^' * (len(self.left_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.left_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |"
        if self.left_type:
            msg += f"\n\t{' ' * max_pad} | "f"{'|' if self.left_definition else ''}""\t"
            msg += f"Left value evaluates to type: '{self.left_type.flat_string()}'"
            msg += f"\t{op_str:{max_pad}} | " f"{'|' if self.left_definition else ''}" f"  {self.left.flat_string()}{self.op.flat_string()}{self.right.flat_string()}\n"
            msg += f"\t{' ' * max_pad} | " f"{'|' if self.left_definition else ''}" f"  {'^' * (len(self.left.flat_string()))}"
            if self.left_definition:
                msg += f"\n\t{' ' * max_pad} | |__|\n"
            else:
                msg += '\n'
        if self.left_type and self.right_type:
            msg += f"\t{' ' * max_pad} |"
        if self.right_definition and self.right_type:
            rhs_index = str(self.right_definition.position[0] + 1)
            msg += f"\n\t{' ' * max_pad} | \t"
            msg += f"Right value defined here"
            msg += f"\t{rhs_index:{max_pad}} | {ErrorSrc.src[self.right_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.right_definition.position[1]}{'^' * (len(self.right_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.right_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |"
        if self.right_type:
            msg += f"\n\t{' ' * max_pad} | " f"{'|' if self.right_definition else ''}" "\t"
            msg += f"Right value evaluates to type: '{self.right_type.flat_string()}'"
            msg += f"\t{op_str:{max_pad}} | " f"{'|' if self.right_definition else ''}" f"  {self.left.flat_string()}{self.op.flat_string()}{self.right.flat_string()}\n"
            msg += f"\t{' ' * max_pad} | " f"{'|' if self.right_definition else ''}" f"  {' ' * (len(self.left.flat_string()) + len(self.op.flat_string()))}{'^' * (len(self.right.flat_string()))}"
            if self.right_definition:
                msg += f"\n\t{' ' * max_pad} | |__"f"{'_' * (1+len(self.left.flat_string()))}|\n"
            else:
                msg += '\n'
        msg += border + '\n'
        return msg

    def __str__(self):
        op_str = str(self.op.position[0] + 1)
        expr_len = 5 + len(self.left.flat_string()) + len(self.op.flat_string()) + len(self.right.flat_string())
        left_def_len = (3 + len(ErrorSrc.src[self.left_definition.position[0]])) if self.left_definition else 0
        right_def_len = (3 + len(ErrorSrc.src[self.right_definition.position[0]])) if self.right_definition else 0
        max_len = max(expr_len, left_def_len, right_def_len)
        max_pad = max(len(op_str), len(str(self.left_definition.position[0])) if self.left_definition else 0,
                      len(str(self.right_definition.position[0])) if self.right_definition else 0)
        border = f"\t{'_' * (max_len + max_pad)}"

        q = "'" # because f-strings lmao
        msg = (self.header + ': '
               f'{(q + self.left.flat_string() + q + " ") if self.left_type else ""}'
               f'{(q + self.right.flat_string() + q) if self.right_type else ""}'
               "\n")
        msg += border
        if self.left_definition and self.left_type:
            lhs_index = str(self.left_definition.position[0] + 1)
            msg += f"\n\t{' ' * max_pad} | \t"
            msg += Styled.sprintln(
                f"Left value defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{lhs_index:{max_pad}} | {ErrorSrc.src[self.left_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.left_definition.position[1]}{'^' * (len(self.left_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.left_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |"
        if self.left_type:
            msg += f"\n\t{' ' * max_pad} | "f"{'|' if self.left_definition else ''}""\t"
            msg += Styled.sprintln(
                f"Left value evaluates to type: '{self.left_type.flat_string()}'",
                color=AnsiColor.RED
            )
            msg += f"\t{op_str:{max_pad}} | " f"{'|' if self.left_definition else ''}" f"  {self.left.flat_string()}{self.op.flat_string()}{self.right.flat_string()}\n"
            msg += f"\t{' ' * max_pad} | " f"{'|' if self.left_definition else ''}" f"  {'^' * (len(self.left.flat_string()))}"
            if self.left_definition:
                msg += f"\n\t{' ' * max_pad} | |__|\n"
            else:
                msg += '\n'
        if self.left_type and self.right_type:
            msg += f"\t{' ' * max_pad} |"
        if self.right_definition and self.right_type:
            rhs_index = str(self.right_definition.position[0] + 1)
            msg += f"\n\t{' ' * max_pad} | \t"
            msg += Styled.sprintln(
                f"Right value defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{rhs_index:{max_pad}} | {ErrorSrc.src[self.right_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.right_definition.position[1]}{'^' * (len(self.right_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.right_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |"
        if self.right_type:
            msg += f"\n\t{' ' * max_pad} | " f"{'|' if self.right_definition else ''}" "\t"
            msg += Styled.sprintln(
                f"Right value evaluates to type: '{self.right_type.flat_string()}'",
                color=AnsiColor.RED
            )
            msg += f"\t{op_str:{max_pad}} | " f"{'|' if self.right_definition else ''}" f"  {self.left.flat_string()}{self.op.flat_string()}{self.right.flat_string()}\n"
            msg += f"\t{' ' * max_pad} | " f"{'|' if self.right_definition else ''}" f"  {' ' * (len(self.left.flat_string()) + len(self.op.flat_string()))}{'^' * (len(self.right.flat_string()))}"
            if self.right_definition:
                msg += f"\n\t{' ' * max_pad} | |__"f"{'_' * (1+len(self.left.flat_string()))}|\n"
            else:
                msg += '\n'
        msg += border + '\n'
        return msg

class NonIterableIndexingError(SemanticError):
    def __init__(self, token: Token, type_definition: Token, token_type: TokenType, usage: str) -> None:
        self.token = token
        self.type_definition = type_definition
        self.token_type = token_type
        self.usage = usage

    def position(self) -> tuple[int, int]|None:
        return self.token.position

    def string(self) -> str:
        tok_index = str(self.token.position[0] + 1)
        def_index = str(self.type_definition.position[0] + 1)
        max_pad = max(len(tok_index), len(def_index))
        max_len = max(len(ErrorSrc.src[self.token.position[0]]), len(ErrorSrc.src[self.type_definition.position[0]]))
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"
        msg = f"Non Iterable Indexing: '{self.usage}'\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += f"Actual type defined here"
        msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.type_definition.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.type_definition.position[1]}{'^' * (len(self.type_definition.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.type_definition.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | |\t"
        msg += f"Tried to index into a non iterable of type: '{self.token_type}'"
        msg += f"\t{tok_index:{max_pad}} | |{ErrorSrc.src[self.token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.token.position[1]}{'^' * (len(self.token.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.token.position[1])}|\n"
        msg += border
        return msg

    def __str__(self):
        tok_index = str(self.token.position[0] + 1)
        def_index = str(self.type_definition.position[0] + 1)
        max_pad = max(len(tok_index), len(def_index))
        max_len = max(len(ErrorSrc.src[self.token.position[0]]), len(ErrorSrc.src[self.type_definition.position[0]]))
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"

        msg = f"Non Iterable Indexing: '{self.usage}'\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            f"Actual type defined here",
            color=AnsiColor.GREEN,
        )
        msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.type_definition.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.type_definition.position[1]}{'^' * (len(self.type_definition.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.type_definition.position[1])}|\n"

        msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            f"Tried to index into a non iterable of type: '{self.token_type}'",
            color=AnsiColor.RED
        )
        msg += f"\t{tok_index:{max_pad}} | |{ErrorSrc.src[self.token.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.token.position[1]}{'^' * (len(self.token.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.token.position[1])}|\n"

        msg += border
        return msg

class NonClassAccessError(SemanticError):
    def __init__(self, id: Token, id_definition: Token|None, usage: str, initialized=True) -> None:
        self.id = id
        self.id_definition = id_definition
        self.usage = usage
        self.initialized = initialized

    def position(self) -> tuple[int, int]|None:
        return self.id.position

    def string(self) -> str:
        id_index = str(self.id.position[0] + 1)
        def_index = str(self.id_definition.position[0] + 1) if self.id_definition else "0"
        max_pad = max(len(id_index), len(def_index))
        max_len = max(len(ErrorSrc.src[self.id.position[0]]), len(ErrorSrc.src[self.id_definition.position[0]]) if self.id_definition else 0)
        border = f"\t{'_' * (max_len + 4 + max_pad)}\n"
        msg = f"Non Class Access: '{self.usage}'\n"
        msg += border
        if self.id_definition:
            msg += f"\t{' ' * max_pad} | \t"
            msg += f"Actual type defined here"
            msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.id_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.id_definition.position[1]}{'^' * (len(self.id_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.id_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.id_definition else ''}" "\t"
        if self.initialized:
            msg += f"Tried to do an access using a non class" f" of type: '{self.id_definition.token}'" if self.id_definition else ""
        else:
            msg += f"Tried to do an access using an uninitialized " f"'{self.id_definition.token}'" if self.id_definition else "variable/constant"
        msg += f"\t{id_index:{max_pad}} | " f"{'|' if self.id_definition else ' '}" f"{ErrorSrc.src[self.id.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.id_definition else ' '}" f"{' ' * self.id.position[1]}{'^' * (len(self.id.flat_string()))}\n"
        if self.id_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.id.position[1])}|\n"
        msg += border
        return msg

    def __str__(self):
        id_index = str(self.id.position[0] + 1)
        def_index = str(self.id_definition.position[0] + 1) if self.id_definition else "0"
        max_pad = max(len(id_index), len(def_index))
        max_len = max(len(ErrorSrc.src[self.id.position[0]]), len(ErrorSrc.src[self.id_definition.position[0]]) if self.id_definition else 0)
        border = f"\t{'_' * (max_len + 4 + max_pad)}\n"

        msg = f"Non Class Access: '{self.usage}'\n"
        msg += border
        if self.id_definition:
            msg += f"\t{' ' * max_pad} | \t"
            msg += Styled.sprintln(
                f"Actual type defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.id_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.id_definition.position[1]}{'^' * (len(self.id_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.id_definition.position[1])}|\n"

            msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | " f"{'|' if self.id_definition else ''}" "\t"
        if self.initialized:
            msg += Styled.sprintln(
                f"Tried to do an access using a non class" f" of type: '{self.id_definition.token}'" if self.id_definition else "",
                color=AnsiColor.RED
            )
        else:
            msg += Styled.sprintln(
                f"Tried to do an access using an uninitialized " f"'{self.id_definition.token}'" if self.id_definition else "variable/constant",
                color=AnsiColor.RED
            )

        msg += f"\t{id_index:{max_pad}} | " f"{'|' if self.id_definition else ' '}" f"{ErrorSrc.src[self.id.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.id_definition else ' '}" f"{' ' * self.id.position[1]}{'^' * (len(self.id.flat_string()))}\n"
        if self.id_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.id.position[1])}|\n"

        msg += border
        return msg

class UndefinedClassMember(SemanticError):
    def __init__(self, cwass: str, property: Token, member_type: GlobalType,
                 actual_definition: tuple[Token|None, GlobalType|None]=(None, None)) -> None:
        self.cwass = cwass
        self.property = property
        self.member_type = member_type
        self.actual_definition, self.actual_type = actual_definition

    def position(self) -> tuple[int, int]|None:
        return self.property.position

    def string(self) -> str:
        property_index = str(self.property.position[0] + 1)
        max_pad = len(property_index)
        border = f"\t{'_' * (max_pad + 4 + len(ErrorSrc.src[self.property.position[0]]))}\n"
        msg = f"Undefined {self.member_type} of '{self.cwass}': '{self.property.flat_string()}'\n"
        msg += border
        if self.actual_type and self.actual_definition:
            msg += f"\t{' ' * max_pad} |\t"
            msg += f"'{self.property.flat_string()}' is a {self.actual_type} of '{self.cwass}' defined here"
            msg += f"\t{str(self.actual_definition.position[0] + 1):{max_pad}} | {ErrorSrc.src[self.actual_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.actual_definition.position[1]}{'^' * (len(self.actual_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.actual_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.actual_type else ''}" "\t"
        msg += f"'{self.property.flat_string()}' is not a {self.member_type} of '{self.cwass}'"
        msg += f"\t{property_index:{max_pad}} | " f"{'|' if self.actual_type else ''}" f"{ErrorSrc.src[self.property.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.actual_type else ''}" f"{' ' * self.property.position[1]}{'^' * (len(self.property.flat_string()))}\n"
        if self.actual_type and self.actual_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.property.position[1])}|\n"
        msg += border
        return msg

    def __str__(self):
        property_index = str(self.property.position[0] + 1)
        max_pad = len(property_index)
        border = f"\t{'_' * (max_pad + 4 + len(ErrorSrc.src[self.property.position[0]]))}\n"

        msg = f"Undefined {self.member_type} of '{self.cwass}': '{self.property.flat_string()}'\n"
        msg += border
        if self.actual_type and self.actual_definition:
            msg += f"\t{' ' * max_pad} |\t"
            msg += Styled.sprintln(
                f"'{self.property.flat_string()}' is a {self.actual_type} of '{self.cwass}' defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{str(self.actual_definition.position[0] + 1):{max_pad}} | {ErrorSrc.src[self.actual_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.actual_definition.position[1]}{'^' * (len(self.actual_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.actual_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | " f"{'|' if self.actual_type else ''}" "\t"
        msg += Styled.sprintln(
            f"'{self.property.flat_string()}' is not a {self.member_type} of '{self.cwass}'",
            color=AnsiColor.RED
        )
        msg += f"\t{property_index:{max_pad}} | " f"{'|' if self.actual_type else ''}" f"{ErrorSrc.src[self.property.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.actual_type else ''}" f"{' ' * self.property.position[1]}{'^' * (len(self.property.flat_string()))}\n"
        if self.actual_type and self.actual_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.property.position[1])}|\n"
        msg += border
        return msg

class MismatchedCallArgType(SemanticError):
    def __init__(self, global_type: GlobalType, call_str: str, id: Token, id_definition: Token|None,
                 expected_types: list[str], args: list[Value], actual_types: list[TokenType], matches: list[bool]
                 ) -> None:
        self.global_type = global_type
        self.call_str = call_str
        self.id = id
        self.id_definition = id_definition
        self.expected_types = expected_types
        self.args = args
        self.actual_types = actual_types
        self.matches = matches

    def position(self) -> tuple[int, int]|None:
        return self.id.position

    def string(self) -> str:
        id_index = str(self.id.position[0] + 1)
        def_index = str(self.id_definition.position[0] + 1) if self.id_definition else ""
        max_pad = max(len(id_index), len(def_index))
        max_len = max([len(arg.flat_string()) for arg in self.args] + [len(ErrorSrc.src[self.id.position[0]]), len(ErrorSrc.src[self.id_definition.position[0]]) if self.id_definition else 0])
        border = f"\t{'_' * (max_pad + 4 + max_len)}\n"

        msg = f"Call arg type mismatch:\n"
        msg += border
        if self.id_definition:
            msg += f"\t{' ' * max_pad} |\t"
            msg += f"'{self.call_str}()' {self.global_type} defined here"
            msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.id_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.id_definition.position[1]}{'^' * (len(self.id_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.id_definition.position[1])}|\n"

        msg += f"\t{' ' * max_pad} | {'|' if self.id_definition else ''}\n"
        msg += f"\t{' ' * max_pad} | {'|' if self.id_definition else ''}\t"
        msg += f"'{self.call_str}()' called here"
        msg += f"\t{id_index:{max_pad}} | {'|' if self.id_definition else ''}{ErrorSrc.src[self.id.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {'|' if self.id_definition else ''}{' ' * self.id.position[1]}{'^' * (len(self.id.flat_string()))}\n"
        if self.id_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.id.position[1])}|\n"
        msg += f"\t{' ' * max_pad} |\n"
        msg += f"\t{' ' * max_pad} |\t"

        msg += (
            f"'{self.call_str}()' {self.global_type} expects {len(self.expected_types)} {'argument' if len(self.expected_types) == 1 else 'arguments'}"+
            (f" but was called with {len(self.args)}" if len(self.expected_types) != len(self.actual_types) else "")
        )
        expected_pad = actual_pad = 4
        if self.expected_types:
            expected_pad += max(max(len(expected) for expected in self.expected_types), 8)
        if self.actual_types:
            actual_pad += max(max(len(actual.flat_string()) for actual in self.actual_types), 6)

        msg += f"\t{' ' * max_pad} |\t"
        msg += f'{"EXPECTED":{expected_pad-1}} '
        msg += f'{"ACTUAL":{actual_pad-1}} '
        msg += f'{"ARG"}\n'

        for expected, actual, arg, matched in zip(self.expected_types, self.actual_types, self.args, self.matches):
            color = AnsiColor.GREEN if matched else AnsiColor.RED
            res = '✓' if matched else '✗'
            msg += f"\t{' ' * max_pad} |\t" + (
                f"{res} {expected}{actual.flat_string():{actual_pad}}"+
                Styled.sprint(arg.flat_string(), color=color)+
                "\n"
            )
        if len(self.expected_types) != len(self.args):
            msg += f"\t{' ' * max_pad} |\n"
            msg += f"\t{' ' * max_pad} |\t"
            expected_len, actual_len = len(self.expected_types), len(self.args)
            if expected_len > actual_len:
                msg += Styled.sprintln(
                    f"{expected_len - actual_len} {'arg' if expected_len - actual_len == 1 else 'args'} missing",
                    color=AnsiColor.RED
                )
                for i in range(len(self.actual_types), len(self.expected_types)):
                    msg += f"\t{' ' * max_pad} |\t" + (
                        f"{Styled.sprint('✗', self.expected_types[i], color=AnsiColor.RED):{expected_pad}} {Styled.sprint('(', 'MISSING', ')', color=AnsiColor.RED):{actual_pad}}\n"
                    )
            elif actual_len > expected_len:
                msg += Styled.sprintln(
                    f"{actual_len - expected_len} {'arg' if actual_len - expected_len == 1 else 'args'} too many",
                    color=AnsiColor.RED
                )
                for i in range(len(self.expected_types), len(self.args)):
                    msg += f"\t{' ' * max_pad} |\t" + (
                        f"{Styled.sprint('✗', 'NONE', color=AnsiColor.RED):{expected_pad}} {Styled.sprint('(', self.args[i].flat_string(), ')', color=AnsiColor.RED):{actual_pad}}"
                        f"{Styled.sprint(self.args[i].flat_string(), color=AnsiColor.RED)}\n"
                    )
        msg += border
        return msg

    def __str__(self):
        id_index = str(self.id.position[0] + 1)
        def_index = str(self.id_definition.position[0] + 1) if self.id_definition else ""
        max_pad = max(len(id_index), len(def_index))
        max_len = max([len(arg.flat_string()) for arg in self.args] + [len(ErrorSrc.src[self.id.position[0]]), len(ErrorSrc.src[self.id_definition.position[0]]) if self.id_definition else 0])
        border = f"\t{'_' * (max_pad + 4 + max_len)}\n"

        msg = f"Call arg type mismatch:\n"
        msg += border
        if self.id_definition:
            msg += f"\t{' ' * max_pad} |\t"
            msg += Styled.sprintln(
                f"'{self.call_str}()' {self.global_type} defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{def_index:{max_pad}} | {ErrorSrc.src[self.id_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.id_definition.position[1]}{'^' * (len(self.id_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.id_definition.position[1])}|\n"

        msg += f"\t{' ' * max_pad} | {'|' if self.id_definition else ''}\n"
        msg += f"\t{' ' * max_pad} | {'|' if self.id_definition else ''}\t"
        msg += Styled.sprintln(
            f"'{self.call_str}()' called here",
            color=AnsiColor.RED
        )
        msg += f"\t{id_index:{max_pad}} | {'|' if self.id_definition else ''}{ErrorSrc.src[self.id.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {'|' if self.id_definition else ''}{' ' * self.id.position[1]}{'^' * (len(self.id.flat_string()))}\n"
        if self.id_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.id.position[1])}|\n"
        msg += f"\t{' ' * max_pad} |\n"
        msg += f"\t{' ' * max_pad} |\t"

        msg += Styled.sprintln(
            f"'{self.call_str}()' {self.global_type} expects {len(self.expected_types)} {'argument' if len(self.expected_types) == 1 else 'arguments'}"+
            (f" but was called with {len(self.args)}" if len(self.expected_types) != len(self.actual_types) else ""),
            color=AnsiColor.CYAN
        )
        expected_pad = actual_pad = 4 + len(AnsiColor.RED.value)*2
        if self.expected_types:
            expected_pad += max(max(len(expected) for expected in self.expected_types), 8)
        if self.actual_types:
            actual_pad += max(max(len(actual.flat_string()) for actual in self.actual_types), 6)

        msg += f"\t{' ' * max_pad} |\t"
        msg += f'{Styled.sprint("EXPECTED", color=AnsiColor.CYAN):{expected_pad-1}} '
        msg += f'{Styled.sprint("ACTUAL", color=AnsiColor.CYAN):{actual_pad-1}} '
        msg += f'{Styled.sprint("ARG", color=AnsiColor.CYAN)}\n'

        for expected, actual, arg, matched in zip(self.expected_types, self.actual_types, self.args, self.matches):
            color = AnsiColor.GREEN if matched else AnsiColor.RED
            res = '✓' if matched else '✗'
            msg += f"\t{' ' * max_pad} |\t" + (
                f"{Styled.sprint(res, expected, color=color):{expected_pad}}{Styled.sprint(actual.flat_string(), color=color):{actual_pad}}"+
                Styled.sprint(arg.flat_string(), color=color)+
                "\n"
            )
        if len(self.expected_types) != len(self.args):
            msg += f"\t{' ' * max_pad} |\n"
            msg += f"\t{' ' * max_pad} |\t"
            expected_len, actual_len = len(self.expected_types), len(self.args)
            if expected_len > actual_len:
                msg += Styled.sprintln(
                    f"{expected_len - actual_len} {'arg' if expected_len - actual_len == 1 else 'args'} missing",
                    color=AnsiColor.RED
                )
                for i in range(len(self.actual_types), len(self.expected_types)):
                    msg += f"\t{' ' * max_pad} |\t" + (
                        f"{Styled.sprint('✗', self.expected_types[i], color=AnsiColor.RED):{expected_pad}} {Styled.sprint('(', 'MISSING', ')', color=AnsiColor.RED):{actual_pad}}\n"
                    )
            elif actual_len > expected_len:
                msg += Styled.sprintln(
                    f"{actual_len - expected_len} {'arg' if actual_len - expected_len == 1 else 'args'} too many",
                    color=AnsiColor.RED
                )
                for i in range(len(self.expected_types), len(self.args)):
                    msg += f"\t{' ' * max_pad} |\t" + (
                        f"{Styled.sprint('✗', 'NONE', color=AnsiColor.RED):{expected_pad}} {Styled.sprint('(', self.args[i].flat_string(), ')', color=AnsiColor.RED):{actual_pad}}"
                        f"{Styled.sprint(self.args[i].flat_string(), color=AnsiColor.RED)}\n"
                    )
        msg += border
        return msg

class HeterogeneousArrayError(SemanticError):
    def __init__(self, arr: ArrayLiteral, vals: list[Value], types: list[str]):
        self.arr = arr
        self.vals = vals
        self.types = types

    def position(self) -> tuple[int, int] | None:
        return None

    def string(self) -> str:
        max_pad = 3
        max_len = len(self.arr.flat_string())
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"
        msg = f"Heterogeneous Array:\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += f"Array contains {len(set(self.types))} unit types: {', '.join([t for t in set(self.types)])}"
        msg += f"\t{' ' * max_pad} | \t{self.arr.flat_string()}\n"
        msg += f"\t{' ' * max_pad} |\n"
        curr_type = None
        max_type_pad = max(len(dtype) for dtype in set(self.types))
        for val, dtype in zip(self.vals, self.types):
            msg += f"\t{' ' * max_pad} |\t"
            if curr_type is None:
                msg += f"{dtype:{max_type_pad}}"
            elif curr_type != dtype:
                msg += f"{dtype:{max_type_pad}}"
            msg += f"\t{'':{max_type_pad if curr_type == dtype else 0}}{val.flat_string():{max_type_pad}}"
            curr_type = dtype
        msg += border
        return msg

    def __str__(self):
        max_pad = 3
        max_len = len(self.arr.flat_string())
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"

        msg = f"Heterogeneous Array:\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            f"Array contains {len(set(self.types))} unit types: {', '.join([t for t in set(self.types)])}",
            color=AnsiColor.RED
        )
        msg += f"\t{' ' * max_pad} | \t{self.arr.flat_string()}\n"

        msg += f"\t{' ' * max_pad} |\n"
        curr_type = None
        max_type_pad = max(len(dtype) for dtype in set(self.types))
        colors = AnsiColor.colors_iter()
        for val, dtype in zip(self.vals, self.types):
            msg += f"\t{' ' * max_pad} |\t"
            if curr_type is None:
                msg += Styled.sprint(
                    f"{dtype:{max_type_pad}}",
                    color=next(colors)
                )
            elif curr_type != dtype:
                msg += Styled.sprint(
                    f"{dtype:{max_type_pad}}",
                    color=next(colors)
                )
            msg += Styled.sprintln(
                f"\t{'':{max_type_pad if curr_type == dtype else 0}}{val.flat_string():{max_type_pad}}",
            )
            curr_type = dtype
        msg += border
        return msg

class NoReturnStatement(SemanticError):
    def __init__(self, func: Function, cwass:str|None=None):
        self.func = func
        self.cwass = cwass

    def position(self) -> tuple[int, int] | None:
        return self.func.id.position

    def strign(self) -> str:
        last_stmt = final_statement(self.func.body) + 1
        rtype_index_str = str(self.func.rtype.position[0] + 1)
        max_pad = max(len(rtype_index_str), 4)
        max_len = max(len(ErrorSrc.src[self.func.rtype.position[0]]), len(ErrorSrc.src[last_stmt-1]))
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"
        name = f"{'Function' if not self.cwass else 'Method'}"
        msg = f"{name} '{self.func.id.flat_string() if not self.cwass else (self.cwass+'.'+self.func.id.flat_string())}()' has no return statement:\n"
        msg += border
        msg += f"\t{' ' * max_pad} |\t"
        msg += f"{name}s that don't have return statements implicitly retuwn 'nuww'."
        msg += f"\t{' ' * max_pad} |\t"
        msg += "Return type defined here"
        msg += f"\t{rtype_index_str:{max_pad}} | {ErrorSrc.src[self.func.rtype.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.func.rtype.position[1]}{'^' * (len(self.func.rtype.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} |\t"
        msg += f"Consider adding a return statement somewhere"
        msg += f"\t{' ' * max_pad} |\t"
        msg += f"like after the statement in line {last_stmt}"
        default_return = default_rtype(self.func.rtype.token)
        msg += f"\t{last_stmt:<{max_pad}} |\t\t{ErrorSrc.src[last_stmt-1].strip()}\n"
        msg += f"\t{f'...n':<{max_pad}} |\t\twetuwn({default_return})~\n"
        msg += f"\t{' ' * max_pad} |\t\t^^^^^^^^^{'^' * len(default_return)}\n"
        msg += border
        return msg

    def __str__(self):
        last_stmt = final_statement(self.func.body) + 1
        rtype_index_str = str(self.func.rtype.position[0] + 1)
        max_pad = max(len(rtype_index_str), 4)
        max_len = max(len(ErrorSrc.src[self.func.rtype.position[0]]), len(ErrorSrc.src[last_stmt-1]))
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"
        name = f"{'Function' if not self.cwass else 'Method'}"

        msg = f"{name} '{self.func.id.flat_string() if not self.cwass else (self.cwass+'.'+self.func.id.flat_string())}()' has no return statement:\n"
        msg += border

        msg += f"\t{' ' * max_pad} |\t"
        msg += Styled.sprintln(
            f"{name}s that don't have return statements implicitly retuwn 'nuww'.",
            color=AnsiColor.GREEN
        )
        msg += f"\t{' ' * max_pad} |\t"
        msg += Styled.sprintln(
            "Return type defined here",
            color=AnsiColor.GREEN
        )
        msg += f"\t{rtype_index_str:{max_pad}} | {ErrorSrc.src[self.func.rtype.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.func.rtype.position[1]}{'^' * (len(self.func.rtype.flat_string()))}\n"

        msg += f"\t{' ' * max_pad} |\t"
        msg += Styled.sprintln(
            f"Consider adding a return statement somewhere",
            color=AnsiColor.CYAN
        )
        msg += f"\t{' ' * max_pad} |\t"
        msg += Styled.sprintln(
            f"like after the statement in line {last_stmt}",
            color=AnsiColor.CYAN
        )
        default_return = default_rtype(self.func.rtype.token)
        msg += f"\t{last_stmt:<{max_pad}} |\t\t{ErrorSrc.src[last_stmt-1].strip()}\n"
        msg += f"\t{f'...n':<{max_pad}} |\t\twetuwn({default_return})~\n"
        msg += f"\t{' ' * max_pad} |\t\t^^^^^^^^^{'^' * len(default_return)}\n"
        msg += border
        return msg

class NonNumberIndex:
    def __init__(self, indexed_id: IndexedIdentifier, indices: list[Value], actual_types: list[TokenType], ok: list[bool] ) -> None:
        self.indexed_id = indexed_id
        self.indices = indices
        self.actual_types = actual_types
        self.ok = ok

    def __str__(self) -> str:
        indexed_id_token = extract_id(self.indexed_id)
        indexed_id_index = str(indexed_id_token.position[0] + 1)
        max_pad = len(indexed_id_index) + 3
        max_len = len(ErrorSrc.src[indexed_id_token.position[0]])
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"

        msg = f"Non Number Indexing: '{self.indexed_id.flat_string()}'\n"
        msg += border
        msg += f"\t{' ' * max_pad} |    "
        context = "Not all indices are a number type" if len(self.indexed_id.index) > 1 else f"Index '{self.indexed_id.index[0].flat_string()}' is not a number type"
        msg += Styled.sprintln(
            context,
            color=AnsiColor.RED
        )
        msg += f"\t{indexed_id_index:{max_pad}} |    {self.indexed_id.flat_string()}\n"
        msg += f"\t{' ' * max_pad} |\n"
        dtype_pad = max([len(dtype.flat_string()) for dtype in self.actual_types]) + 5
        msg += f"\t{' ' * max_pad} |    "
        msg += Styled.sprintln(f'{"TYPE":<{dtype_pad}}INDEX', color=AnsiColor.CYAN)

        for index, dtype, ok in zip(self.indices, self.actual_types, self.ok):
            res = '✓' if ok else '✗'
            msg += f"\t{' ' * max_pad} |    "
            msg += Styled.sprintln(
                f"{res} {dtype.flat_string():{dtype_pad}}{index.flat_string()}",
                color=AnsiColor.GREEN if ok else AnsiColor.RED
            )
        msg += border
        return msg

### HELPER FUNCTIONS FOR SUGGESTIONS
def extract_id(accessor: Token | FnCall | IndexedIdentifier | ClassAccessor) -> Token:
    'gets the very first id of a class accessor'
    match accessor:
        case Token():
            return accessor
        case FnCall():
            return accessor.id
        case IndexedIdentifier():
            match accessor.id:
                case Token():
                    return accessor.id
                case FnCall():
                    return accessor.id.id
                case _:
                    raise ValueError(f"Unknown class accessor: {accessor}")
        case ClassAccessor():
            return extract_id(accessor.id)
        case _:
            raise ValueError(f"Unknown class accessor: {accessor}")
def final_statement(body: BlockStatement) -> int:
    stmt: Statement = body.statements[-1]
    match stmt:
        case Print():
            return stmt.print.position[0]
        case Declaration():
            return stmt.id.position[0]
        case Assignment():
            return extract_id(stmt.id).position[0]
        case IfStatement():
            if stmt.else_block.statements:
                return final_statement(stmt.else_block)
            elif stmt.else_if:
                return final_statement(stmt.else_if[-1].then)
            else:
                return final_statement(stmt.then)
        case WhileLoop() | ForLoop():
            return final_statement(stmt.body)
        case _:
            raise ValueError(f"Unknown statement: {stmt}")
def default_rtype(token: TokenType) -> str:
    match token:
        case UniqueTokenType():
            if token.is_arr_type():
                return '{}'
            else:
                return token.token + '()'
        case TokenType.CHAN_ARR | TokenType.KUN_ARR | TokenType.SAMA_ARR | TokenType.SAN_ARR | TokenType.SENPAI_ARR:
            return '{}'
        case TokenType.CHAN:
            return '0'
        case TokenType.KUN:
            return '0.0'
        case TokenType.SAMA:
            return 'cap'
        case TokenType.SENPAI:
            return '""'
        case _:
            raise ValueError(f"Unknown token: {token}")
