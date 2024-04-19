from enum import Enum
from src.parser.productions import ArrayLiteral, ReturnStatement, Value
from src.lexer.token import Token, TokenType
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

class NonFunctionIdCall:
    def __init__(self, original: Token, called: Token):
        self.original = original
        self.called = called

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

class FunctionAssignmentError:
    def __init__(self, original: Token, assignment: Token):
        self.original = original
        self.assignment = assignment

    def __str__(self):
        index_str = str(self.original.position[0] + 1)
        assign_index = str(self.assignment.position[0] + 1)
        max_pad = max(len(index_str), len(assign_index))
        border = f"\t{'_' * (len(ErrorSrc.src[self.original.position[0]]) + len(str(self.original.position[0] + 1)) + max_pad)}\n"
        og_range = 1 if self.original.end_position is None else self.original.end_position[1] - self.original.position[1] + 1
        error_range = 1 if self.assignment.end_position is None else self.assignment.end_position[1] - self.assignment.position[1] + 1

        msg = f"Tried to assign a value to a function: {self.assignment}\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            f'Original function definition',
            color=AnsiColor.GREEN)
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.original.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.original.position[1]}{'^' * (og_range)}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.original.position[1])}|\n"
        msg += f"\t{' ' * max_pad} | |\n"

        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            f"'{self.original}()' is a function and cannot be assigned to",
            color=AnsiColor.RED)
        msg += f"\t{assign_index:{max_pad}} | |{ErrorSrc.src[self.assignment.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * self.assignment.position[1]}{'^' * (error_range)}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * (self.assignment.position[1])}|\n"
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

class ReassignedConstantError:
    'errors that include two tokens'
    def __init__(self, token: Token, defined_token: Token,
                 header: str, token_msg: str):
        self.token = token
        self.defined_token = defined_token
        self.header = header
        self.msg = token_msg

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

class ReturnTypeMismatchError:
    def __init__(self, expected: Token, return_stmt: ReturnStatement, actual_type: TokenType) -> None:
        self.expected = expected
        self.return_stmt = return_stmt
        self.actual_type = actual_type

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

class TypeMismatchError:
    def __init__(self, expected: Token, actual_val: Value, actual_type: TokenType, assignment: bool) -> None:
        self.expected = expected
        self.actual_val = actual_val
        self.actual_type = actual_type
        self.assignment = assignment # if false, its an assignment, if true, its a declaration

    def __str__(self):
        index_str = str(self.expected.position[0] + 1)
        max_pad = max(len(index_str), 3)
        border = f"\t{'_' * (len(ErrorSrc.src[self.expected.position[0]]) + len(str(self.expected.position[0] + 1)) + max_pad)}\n"

        msg = f"{'Assignment' if self.assignment else 'Declaration'} Type Mismatch: expected '{self.expected.flat_string()}' but got '{self.actual_type.flat_string()}'\n"
        msg += border

        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            f"Expected type defined here",
            color=AnsiColor.GREEN,
        )
        msg += f"\t{index_str:{max_pad}} | {ErrorSrc.src[self.expected.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | {' ' * self.expected.position[1]}{'^' * (len(self.expected.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | {'_' * (self.expected.position[1])}|\n"

        msg += f"\t{' ' * max_pad} | |\t"
        msg += Styled.sprintln(
            f"Tried to assign a value that evaluates to type: '{self.actual_type.flat_string()}'",
            color=AnsiColor.RED
        )
        msg += f"\t{'rhs':{max_pad}} | |    {self.actual_val.flat_string()}\n"
        msg += f"\t{' ' * max_pad} | |{' ' * 4}{'^' * (len(self.actual_val.flat_string()))}\n"
        msg += f"\t{' ' * max_pad} | |{'_' * 4}|\n"

        msg += border
        return msg

class PrePostFixOperandError:
    def __init__(self, op: Token, val: Value, val_definition: Token|None, val_type: TokenType, header: str, postfix=False) -> None:
        self.op = op
        self.val = val
        self.val_definition = val_definition
        self.val_type = val_type
        self.header = header
        self.postfix = postfix

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

