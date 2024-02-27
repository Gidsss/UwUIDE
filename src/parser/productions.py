from src.lexer import Token

### BASE CLASS
# for type checking
class Production:
    pass
'''
All productions must have these methods:
1. string(self, indent = 0)

2. header(self) -> str
    - returns the string representation of the production
    - it can be a title or the value of the production itself
    - titles are for class productions
    - values are for atomic productions

3. child_nodes(self) -> None | dict[str, Production]
    - returns None if atomic (aka leaf)
        - the value of the atomic production is in the header() method
    - returns a dict of key:val where key is the title of the child and val is the production
'''

def sprint(*val, indent = 0):
    'return string with optional identation'
    return "    " * indent + " ".join(val)
def sprintln(*val, indent = 0):
    'return newline terminated string with optional identation'
    return sprint(*val, indent=indent) + "\n"

### EXPRESSION PRODUCTIONS
class PrefixExpression(Production):
    def __init__(self):
        self.op = None
        self.right = None

    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, _ = 1):
        return sprint(self.op.string(), self.right.string())
    def __len__(self):
        return 1

class InfixExpression(Production):
    def __init__(self):
        self.left = None
        self.op = None
        self.right = None
    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, _ = 1):
        return f'({self.left.string()} {self.op.string()} {self.right.string()})'
    def __len__(self):
        return 1

class PostfixExpression(Production):
    def __init__(self):
        self.left = None
        self.op = None
    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, _ = 1):
        return sprint(self.left.string(), self.op.string(), indent=0)
    def __len__(self):
        return 1

### LITERAL PRODUCTIONS
class StringFmt(Production):
    def __init__(self):
        self.start = None
        self.mid = []
        self.exprs = []
        self.end = None

    def header(self):
        return "string fmt:"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"start":self.start, **{f"mid_{i+1}":m for i,m in enumerate(self.mid_expr_iter())}, "end":self.end}

    def string(self, indent = 0):
        res = sprintln("string fmt:", indent=0)
        res += sprintln(self.start.string(), indent=indent+1)
        for val in self.mid_expr_iter():
            res += sprintln(val.string(), indent=indent+1)
        res += sprint(self.end.string(), indent=indent+1)
        return res[:-1]
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

class ArrayLiteral(Production):
    def __init__(self):
        self.elements = []

    def header(self):
        return "array literal:"
    def child_nodes(self) -> None | dict[str, Production]:
        return {f"item_{i+1}":e for i,e in enumerate(self.elements)}

    def string(self, indent = 0):
        res = sprintln("array literal:", indent=0)
        for e in self.elements:
            res += sprintln(e.string(indent+1), indent=indent+1)
        return res
    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)

class FnCall(Production):
    def __init__(self):
        self.id = None
        self.args = []
        self.in_expr = False    # For determining indent in printing

    def header(self):
        if self.in_expr:
            return sprint(self.id.string(),
                            f'({", ".join([a.string() for a in self.args])})',
                            indent=0)
        return sprint("call:", self.id.string(),
                        f'({", ".join([a.string() for a in self.args])})',
                        indent=0)

    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, indent = 1):
        if self.in_expr:
            return sprint("call:", self.id.string(),
                            f'({", ".join([a.string() for a in self.args])})',
                            indent=0)
        else:
            return sprintln("call:", self.id.string(),
                          f'({", ".join([a.string() for a in self.args])})',
                          indent=indent)
    def __len__(self):
        return 1

class IndexedIdentifier(Production):
    '''
    id can be:
    - token:    ident[i]
    - FnCall:   fn()[i]
    '''
    def __init__(self):
        self.id: Token | FnCall = None
        self.index = None

    def header(self):
        return self.string()

    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, indent = 0):
        return sprintln("id:", self.id.string(), "index:", self.index.string(), indent=indent)

class ClassAccessor(Production):
    '''
    id can be:
    - token:    ident.property, Cwass.property
    - FnCall:   fn().property
    can access:
    - token:         ident.property, Cwass.property
    - FnCall:        ident.method(), Cwass.method()
    - indexed:       ident.property[index], Cwass.method()[index]
    - ClassAccessor: ident.property.property, Cwass.property.method()
    '''
    def __init__(self):
        self.id: Token | FnCall = None
        self.accessed: Token | FnCall | IndexedIdentifier | ClassAccessor = None

    def header(self):
        return f"{self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"accessed":self.accessed}

    def string(self, indent = 0):
        ret = sprintln("id:", self.id.string())
        ret += sprintln("accessed:", self.accessed.string(indent+1), indent=indent+1)
        return ret
    def __len__(self):
        return 1


