import re
from src.lexer.token import TokenType, UniqueTokenType, class_properties
from src.parser.production_types import *
from src.lexer import Token

### UTILS
def sprint(*val, indent = 0):
    'return string with optional identation'
    return "    " * indent + " ".join(val)
def sprintln(*val, indent = 0):
    'return newline terminated string with optional identation'
    return sprint(*val, indent=indent) + "\n"

### EXPRESSION PRODUCTIONS
class PrefixExpression(Expression):
    def __init__(self):
        self.op: Token = Token()
        self.right: Value = Value()

        self.grouped = False

    def header(self) -> str:
        return self.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.op.flat_string()}{self.right.flat_string()}"
    def python_string(self, indent=0, cwass=False) -> str:
        return f"{self.op.python_string(cwass=cwass)}{self.right.python_string(cwass=cwass)}"
    def formatted_string(self, indent=0) -> str:
        res = f"{self.op.formatted_string()}{self.right.formatted_string()}"
        if self.grouped:
            res = f"({res})"
        return res

    def __len__(self):
        return 1

    @property
    def start_pos(self):
        return self.op.position

    @property
    def end_pos(self):
        return self.right.end_position if isinstance(self.right, Token) else self.right.end_pos

class InfixExpression(Expression):
    def __init__(self):
        self.left: Value = Value()
        self.op: Token = Token()
        self.right: Value = Value()

        self._start_pos = None
        self._end_pos = None

        self.grouped = False

    def header(self):
        return ""
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"left":self.left, "op":self.op, "right":self.right}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f'({self.left.flat_string()} {self.op.flat_string()} {self.right.flat_string()})'
    def python_string(self, indent=0, cwass=False) -> str:
        lhs = self.left.python_string(cwass=cwass)
        op = self.op.python_string(cwass=cwass)
        rhs = self.right.python_string(cwass=cwass)
        if self.op.token in [TokenType.AND_OPERATOR, TokenType.OR_OPERATOR]:
            lhs = f"Bool({lhs})"
            rhs = f"Bool({rhs})"
        return f"({lhs} {op} {rhs})"
    def formatted_string(self, indent=0, spaced=True) -> str:
        lhs = self.left.formatted_string()
        op = self.op.formatted_string()
        rhs = self.right.formatted_string()

        return f"({lhs} {op} {rhs})" if self.grouped else f"{lhs} {op} {rhs}"

    def __len__(self):
        return 1

    @property
    def start_pos(self):
        pos = self.left.position if isinstance(self.left, Token) else self.left.start_pos
        return self._start_pos if self._start_pos else pos

    @property
    def end_pos(self):
        pos = self.right.end_position if isinstance(self.right, Token) else self.right.end_pos
        return self._end_pos if self._end_pos else pos

    @start_pos.setter
    def start_pos(self, value):
        self._start_pos = value

    @end_pos.setter
    def end_pos(self, value):
        self._end_pos = value

class PostfixExpression(Expression):
    def __init__(self):
        self.left: Value = Value()
        self.op: Token = Token()


        self.grouped = False

    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None

    def string(self, indent = 1) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.left.flat_string()}{self.op.flat_string()}"
    def python_string(self, indent=0, cwass=False) -> str:
        return f"({self.left.python_string(cwass=cwass)}{self.op.python_string(cwass=cwass)})"
    def formatted_string(self, indent=0) -> str:
        res = f"{self.left.formatted_string()}{self.op.formatted_string()}"
        if self.grouped:
            res = f"({res})"
        return res

    def __len__(self):
        return 1

    @property
    def start_pos(self):
        return self.left.position if isinstance(self.left, Token) else self.left.start_pos

    @property
    def end_pos(self):
        return self.op.end_position

### LITERAL PRODUCTIONS
class StringLiteral(Iterable):
    def __init__(self, val: Token):
        self.val: Token = val
        self.concats: list[StringFmt | Input | StringLiteral] = []

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None
    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        res = sprint(self.val.flat_string(), *[c.flat_string() for c in self.concats])
        if self.concats:
            res += ' & ' + ' & '.join(c.flat_string() for c in self.concats)
        return res
    def python_string(self, indent=0, cwass=False) -> str:
        res = self.val.python_string(cwass=cwass)
        if self.concats:
            res += ' + ' + ' + '.join(c.python_string(cwass=cwass) for c in self.concats)
        return res

    def formatted_string(self, indent=0) -> str:
        res = self.val.formatted_string()
        if self.concats:
            res += ' & ' + ' & '.join(c.formatted_string() for c in self.concats)

        return res

    def __len__(self):
        return 1

