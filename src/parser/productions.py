from src.lexer.token import TokenType
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

    def header(self) -> str:
        return self.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.op.flat_string()}{self.right.flat_string()}"

    def __len__(self):
        return 1

class InfixExpression(Expression):
    def __init__(self):
        self.left: Value = Value()
        self.op: Token = Token()
        self.right: Value = Value()
    def header(self):
        return ""
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"left":self.left, "op":self.op, "right":self.right}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f'({self.left.flat_string()} {self.op.flat_string()} {self.right.flat_string()})'

    def __len__(self):
        return 1

class PostfixExpression(Expression):
    def __init__(self):
        self.left: Value = Value()
        self.op: Token = Token()
    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None

    def string(self, indent = 1) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.left.flat_string()}{self.op.flat_string()}"
    def __len__(self):
        return 1

### LITERAL PRODUCTIONS
class StringLiteral(Iterable):
    def __init__(self, val: Token):
        self.val: Token = val
        self.concats: list[StringFmt | Input | StringLiteral] = []
    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None
    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return sprint(self.val.flat_string(), *[c.flat_string() for c in self.concats])
    def __len__(self):
        return 1

class Input(Iterable):
    def __init__(self):
        self.expr: Value | Token = Value()
        self.concats: list[StringFmt | Input | StringLiteral] = []

    def header(self):
        return "input:"

    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"expr":self.expr, **{f"concat_{i+1}":c for i,c in enumerate(self.concats)}}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"input({self.expr.flat_string()}) & {' & '.join(c.flat_string() for c in self.concats)}"

    def __len__(self):
        return 1

class StringFmt(Iterable):
    def __init__(self):
        self.start: Token = Token()
        self.mid: list[Token] = []
        self.exprs: list[Value | Token] = []
        self.end: Token = Token()
        self.concats: list[StringFmt | Input | StringLiteral] = []

    def header(self):
        return "string fmt:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"start":self.start, **{f"mid_{i+1}":m for i,m in enumerate(self.mid_expr_iter())}, "end":self.end, **{f"concat_{i+1}":c for i,c in enumerate(self.concats)}}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.start.flat_string()}{' '.join(m.flat_string() for m in self.mid_expr_iter())}{self.end.flat_string()}"
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

    def __len__(self):
        return 1

class ArrayLiteral(Iterable):
    def __init__(self):
        self.elements: list[Value] = []

    def header(self):
        return "array literal:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {f"item_{i+1}":e for i,e in enumerate(self.elements)}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{{{', '.join(e.flat_string() for e in self.elements)}}}"
    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)

class FnCall(IdentifierProds):
    def __init__(self):
        self.id: Token = Token()
        self.args: list[Value] = []

    def header(self):
        return sprint("call:", self.id.string(),indent=0)
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {**{f"arg_{i+1}":a for i,a in enumerate(self.args)}}

    def string(self, indent = 0) -> str:
        return self.flat_string(indent) + '\n'
    def flat_string(self, indent = 0) -> str:
        return sprint(f"{self.id.flat_string()}({', '.join(a.flat_string() for a in self.args)})", indent=indent)
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

    def header(self):
        return self.string()

    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        res = self.id.flat_string()
        for index in self.index:
            res += f"[{index.flat_string()}]"
        return res

class ClassConstructor(IdentifierProds):
    def __init__(self):
        self.id: Token = Token()
        self.args: list[Value] = []

    def header(self):
        return sprint("constructor:", self.id.string(),indent=0)
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {**{f"arg_{i+1}":a for i,a in enumerate(self.args)}}

    def string(self, indent = 1) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.id.flat_string()}({', '.join(a.flat_string() for a in self.args)})"
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

    def header(self):
        return self.id.string()
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"accessed":self.accessed}

    def string(self, indent = 0) -> str:
        return self.flat_string()
    def flat_string(self) -> str:
        return f"{self.id.flat_string()}.{self.accessed.flat_string()}"
    def __len__(self):
        return 1


### BLOCK STATEMENT PRODUCTIONS
class ReturnStatement(Statement):
    def __init__(self):
        self.expr: Value = Value()

    def header(self):
        return "return"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"val":self.expr}

    def string(self, indent = 0) -> str:
        return sprintln("return", self.expr.string(indent), indent=indent)
    def __len__(self):
        return 1

class Declaration(Statement):
    def __init__(self):
        self.id: Token = Token()
        self.dtype: Token = Token() 
        self.value: Value = Value()
        self.is_const: bool = False

    def header(self):
        return f"declare {'constant' if self.is_const else 'variable'}: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"dtype":self.dtype, "value":self.value}

    def string(self, indent = 0) -> str:
        res = sprintln("declare:", self.id.flat_string(), indent=indent)
        res += sprintln("type:", self.dtype.flat_string(), indent=indent+1)
        if self.is_const:
            res += sprintln("constant", indent=indent+1)
        if self.value:
            res += sprintln("value:", self.value.flat_string(), indent=indent+1)
        return res