### GENERAL STATEMENT PRODUCTIONS ###
class ReturnStatement(Production):
    def __init__(self):
        self.expr = None

    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, indent = 0):
        return sprintln("return", self.expr.string(indent), indent=indent)
    def __len__(self):
        return 1

class ArrayDeclaration(Production):
    def __init__(self):
        self.id: Token = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False

    def header(self):
        return f"declare{' constant' if self.is_const else ''} array: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"dtype":self.dtype, "value":self.value}

    def string(self, indent = 0):
        res = sprintln("declare array:", self.id.string(), indent=indent)
        res += sprintln("type:", self.dtype.string(), indent=indent+1)
        if self.is_const:
            res += sprintln("constant", indent=indent+1)
        if self.value:
            res += sprintln("value:", self.value.string(indent+1), indent=indent+1)
        return res

    def compute_len(self):
        def compute_lengths(array, depth):
            if isinstance(array, ArrayLiteral):
                # initialize with zero value so self.length[depth]
                # is not an out of bounds error
                if depth >= len(self.length):
                    self.length.append(0)

                # get length of largest element in current dimension
                self.length[depth] = max(self.length[depth], len(array.elements))

                # go through each element since elements
                # might not have the same depth
                for elem in array.elements:
                    compute_lengths(elem, depth + 1)

        compute_lengths(self.value, 0)

class UselessIdStatement(Production):
    def __init__(self):
        self.id: Token = None

    def header(self):
        return self.string()
    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, indent = 0):
        return sprintln("id:", self.id.string(), indent=indent)

class Assignment(Production):
    def __init__(self):
        self.id: Token = None
        self.value = None

    def header(self):
        return f"assign: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"value": self.value}

    def string(self, indent = 0):
        res = sprintln("assign:", self.id.string(), indent=indent)
        res += sprintln("value:", self.value.string(indent), indent=indent+1)
        return res
    def __len__(self):
        return 1

class Declaration(Production):
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False

    def header(self):
        return f"declare {'constant' if self.is_const else 'variable'}: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"dtype":self.dtype, "value":self.value}

    def string(self, indent = 0):
        res = sprintln("declare:", self.id.string(), indent=indent)
        res += sprintln("type:", self.dtype.string(), indent=indent+1)
        if self.is_const:
            res += sprintln("constant", indent=indent+1)
        if self.value:
            res += sprintln("value:", self.value.string(indent+1), indent=indent+1)
        return res

class Print(Production):
    def __init__(self):
        self.values = []

    def header(self):
        return "print:"
    def child_nodes(self) -> None | dict[str, Production]:
        if self.values:
            return {**{f"val_{i+1}":v for i,v in enumerate(self.values)}}
        return None

    def string(self, indent = 0):
        res = sprintln("print:", indent=indent)
        for v in self.values:
            res += sprintln(v.string(), indent=indent+1)
        return res

class Input(Production):
    def __init__(self):
        self.value = None

    def header(self):
        return "input"
    def child_nodes(self) -> None | dict[str, Production]:
        if self.value:
            return {"value":self.value}
        return None

    def string(self, indent = 0):
        return sprintln("input:", self.value.string(), indent=indent)
    def print(self, indent = 0):
        print(f"{INDENT(indent)} input: ", end='')
        self.value.print(indent)

class Parameter(Production):
    def __init__(self):
        self.id = None
        self.dtype = None

    def header(self):
        return f"id: {self.id.string()}, dtype: {self.dtype.string()}"
    def child_nodes(self) -> None | dict[str, Production]:
        return None

    def string(self, indent = 0):
        res = sprintln("param:", self.id.string(), indent=0)
        res += sprintln("dtype:", self.dtype.string(), indent=indent+1)
        return res