class Input(Iterable):
    def __init__(self):
        self.expr: Value | Token = Value()
        self.concats: list[StringFmt | Input | StringLiteral] = []
        self.stmt: bool = False

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "input:"

    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"expr":self.expr, **{f"concat_{i+1}":c for i,c in enumerate(self.concats)}}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        res = f"inpwt({self.expr.flat_string()})"
        if self.concats:
            res += ' & ' + ' & '.join(c.flat_string() for c in self.concats)
        return res
    def python_string(self, indent=0, cwass=False) -> str:
        res = f"input({self.expr.python_string(cwass=cwass)})"
        if self.concats:
            res += ' + ' + ' + '.join(c.python_string(cwass=cwass) for c in self.concats)
        return sprint(res, indent=indent if self.stmt else 0)

    def formatted_string(self, indent=0) -> str:
        res = f"inpwt({self.expr.formatted_string()})"
        res += "~" if self.stmt else ""
        if self.concats:
            res += ' & ' + ' & '.join(c.formatted_string() for c in self.concats)
        return sprint(res, indent=indent if self.stmt else 0)

    def __len__(self):
        return 1

class StringFmt(Iterable):
    def __init__(self):
        self.start: Token = Token()
        self.mid: list[Token] = []
        self.exprs: list[Value | Token] = []
        self.end: Token = Token()
        self.concats: list[StringFmt | Input | StringLiteral] = []

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "string fmt:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"start":self.start, **{f"mid_{i+1}":m for i,m in enumerate(self.mid_expr_iter())}, "end":self.end, **{f"concat_{i+1}":c for i,c in enumerate(self.concats)}}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        res = f"{self.start.flat_string()}{' '.join(m.flat_string() for m in self.mid_expr_iter())}{self.end.flat_string()}"
        if self.concats:
            res += ' & ' + ' & '.join(c.flat_string() for c in self.concats)
        return res
    def python_string(self, indent=0, cwass=False) -> str:
        res = f"{self.start.python_string(cwass=cwass)}{' '.join(m.python_string(cwass=cwass) for m in self.mid_expr())}{self.end.python_string(cwass=cwass)}"
        if self.concats:
            res += ' + ' + ' + '.join(c.python_string(cwass=cwass) for c in self.concats)
        return res

    def formatted_string(self, indent=0) -> str:
        start = self.start.lexeme[:-1].replace("|", "\|")
        end = self.end.lexeme[1:].replace("|", "\|")
        res = "''"
        res = f"{start}{''.join([c for c in self.mid_expr_uwu(format=True)])}{end}"
        if self.concats:
            res += ' & ' + ' & '.join(c.formatted_string() for c in self.concats)
        return res

    def mid_expr_iter(self):
        if self.exprs:
            yield self.exprs[0]
        for m,e in zip(self.mid, self.exprs[1:]):
            yield m
            yield e
    def mid_expr(self):
        all = []
        if self.exprs:
            all.append(self.exprs[0])
        for m,e in zip(self.mid, self.exprs[1:]):
            all.append(m)
            all.append(e)
        return all
    def mid_expr_uwu(self, format=False) -> list[str]:
        all: list[str] = []
        if self.exprs:
            all.append(f"|{self.exprs[0].formatted_string() if format else self.exprs[0].flat_string()}|")
        for m,e in zip(self.mid, self.exprs[1:]):
            all.append(m.lexeme[1:-1].replace("|", "\|"))
            all.append(f"|{e.formatted_string() if format else e.flat_string()}|")
        return all

    def __len__(self):
        return 1