class InfixOperandError:
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
        if self.left_definition:
            lhs_index = str(self.left_definition.position[0] + 1)
            msg += f"\n\t{' ' * max_pad} | \t"
            msg += Styled.sprintln(
                f"Left hand side defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{lhs_index:{max_pad}} | {ErrorSrc.src[self.left_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.left_definition.position[1]}{'^' * (len(self.left_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.left_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |"
        if self.left_type:
            msg += f"\n\t{' ' * max_pad} | "f"{'|' if self.left_definition else ''}""\t"
            msg += Styled.sprintln(
                f"Value below evaluates to type: '{self.left_type.flat_string()}'",
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
        if self.right_definition:
            rhs_index = str(self.right_definition.position[0] + 1)
            msg += f"\n\t{' ' * max_pad} | \t"
            msg += Styled.sprintln(
                f"Right hand side defined here",
                color=AnsiColor.GREEN,
            )
            msg += f"\t{rhs_index:{max_pad}} | {ErrorSrc.src[self.right_definition.position[0]]}\n"
            msg += f"\t{' ' * max_pad} | {' ' * self.right_definition.position[1]}{'^' * (len(self.right_definition.flat_string()))}\n"
            msg += f"\t{' ' * max_pad} | {'_' * (self.right_definition.position[1])}|\n"
            msg += f"\t{' ' * max_pad} | |"
        if self.right_type:
            msg += f"\n\t{' ' * max_pad} | " f"{'|' if self.right_definition else ''}" "\t"
            msg += Styled.sprintln(
                f"Value below evaluates to type: '{self.right_type.flat_string()}'",
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

class NonIterableIndexingError:
    def __init__(self, token: Token, type_definition: Token, token_type: TokenType, usage: str) -> None:
        self.token = token
        self.type_definition = type_definition
        self.token_type = token_type
        self.usage = usage

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

class NonClassAccessError:
    def __init__(self, id: Token, id_definition: Token|None, usage: str) -> None:
        self.id = id
        self.id_definition = id_definition
        self.usage = usage

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
        msg += Styled.sprintln(
            f"Tried to do an access using a non class" f" of type: '{self.id_definition.token}'" if self.id_definition else "",
            color=AnsiColor.RED
        )

        msg += f"\t{id_index:{max_pad}} | " f"{'|' if self.id_definition else ' '}" f"{ErrorSrc.src[self.id.position[0]]}\n"
        msg += f"\t{' ' * max_pad} | " f"{'|' if self.id_definition else ' '}" f"{' ' * self.id.position[1]}{'^' * (len(self.id.flat_string()))}\n"
        if self.id_definition:
            msg += f"\t{' ' * max_pad} | |{'_' * (self.id.position[1])}|\n"

        msg += border
        return msg

class UndefinedClassMember:
    def __init__(self, cwass: str, property: Token, member_type: GlobalType,
                 actual_definition: tuple[Token|None, GlobalType|None]=(None, None)) -> None:
        self.cwass = cwass
        self.property = property
        self.member_type = member_type
        self.actual_definition, self.actual_type = actual_definition

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

class MismatchedCallArgType:
    def __init__(self, global_type: GlobalType, call_str: str, id: Token, id_definition: Token|None,
                 expected_types: list[Token], args: list[Value], actual_types: list[TokenType], matches: list[bool]
                 ) -> None:
        self.global_type = global_type
        self.call_str = call_str
        self.id = id
        self.id_definition = id_definition
        self.expected_types = expected_types
        self.args = args
        self.actual_types = actual_types
        self.matches = matches

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
        max_type_pad = 4 + len(AnsiColor.RED.value)*2
        if self.expected_types:
            max_type_pad += max(len(expected.flat_string()) for expected in self.expected_types)
        msg += f"\t{' ' * max_pad} |\t"
        msg += f'{Styled.sprint("EXPECTED", color=AnsiColor.CYAN):{max_type_pad}} '
        msg += f'{Styled.sprint("ACTUAL", color=AnsiColor.CYAN):{max_type_pad+2}}'
        msg += f'{Styled.sprint("ARG", color=AnsiColor.CYAN)}\n'
        for expected, actual, arg, matched in zip(self.expected_types, self.actual_types, self.args, self.matches):
            color = AnsiColor.GREEN if matched else AnsiColor.RED
            res = '✓' if matched else '✗'
            msg += f"\t{' ' * max_pad} |\t" + (
                f"{Styled.sprint(res, expected.flat_string(), color=color):{max_type_pad}} {Styled.sprint('(', actual.flat_string(), ')', color=color):{max_type_pad+2}}"+
                Styled.sprint(arg.flat_string(), color=color)+
                "\n"
            )
        if len(self.expected_types) != len(self.actual_types):
            msg += f"\t{' ' * max_pad} |\n"
            msg += f"\t{' ' * max_pad} |\t"
            expected_len, actual_len = len(self.expected_types), len(self.actual_types)
            if expected_len > actual_len:
                msg += Styled.sprintln(
                    f"{expected_len - actual_len} {'arg' if expected_len - actual_len == 1 else 'args'} missing",
                    color=AnsiColor.RED
                )
                for i in range(len(self.actual_types), len(self.expected_types)):
                    msg += f"\t{' ' * max_pad} |\t" + (
                        f"{Styled.sprint('✗', self.expected_types[i].flat_string(), color=AnsiColor.RED):{max_type_pad}} {Styled.sprint('(', 'MISSING', ')', color=AnsiColor.RED):{max_type_pad+2}}\n"
                    )
            elif actual_len > expected_len:
                msg += Styled.sprintln(
                    f"{actual_len - expected_len} {'arg' if actual_len - expected_len == 1 else 'args'} too many",
                    color=AnsiColor.RED
                )
                for i in range(len(self.expected_types), len(self.actual_types)):
                    msg += f"\t{' ' * max_pad} |\t" + (
                        f"{Styled.sprint('✗', 'NONE', color=AnsiColor.RED):{max_type_pad}} {Styled.sprint('(', self.actual_types[i].flat_string(), ')', color=AnsiColor.RED):{max_type_pad+2}}"
                        f"{Styled.sprint(self.args[i].flat_string(), color=AnsiColor.RED)}\n"
                    )
        msg += border
        return msg

class HeterogeneousArrayError:
    def __init__(self, arr: ArrayLiteral, vals: list[Value], types: list[TokenType]):
        self.arr = arr
        self.vals = vals
        self.types = types

    def __str__(self):
        max_pad = 3
        max_len = len(self.arr.flat_string())
        border = f"\t{'_' * (max_len + 3 + max_pad)}\n"

        msg = f"Heterogeneous Array:\n"
        msg += border
        msg += f"\t{' ' * max_pad} | \t"
        msg += Styled.sprintln(
            f"Array contains {len(set(self.types))} unit types: {', '.join([t.token for t in set(self.types)])}",
            color=AnsiColor.RED
        )
        msg += f"\t{' ' * max_pad} | \t{self.arr.flat_string()}\n"

        msg += f"\t{' ' * max_pad} |\n"
        curr_type = None
        max_type_pad = max(len(dtype.token) for dtype in set(self.types))
        colors = AnsiColor.colors_iter()
        for val, dtype in zip(self.vals, self.types):
            msg += f"\t{' ' * max_pad} |\t"
            if curr_type is None:
                curr_type = dtype
                msg += Styled.sprint(
                    f"{dtype.token:{max_type_pad}}",
                    color=next(colors)
                )
            elif curr_type != dtype:
                curr_type = dtype
                msg += Styled.sprint(
                    f"{dtype.token:{max_type_pad}}",
                    color=next(colors)
                )
            msg += Styled.sprintln(
                f"\t{val.flat_string():{max_type_pad}}",
            )
        msg += border
        return msg