### BLOCK STATEMENT PRODUCTIONS
class IfStatement(Production):
    def __init__(self):
        self.condition = None
        self.then = None
        self.else_if: list[ElseIfStatement] = []
        self.else_block: ElseStatement = None

    def header(self):
        return "if statement:"
    def child_nodes(self) -> None | dict[str, Production]:
        ret = {"condition": self.condition, "then": self.then}
        if self.else_if:
            ret.update(**{f"else if {i+1}":e for i,e in enumerate(self.else_if)})
        if self.else_block:
            ret["else"] = self.else_block
        return ret

    def string(self, indent = 0):
        res = sprintln("if statement:", indent=indent)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("then:", indent=indent+1)
        res += self.then.string(indent+2)
        for e in self.else_if:
            res += e.string(indent+1)
        if self.else_block:
            res += self.else_block.string(indent+1)
        return res

class ElseIfStatement(Production):
    def __init__(self):
        self.condition = None
        self.then = None

    def header(self):
        return "else if statement:"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"condition":self.condition, "then":self.then}

    def string(self, indent = 0):
        res = sprintln("else if statement:", indent=indent)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("then:", indent=indent+1)
        res += self.then.string(indent+2)
        return res

class ElseStatement(Production):
    def __init__(self):
        self.body = None

    def header(self):
        return "else statement:"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"body":self.body}

    def string(self, indent = 0):
        res = sprintln("else statement:", indent=indent)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

class WhileLoop(Production):
    def __init__(self):
        self.condition = None
        self.body = None
        self.is_do = False

    def header(self):
        return f"{'do' if self.is_do else ''} while statement:"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"condition":self.condition, "body":self.body}

    def string(self, indent = 0):
        res = sprintln(f"{f'do' if self.is_do else ''} while statement:", indent=indent)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

class ForLoop(Production):
    def __init__(self):
        self.init = None # can be declaration or just an ident
        self.condition = None
        self.update = None
        self.body = None

    def header(self):
        return "for loop:"
    def child_nodes(self) -> None | dict[str, Production]:
        return {"init":self.init, "condition":self.condition, "update":self.update, "body":self.body}

    def string(self, indent = 0):
        res = sprintln("for statement:", indent=indent)
        res += sprintln("init:", self.init.string(), indent=indent+1)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("update:", self.update.string(), indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

class Function(Production):
    def __init__(self):
        self.id = None
        self.rtype = None
        self.params: list[Parameter] = []
        self.body = None

    def header(self):
        return f"function: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production]:
        ret = {"rtype":self.rtype}
        if self.params:
            ret.update(**{f"param_{i+1}":p for i,p in enumerate(self.params)})
        ret["body"] = self.body
        return ret

    def string(self, indent = 0):
        res = sprintln("function:", self.id.string(), indent=indent)
        res += sprintln("rtype:", self.rtype.string(), indent=indent+1)
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
        self.id = None
        self.params: list = []
        self.body: BlockStatement = None
        self.properties: list = []
        self.methods: list = []

    def header(self):
        return f"class: {self.id.string()}"
    def child_nodes(self) -> None | dict[str, Production]:
        ret = {}
        if self.params:
            ret.update(**{f"param_{i+1}":p for i,p in enumerate(self.params)})
        if self.body:
            ret["body"] = self.body
        if self.properties:
            ret.update(**{f"property_{i+1}":p for i,p in enumerate(self.properties)})
        if self.methods:
            ret.update(**{f"method_{i+1}":m for i,m in enumerate(self.methods)})
        return ret

    def string(self, indent = 0):
        res = sprintln("class:", self.id.string(), indent=indent)
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
        if self.body:
            res += sprintln("body:", indent=indent+1)
            res += self.body.string(indent+2)
        return res

class BlockStatement(Production):
    def __init__(self):
        self.statements = []

    def header(self):
        return "block"
    def child_nodes(self) -> None | dict[str, Production]:
        if self.statements:
            return {**{f"statement {i+1}":s for i,s in enumerate(self.statements)}}
        return None

    def string(self, indent = 0):
        res = sprintln("block:", indent=indent)
        for s in self.statements:
            res += s.string(indent+1)
        return res

class Program(Production):
    'the root node of the syntax tree'
    def __init__(self):
        self.mainuwu = None
        self.globals: list = []
        self.functions: list = []
        self.classes: list = []

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