class ArrayLiteral(Iterable):
    def __init__(self):
        self.elements: list[Value] = []

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "array literal:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {f"item_{i+1}":e for i,e in enumerate(self.elements)}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{{{', '.join(e.flat_string() for e in self.elements)}}}"
    def python_string(self, indent=0, cwass=False) -> str:
        return f"Array([{', '.join(e.python_string(cwass=cwass) for e in self.elements)}])"

    def formatted_string(self, indent=0) -> str:
        if len(self.elements)>0 and isinstance(self.elements[0], ArrayLiteral):
            res = "{\n"
            elems = []
            for elem in self.elements:
                elems.append(elem.formatted_string_multi(indent+1))
            res += ",\n".join(elems) + "\n"
            res += sprint("}", indent=indent+1)
            return res
        return f"{{{', '.join(e.formatted_string() for e in self.elements)}}}"

    def formatted_string_multi(self, indent=0) -> str:
        if len(self.elements)>0 and isinstance(self.elements[0], ArrayLiteral):
            res = sprint("{\n", indent=indent+1)
            elems = []
            for elem in self.elements:
                elems.append(elem.formatted_string_multi(indent+1))
            res += ",\n".join(elems) + "\n"
            res += sprint("}", indent=indent+1)
            return res
        else:
            return sprint(f"{{{', '.join(e.formatted_string() for e in self.elements)}}}", indent=indent+1)

    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)

class FnCall(IdentifierProds):
    def __init__(self):
        self.id: Token = Token()
        self.args: list[Value] = []
        self.need_self = False

        self.start_pos = None
        self.end_pos = None

        self.is_statement = False

    def header(self):
        return sprint("call:", self.id.string(),indent=0)
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {**{f"arg_{i+1}":a for i,a in enumerate(self.args)}}

    def string(self, indent = 0) -> str:
        return self.flat_string(indent) + '\n'
    def flat_string(self, indent = 0) -> str:
        return sprint(f"{self.id.flat_string()}({', '.join(a.flat_string() for a in self.args)})", indent=indent)
    def python_string(self, indent=0, cwass=False) -> str:
        res = ""
        if self.need_self: res += "self."
        return sprint(res + f"{self.id.python_string(cwass=cwass)}({', '.join(a.python_string(cwass=cwass) for a in self.args)})", indent=indent)
    def formatted_string(self, indent=0) -> str:
        tilde  = "~" if self.is_statement else ""
        return sprint(f"{self.id.formatted_string()}({', '.join(a.formatted_string() for a in self.args)}){tilde}", indent=indent)

    def __len__(self):
        return 1

class IndexedIdentifier(IdentifierProds):
    '''
    id can be:
    - token:             ident[i]
    - FnCall:            fn()[i]
    '''
    def __init__(self):
        self.id: Token | FnCall = Token()
        self.index: list[Value] = []

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return self.string()

    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        res = self.id.flat_string()
        for index in self.index:
            res += f"{{{index.flat_string()}}}"
        return res
    def python_string(self, indent=0, cwass=False) -> str:
        res = self.id.python_string(cwass=cwass)
        for index in self.index:
            res += f"[int({index.python_string(cwass=cwass)})]"
        return res
    def formatted_string(self, indent=0) -> str:
        res = self.id.formatted_string()
        for index in self.index:
            res += f"{{{index.formatted_string()}}}"
        return res

class ClassConstructor(IdentifierProds):
    def __init__(self):
        self.id: Token = Token()
        self.args: list[Value] = []

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return sprint("constructor:", self.id.string(),indent=0)
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {**{f"arg_{i+1}":a for i,a in enumerate(self.args)}}

    def string(self, indent = 1) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.id.flat_string()}({', '.join(a.flat_string() for a in self.args)})"
    def python_string(self, indent=0, cwass=False) -> str:
        return f"{self.id.python_string(cwass=cwass)}({', '.join(a.python_string(cwass=cwass) for a in self.args)})"
    def formatted_string(self, indent=0) -> str:
        return f"{self.id.formatted_string()}({', '.join(a.formatted_string() for a in self.args)})"

    def __len__(self):
        return 1

class ClassAccessor(IdentifierProds):
    '''
    id can be:
    - token:    ident.property, Cwass.property
    - FnCall:   fn().property
    - indexed:  ident[index].property
    - ClassAccessor: ident.accessed.property
    can access:
    - token:         ident.property, Cwass.property
    - FnCall:        ident.method(), Cwass.method()
    - indexed:       ident.property[index], Cwass.method()[index]
    - ClassAccessor: ident.property.property, Cwass.property.method()
    '''
    def __init__(self):
        self.id: Token | FnCall | IndexedIdentifier | ClassAccessor = Token()
        self.accessed: Token | FnCall | IndexedIdentifier | ClassAccessor = Token()

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return self.id.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"accessed":self.accessed}

    def string(self, indent = 0) -> str:
        return sprintln("call:", self.flat_string(), indent=indent)
    def flat_string(self) -> str:
        return f"{self.id.flat_string()}.{self.accessed.flat_string()}"
    def python_string(self, indent=0, cwass=False) -> str:
        return sprint(f"{self.id.python_string(cwass=cwass)}.{self.accessed.python_string(cwass=cwass)}", indent=indent)
    def formatted_string(self, indent=0) -> str:
        return sprint(f"{self.id.formatted_string()}.{self.accessed.formatted_string()}", indent=indent)

    def __len__(self):
        return 1