class ArrayDeclaration(Statement):
    def __init__(self):
        self.id: Token = Token()
        self.dtype: Token = Token()
        self.value: Value = Value()
        self.is_const: bool = False

    def header(self):
        return f"declare{' constant' if self.is_const else ''} array: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"dtype":self.dtype, "value":self.value}

    def string(self, indent = 0) -> str:
        res = sprintln("declare array:", self.id.flat_string(), indent=indent)
        res += sprintln("type:", self.dtype.flat_string(), indent=indent+1)
        if self.is_const:
            res += sprintln("constant", indent=indent+1)
        if self.value:
            res += sprintln("value:", self.value.flat_string(), indent=indent+1)
        return res

class Assignment(Statement):
    def __init__(self):
        self.id: Token | IndexedIdentifier | ClassAccessor = Token() 
        self.value: Value = Value()

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
    def __len__(self):
        return 1

class Print(Statement):
    def __init__(self):
        self.values: list[Value] = []

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

class IfStatement(Statement):
    def __init__(self):
        self.condition: Value = Value()
        self.then: BlockStatement = BlockStatement()
        self.else_if: list[ElseIfStatement] = []
        self.else_block: BlockStatement = BlockStatement()

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

class ElseIfStatement(Statement):
    def __init__(self):
        self.condition: Value = Value()
        self.then: BlockStatement = BlockStatement()

    def header(self):
        return "else if statement:"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return {"condition":self.condition, "then":self.then}

    def string(self, indent = 0) -> str:
        res = sprintln("else if statement:", indent=indent)
        res += sprintln("condition:", self.condition.flat_string(), indent=indent+1)
        res += sprintln("then:", indent=indent+1)
        res += self.then.string(indent+2)
        # res = sprintln("else if statement:", indent=indent)
        # res += sprintln("condition:", self.condition.string(), indent=indent+1)
        # res += sprintln("then:", indent=indent+1)
        # res += self.then.string(indent+2)
        return res

class WhileLoop(Statement):
    def __init__(self):
        self.condition: Value = Value()
        self.body: BlockStatement = BlockStatement()
        self.is_do = False

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

class ForLoop(Statement):
    def __init__(self):
        self.init: (
            Token |  FnCall | IndexedIdentifier
            | ClassAccessor
            | Assignment | Declaration | ArrayDeclaration
        ) = Token()
        self.condition: Value = Value()
        self.update: Value = Value()
        self.body: BlockStatement = BlockStatement()

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

class Parameter(Production):
    def __init__(self):
        self.id: Token = Token()
        self.dtype: Token = Token()

    def header(self):
        return f"id: {self.id.string()}, dtype: {self.dtype.string()}"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        return None

    def string(self, indent = 0) -> str:
        res = sprintln("param:", self.id.flat_string(), indent=0)
        res += sprintln("dtype:", self.dtype.flat_string(), indent=indent+1)
        return res

class Function(Production):
    def __init__(self):
        self.id: Token = Token()
        self.rtype: Token = Token()
        self.params: list[Parameter] = []
        self.body: BlockStatement = BlockStatement()

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
        if self.params:
            res += sprintln("parameters:", indent=indent+1)
            for param in self.params:
                res += sprint(param.string(indent+2), indent=indent+2)
        else:
            res += sprintln("parameters: None", indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

class Class(Production):
    def __init__(self):
        self.id: Token = Token()
        self.params: list[Parameter] = []
        self.properties: list[Declaration | ArrayDeclaration] = []
        self.methods: list[Function] = []

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

    def member_signatures(self) -> dict[str, TokenType]:
        ret: dict[str, TokenType] = {}
        for p in self.params:
            ret[f"{self.id.string()}.{p.id.string()}"] = p.dtype.token
        for p in self.properties:
            ret[f"{self.id.string()}.{p.id.string()}"] = p.dtype.token
        for m in self.methods:
            ret[f"{self.id.string()}.{m.id.string()}"] = m.rtype.token
        return ret

class BlockStatement(Production):
    def __init__(self):
        self.statements = []

    def header(self):
        return "block"
    def child_nodes(self) -> None | dict[str, Production | Token]:
        if self.statements:
            return {**{f"statement {i+1}":s for i,s in enumerate(self.statements)}}
        return None

    def string(self, indent = 0) -> str:
        res = sprintln("block:", indent=indent)
        for s in self.statements:
            res += s.string(indent+1)
        return res

class Program:
    'the root node of the syntax tree'
    def __init__(self):
        self.mainuwu: Function | None = None
        self.globals: list[Declaration | ArrayDeclaration] = []
        self.functions: list[Function] = []
        self.classes: list[Class] = []

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