### BLOCK STATEMENT PRODUCTIONS
class ReturnStatement(Statement):
    def __init__(self):
        self.expr: Value = Value()

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "return"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"val":self.expr}

    def string(self, indent = 0) -> str:
        return sprintln("return", self.expr.string(indent), indent=indent)
    def python_string(self, indent=0, cwass=False) -> str:
        return sprint("return", self.expr.python_string(indent, cwass=cwass), indent=indent)
    def formatted_string(self, indent=0) -> str:
        return sprint(f"wetuwn({self.expr.formatted_string()})~", indent=indent)
    def __len__(self):
        return 1

class Declaration(Statement):
    def __init__(self):
        self.id: Token = Token()
        self.dtype: Token = Token() 
        self.value: Value = Value()
        self.dono_token: Token = Token()
        self.initialized: bool = False
        self.is_param: bool = False
        self.is_global: bool = False

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return f"{'declare' if not self.is_param else 'param'} {'constant' if self.dono_token.exists() else 'variable'}: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        if self.is_param:
            return {"dtype":self.dtype}
        return {"dtype":self.dtype, "value":self.value}

    def string(self, indent = 0) -> str:
        res = sprintln("declare:", self.id.flat_string(), indent=indent)
        res += sprintln("type:", self.dtype.flat_string(), indent=indent+1)
        if self.dono_token.exists():
            res += sprintln("constant", indent=indent+1)
        if self.initialized and not self.is_param:
            res += sprintln("value:", self.value.flat_string(), indent=indent+1)
        return res
    def python_string(self, indent=0, cwass=False) -> str:
        res = ""
        if cwass:
            global class_properties
            if self.id.python_string(cwass=cwass) in class_properties:
                res = "self."
        res += f"{self.id.python_string(cwass=cwass)}: {self.dtype.python_string(cwass=cwass)}"
        if self.is_param: return res

        if self.initialized:
            if self.dtype.token == TokenType.CHAN:
                # convert value to floats first then to int
                # this for strings being float strings but passed as int
                res += f" = {self.dtype.python_string(cwass=cwass)}({TokenType.KUN.python_string()}({self.value.python_string(cwass=cwass)}))"
            elif self.dtype.is_unique_type() or self.dtype.is_arr_type():
                res += f" = {self.value.python_string(cwass=cwass)}"
            else:
                res += f" = {self.dtype.python_string(cwass=cwass)}({self.value.python_string(cwass=cwass)})"
        elif self.is_param: pass
        else: res += f" = None"
        return sprint(res, indent=indent)

    def formatted_string(self, indent=0) -> str:
        res = sprint("", indent=indent)

        if self.is_global:
            res += "gwobaw "

        res += f"{self.id}-{self.dtype.formatted_string()}"
        if self.dono_token.exists():
            res += "-dono"

        if self.initialized and not self.is_param:
            res += f" = {self.value.formatted_string()}"

        if not self.is_param:
            res += "~"

        return res

class Assignment(Statement):
    def __init__(self):
        self.id: Token | IndexedIdentifier | ClassAccessor = Token() 
        self.value: Value = Value()
        self.dtype: Token = Token()

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return f"assign: {self.id.header()}"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        res: dict = {}
        if isinstance(self.id, ClassAccessor):
            res["accessed"] = self.id.accessed
        res["value"] = self.value
        return res

    def string(self, indent = 0) -> str:
        res = sprintln("assign:", self.id.flat_string(), indent=indent)
        res += sprintln("value:", self.value.flat_string(), indent=indent+1)
        return res
    def python_string(self, indent=0, cwass=False) -> str:
        res = ""
        if cwass:
            global class_properties
            if self.id.python_string(cwass=cwass) in class_properties:
                res = "self."
        if not self.dtype.exists(): raise Exception(f"UNREACHABLE::no dtype for assignment: '{self.id.flat_string()}'")
        res += f"{self.id.python_string(cwass=cwass)}"
        if self.dtype.token == TokenType.CHAN:
            # convert value to floats first then to int
            # this for strings being float strings but passed as int
            res += f" = {self.dtype.python_string(cwass=cwass)}({TokenType.KUN.python_string()}({self.value.python_string(cwass=cwass)}))"
        elif self.dtype.is_unique_type() or self.dtype.is_arr_type():
            res += f" = {self.value.python_string(cwass=cwass)}"
        else:
            res += f" = {self.dtype.python_string(cwass=cwass)}({self.value.python_string(cwass=cwass)})"
        return sprint(res, indent=indent)
    def formatted_string(self, indent=0) -> str:
        res = f"{self.id.formatted_string()} = {self.value.formatted_string()}~"
        return sprint(res, indent=indent)

    def __len__(self):
        return 1

class Print(Statement):
    def __init__(self):
        self.print: Token = Token()
        self.values: list[Value] = []

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "print:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        if self.values:
            return {**{f"val_{i+1}":v for i,v in enumerate(self.values)}}
        return None

    def string(self, indent = 0) -> str:
        res = sprintln("print:", indent=indent)
        for v in self.values:
            res += sprintln(v.flat_string(), indent=indent+1)
        return res

    def python_string(self, indent=0, cwass=False) -> str:
        res = "print("
        res += f"{', '.join(v.python_string(cwass=cwass) for v in self.values)}"
        res += ")"
        return sprint(res, indent=indent)

    def formatted_string(self, indent=0) -> str:
        res = f"pwint({', '.join(v.formatted_string() for v in self.values)})~"
        return sprint(res, indent=indent)

class IfStatement(Statement):
    def __init__(self):
        self.condition: Value = Value()
        self.then: BlockStatement = BlockStatement()
        self.else_if: list[ElseIfStatement] = []
        self.else_block: BlockStatement = BlockStatement()

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "if statement:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        ret = {"condition": self.condition, "then": self.then}
        if self.else_if:
            ret.update(**{f"else if {i+1}":e for i,e in enumerate(self.else_if)})
        if self.else_block:
            ret["else"] = self.else_block
        return ret

    def string(self, indent = 0) -> str:
        res = sprintln("if statement:", indent=indent)
        res += sprintln("condition:", self.condition.flat_string(), indent=indent+1)
        res += sprintln("then:", indent=indent+1)
        res += self.then.string(indent+2)
        for e in self.else_if:
            res += e.string(indent+1)
        if self.else_block:
            res += self.else_block.string(indent+1)
        return res

    def python_string(self, indent=0, cwass=False) -> str:
        res = sprintln(f"if {self.condition.python_string(cwass=cwass)}:", indent=0)
        res += self.then.python_string(indent+1, cwass=cwass)
        for e in self.else_if:
            res += e.python_string(indent, cwass=cwass)
        if self.else_block.statements:
            res += sprintln("else:", indent=indent)
            res += self.else_block.python_string(indent+1, cwass=cwass)
        return sprint(res, indent=indent)

    def formatted_string(self, indent=0) -> str:
        # iwf (condition) [[
        res = sprintln(f"iwf ({self.condition.formatted_string()}) [[", indent=indent)

        # then block
        res += self.then.formatted_string(indent+1)

        # ]] ewse iwf (condition) [[
        res += sprint("]]", indent=indent)
        for e in self.else_if:
            res += e.formatted_string(indent=indent)
        if self.else_block.statements:
            res += sprintln(" ewse [[", indent=0)
            res += self.else_block.formatted_string(indent=indent+1)
            res += sprint("]]", indent=indent)

        return res


class ElseIfStatement(Statement):
    def __init__(self):
        self.condition: Value = Value()
        self.then: BlockStatement = BlockStatement()

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "else if statement:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"condition":self.condition, "then":self.then}

    def string(self, indent = 0) -> str:
        res = sprintln("else if statement:", indent=indent)
        res += sprintln("condition:", self.condition.flat_string(), indent=indent+1)
        res += sprintln("then:", indent=indent+1)
        res += self.then.string(indent+2)
        return res

    def python_string(self, indent=0, cwass=False) -> str:
        res = sprintln(f"elif {self.condition.python_string(cwass=cwass)}:", indent=0)
        res += self.then.python_string(indent+1, cwass=cwass)
        return sprint(res, indent=indent)

    def formatted_string(self, indent=0) -> str:
        res = sprintln(f" ewse iwf ({self.condition.formatted_string()}) [[", indent=0)
        res += self.then.formatted_string(indent + 1)
        res += sprint("]]", indent=indent)
        return res

class WhileLoop(Statement):
    def __init__(self):
        self.condition: Value = Value()
        self.body: BlockStatement = BlockStatement()
        self.is_do = False

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return f"{'do' if self.is_do else ''} while statement:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"condition":self.condition, "body":self.body}

    def string(self, indent = 0) -> str:
        res = sprintln(f"{f'do' if self.is_do else ''} while statement:", indent=indent)
        res += sprintln("condition:", self.condition.flat_string(), indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

    def python_string(self, indent=0, cwass=False) -> str:
        res = ""
        if self.is_do:
            res = self.body.python_string(indent, cwass=cwass)
            # initial body of do while, remove breaks
            res = re.sub(r"break", "...", res)
        res += sprintln(f"while {self.condition.python_string(cwass=cwass)}:", indent=indent)
        res += self.body.python_string(indent+1, cwass=cwass)
        return res

    def formatted_string(self, indent=0) -> str:
        res = ""

        if self.is_do:
            res += "do "

        res += sprintln(f"whiwe({self.condition.formatted_string()}) [[", indent=0)
        res += self.body.formatted_string(indent=indent+1)
        res += sprint("]]", indent=indent)

        return sprint(res, indent=indent)

class ForLoop(Statement):
    def __init__(self):
        self.init: Declaration = Declaration()
        self.condition: Value = Value()
        self.update: Value = Value()
        self.body: BlockStatement = BlockStatement()

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "for loop:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"init":self.init, "condition":self.condition, "update":self.update, "body":self.body}

    def string(self, indent = 0) -> str:
        res = sprintln("for statement:", indent=indent)
        res += sprintln("init:", self.init.string(), indent=indent+1)
        res += sprintln("condition:", self.condition.flat_string(), indent=indent+1)
        res += sprintln("update:", self.update.flat_string(), indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

    def python_string(self, indent=0, cwass=False) -> str:
        res = sprintln(self.init.python_string(indent=indent))
        res += sprintln(f"while {self.condition.python_string(cwass=cwass)}:", indent=indent)
        res += self.body.python_string(indent+1, cwass=cwass)
        res += sprintln(f"{self.init.id.python_string(cwass=cwass)} = {self.update.python_string(cwass=cwass)}", indent=indent+1)
        return res

    def formatted_string(self, indent=0) -> str:
        init = self.init.formatted_string().replace(" ", "")
        condition = self.condition.formatted_string().replace(" ", "")
        update = self.update.formatted_string().replace(" ", "")

        res = sprintln(f"fow({init} {condition}~ {update}) [[", indent=0)
        res += self.body.formatted_string(indent=indent+1)
        res += sprint("]]", indent=indent)

        return sprint(res, indent=indent)

class Break(Statement):
    def __init__(self):
        self.token: Token = Token()
        self.in_loop: bool = False

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "break statement:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"break":self.token}

    def string(self, indent = 0) -> str:
        return sprintln("break statement:", indent=indent)
    def python_string(self, indent=0, cwass=False) -> str:
        return sprint("break" if self.in_loop else "...", indent=indent)
    def formatted_string(self, indent=0) -> str:
        return sprint("bweak~", indent=indent)

class Function(Production):
    def __init__(self):
        self.id: Token = Token()
        self.rtype: Token = Token()
        self.params: list[Declaration] = []
        self.body: BlockStatement = BlockStatement()

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return f"function: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        ret: dict[str, Production | Token] = {"rtype":self.rtype}
        if self.params:
            ret.update(**{f"param_{i+1}":p for i,p in enumerate(self.params)})
        ret["body"] = self.body
        return ret

    def string(self, indent = 0) -> str:
        res = sprintln("function:", self.id.flat_string(), indent=indent)
        res += sprintln("rtype:", self.rtype.flat_string(), indent=indent+1)
        if len(self.params) > 0:
            res += sprintln("parameters:", indent=indent+1)
            for param in self.params:
                res += sprint(param.string(indent+2), indent=indent+2)
        else:
            res += sprintln("parameters: None", indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

    def python_string(self, indent=0, cwass=False) -> str:
        params_string = [p.python_string(cwass=cwass) for p in self.params]
        if cwass:
            params_string.insert(0, "self")
        res = sprintln(f"def {self.id.python_string(cwass=cwass)}({', '.join(params_string)}):", indent=0)
        for param in self.params:
            if param.dtype.is_unique_type():
                res += sprintln(
                    f"{param.id.python_string(cwass=cwass)}: {param.dtype.python_string(cwass=cwass)} = {param.id.python_string(cwass=cwass)}",
                    indent=indent + 1)
            else:
                res += sprintln(
                    f"{param.id.python_string(cwass=cwass)}: {param.dtype.python_string(cwass=cwass)} = {param.dtype.python_string(cwass=cwass)}({param.id.python_string(cwass=cwass)})",
                    indent=indent + 1)
        res += self.body.python_string(indent+1, cwass=cwass)
        return sprintln(res, indent=indent)

    def formatted_string(self, indent=0) -> str:
        params_string = [p.formatted_string() for p in self.params]

        # fwunc id-dtype(params, params) [[
        res = f"fwunc {self.id.formatted_string()}-{self.rtype.formatted_string()}({', '.join(params_string)}) [["
        res = sprintln(res, indent=indent)

        # block statements
        res += self.body.formatted_string(indent=indent+1)

        # ]]
        res += sprint("]]", indent=indent)

        return res

class Class(Production):
    def __init__(self):
        self.id: Token = Token()
        self.params: list[Declaration] = []
        self.properties: list[Declaration] = []
        self.methods: list[Function] = []

        self.start_pos = None
        self.end_pos = None

        # For formatting
        self.definition_order = []

    def header(self):
        return f"class: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        ret = {}
        if self.params:
            ret.update(**{f"param_{i+1}":p for i,p in enumerate(self.params)})
        if self.properties:
            ret.update(**{f"property_{i+1}":p for i,p in enumerate(self.properties)})
        if self.methods:
            ret.update(**{f"method_{i+1}":m for i,m in enumerate(self.methods)})
        return ret

    def string(self, indent = 0) -> str:
        res = sprintln("class:", self.id.flat_string(), indent=indent)
        if self.params:
            res += sprintln("parameters:", indent=indent+1)
            for param in self.params:
                res += sprint(param.string(indent+2), indent=indent+2)
        if self.properties:
            res += sprintln("properties:", indent=indent+1)
            for prop in self.properties:
                res += prop.string(indent+2)
        if self.methods:
            res += sprintln("methods:", indent=indent+1)
            for method in self.methods:
                res += method.string(indent+2)
        return res

    def python_string(self, indent=0, cwass=False) -> str:
        global class_properties
        res = sprintln(f"class {self.id.python_string(cwass=True)}:", indent=indent)
        if self.params or self.properties:
            res += sprint(f"def __init__(self", indent=indent+1)
            if self.params:
                res += sprintln(f", {', '.join([p.python_string(cwass=cwass) for p in self.params])}):", indent=indent+1)
            else:
                res += '):\n'
            for param in self.params:
                if param.dtype.is_unique_type():
                    res += sprintln(
                        f"self.{param.id.python_string(cwass=True)}: {param.dtype.python_string(cwass=True)} = {param.id.python_string(cwass=True)}",
                        indent=indent + 2)
                else:
                    res += sprintln(f"self.{param.id.python_string(cwass=True)}: {param.dtype.python_string(cwass=True)} = {param.dtype.python_string(cwass=True)}({param.id.python_string(cwass=True)})", indent=indent+2)
                class_properties.add(param.id.python_string(cwass=True))
            for prop in self.properties:
                res += sprintln(f"self.{prop.python_string(cwass=True)}", indent=indent+2)
                class_properties.add(prop.id.python_string(cwass=True))
        res += sprintln(f"def __repr__(self):", indent=indent+1)
        res += sprintln(f'''return f"{{self.__class__.__name__[1:]}}({{', '.join(f'{{key[1:]}}={{value}}' for key, value in self.__dict__.items())}})"''', indent=indent+2)
        res += sprintln(f"def __str__(self):", indent=indent+1)
        res += sprintln(f'''return f"{{self.__class__.__name__[1:]}}({{', '.join(f'{{key[1:]}}={{value}}' for key, value in self.__dict__.items())}})"''', indent=indent+2)
        for method in self.methods:
            res += method.python_string(indent+1, cwass=True)
        class_properties.clear()
        return res

    def formatted_string(self, indent=0) -> str:
        params = ', '.join([p.formatted_string() for p in self.params])
        res = sprintln(f"cwass {self.id.formatted_string()}({params}) [[")

        definitions = []
        for definition in self.definition_order:
            if isinstance(definition, list):
                attrib_group = [att.formatted_string(indent=indent+1) for att in definition]
                definitions.append('\n'.join(attrib_group))
            else:
                definitions.append(definition.formatted_string(indent=indent+1))

        res += "\n\n".join(definitions)
        res += "\n]]"

        return res


class BlockStatement(Production):
    def __init__(self):
        self.statements: list[Statement] = []

        self.start_pos = None
        self.end_pos = None

    def header(self):
        return "block"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        if self.statements:
            # Filter out comments when constructing visual AST
            return {**{f"statement {i+1}":s for i,s in enumerate(self.statements) if not isinstance(s, Comment)}}
        return None

    def string(self, indent = 0) -> str:
        res = sprintln("block:", indent=indent)
        for s in self.statements:
            res += s.string(indent+1)
        return res
    def python_string(self, indent=0, cwass=False) -> str:
        res = ""
        for s in self.statements:
            res += s.python_string(indent, cwass=cwass) + '\n'
        return res

    def formatted_string(self, indent=0) -> str:
        res = ""
        for s in self.statements:
            res += s.formatted_string(indent=indent) + '\n'
        return res

class Comment:
    'only used in formatting'
    def __init__(self, token):
        self.comment: Token = token

        self.start_pos = None
        self.end_pos = None

    def python_string(self, indent=0, cwass=False) -> str:
        return ""

    def formatted_string(self, indent=0) -> str:
        return sprint(f"{str(self.comment)}", indent=indent)

class Program:
    'the root node of the syntax tree'
    def __init__(self):
        self.mainuwu: Function | None = None
        self.globals: list[Declaration] = []
        self.functions: list[Function] = []
        self.classes: list[Class] = []

        # For highlighting
        self.start_pos = None
        self.end_pos = None

        # For formatting
        self.definition_order = []

    def mainuwu_string(self, indent = 0):
        if not self.mainuwu:
            return ''
        res = self.mainuwu.string(indent)
        return res + "\n"

    def globals_string(self, indent = 0):
        res = ''
        for g in self.globals:
            res += g.string(indent)
        return res + "\n"

    def functions_string(self, indent = 0):
        res = ''
        for fn in self.functions:
            res += fn.string(indent)
        return res + "\n"

    def classes_string(self, indent = 0):
        res = ''
        for c in self.classes:
            res += c.string(indent)
        return res + "\n"

    def python_string(self, indent=0, cwass=False) -> str:
        res = ""
        if self.mainuwu:
            res += self.mainuwu.python_string(indent, cwass=cwass)
        for c in self.classes:
            res += c.python_string(indent, cwass=cwass)
        for fn in self.functions:
            res += fn.python_string(indent, cwass=cwass)
        res += sprintln("if __name__ == '__main__':", indent=indent)
        res += sprintln("# clear screen before executing", indent=indent+1)
        res += sprintln("import platform", indent=indent+1)
        res += sprintln("import os", indent=indent+1)
        res += sprintln("os.system('cls' if platform.system() == 'Windows' else 'clear')", indent=indent+1)
        res += sprintln()
        res += sprintln("# declare globals", indent=indent+1)
        for g in self.globals:
            res += sprintln(g.python_string(cwass=cwass), indent=indent+1)
        res += sprintln("main()", indent=indent+1)
        return res

    def formatted_string(self, indent=0) -> str:
        definitions = []
        for definition in self.definition_order:
            if isinstance(definition, list):
                global_dec_group = [dec.formatted_string() for dec in definition]
                definitions.append('\n'.join(global_dec_group))
            else:
                definitions.append(definition.formatted_string())

        return "\n\n".join(definitions)

    def __str__(self):
        res = "MAINUWU:\n"
        res += self.mainuwu_string(1)
        res += "GLOBALS:\n"
        res += self.globals_string(1)
        res += "FUNCTIONS:\n"
        res += self.functions_string(1)
        res += "CLASSES:\n"
        res += self.classes_string(1)
        return res
