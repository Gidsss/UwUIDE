'''
All productions must have these properties:
1. folded: bool

All productions must have these methods:
1. string(self, indent = 0)
2. toggle_fold(self)
3. child_nodes(self) -> str | list[production classes]
    - returns string if atomic (aka leaf)
    - returns other production classes if not
'''

def sprint(*val, indent = 0):
    'return string with optional identation'
    return "    " * indent + " ".join(val)
def sprintln(*val, indent = 0):
    'return newline terminated string with optional identation'
    return sprint(*val, indent=indent) + "\n"

### EXPRESSION PRODUCTIONS
class PrefixExpression:
    def __init__(self):
        self.op = None
        self.right = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return self.string()

    def string(self, _ = 1):
        return sprint(self.op.string(), self.right.string(), indent=0)
    def __len__(self):
        return 1

class InfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
        self.right = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return self.string()

    def string(self, _ = 1):
        return sprint(f'({self.left.string()} {self.op.string()} {self.right.string()})', indent=0)
    def __len__(self):
        return 1

class PostfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
        self.folded = False

    def toggle_fold(self) -> str | list:
        self.folded = not self.folded
    def child_nodes(self):
        return self.string()

    def string(self, _ = 1):
        return sprint(self.left.string(), self.op.string(), indent=0)
    def __len__(self):
        return 1

### LITERAL PRODUCTIONS
class StringFmt:
    def __init__(self):
        self.start = None
        self.mid = []
        self.exprs = []
        self.end = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return self.string()

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
    def __len__(self):
        return 1

class ArrayLiteral:
    def __init__(self):
        self.elements = []
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return self.elements

    def string(self, indent = 0):
        res = sprintln("array literal:", indent=0)
        for e in self.elements:
            res += sprintln(e.string(indent+1), indent=indent+1)
        return res
    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)

class FnCall:
    def __init__(self):
        self.id = None
        self.args = []
        self.in_expr = False    # For determining indent in printing
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return self.args

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

### GENERAL STATEMENT PRODUCTIONS ###
class ReturnStatement:
    def __init__(self):
        self.expr = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return self.string()

    def string(self, indent = 0):
        return sprintln("return", self.expr.string(indent), indent=indent)
    def __len__(self):
        return 1

class ArrayDeclaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.dtype, self.value, self.is_const]

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

class UselessIdStatement:
    def __init__(self):
        self.id = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return self.string()

    def string(self, indent = 0):
        return sprintln("id:", self.id.string(), indent=indent)

class Assignment:
    def __init__(self):
        self.id = None
        self.value = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.value]

    def string(self, indent = 0):
        res = sprintln("assign:", self.id.string(), indent=indent)
        res += sprintln("value:", self.value.string(), indent=indent+1)
        return res
    def __len__(self):
        return 1

class Declaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.dtype, self.value, self.is_const]

    def string(self, indent = 0):
        res = sprintln("declare:", self.id.string(), indent=indent)
        res += sprintln("type:", self.dtype.string(), indent=indent+1)
        if self.is_const:
            res += sprintln("constant", indent=indent+1)
        if self.value:
            res += sprintln("value:", self.value.string(indent+1), indent=indent+1)
        return res

class Print:
    def __init__(self):
        self.values = []
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return self.string()

    def string(self, indent = 0):
        res = sprintln("print:", indent=indent)
        for v in self.values:
            res += sprintln(v.string(), indent=indent+1)
        return res

class Input:
    def __init__(self):
        self.value = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return self.string()

    def string(self, indent = 0):
        return sprintln("input:", self.value.string(), indent=indent)
    def print(self, indent = 0):
        print(f"{INDENT(indent)} input: ", end='')
        self.value.print(indent)

class Parameter:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        return f"id: {self.id}, dtype: {self.dtype}"

    def string(self, indent = 0):
        res = sprintln("param:", self.id.string(), indent=0)
        res += sprintln("dtype:", self.dtype.string(), indent=indent+1)
        return res

### BLOCK STATEMENT PRODUCTIONS
class IfStatement:
    def __init__(self):
        self.condition = None
        self.then = None
        self.else_if: list[ElseIfStatement] = []
        self.else_block = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.condition, self.then, self.else_if, self.else_block]

    def string(self, indent = 0):
        res = sprintln("if statement:", indent=indent)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("then:", indent=indent+1)
        res += self.then.string(indent+1)
        for e in self.else_if:
            res += e.string(indent+1)
        if self.else_block:
            res += sprintln("else:", indent=indent+1)
            res += self.else_block.string(indent+2)
        return res

class ElseIfStatement:
    def __init__(self):
        self.condition = None
        self.then = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.condition, self.then]

    def string(self, indent = 0):
        res = sprintln("else if statement:", indent=indent)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("then:", indent=indent+1)
        res += self.then.string(indent+2)
        return res

class WhileLoop:
    def __init__(self):
        self.condition = None
        self.body = None
        self.is_do = False
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        if self.is_do:
            return ["do while", self.condition, self.body]
        return [self.condition, self.body]

    def string(self, indent = 0):
        res = sprintln(f"{f'do' if self.is_do else ''} while statement:", indent=indent)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

class ForLoop:
    def __init__(self):
        self.init = None # can be declaration or just an ident
        self.condition = None
        self.update = None
        self.body = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.init, self.condition, self.update, self.body]

    def string(self, indent = 0):
        res = sprintln("for statement:", indent=indent)
        res += sprintln("init:", self.init.string(), indent=indent+1)
        res += sprintln("condition:", self.condition.string(), indent=indent+1)
        res += sprintln("update:", self.update.string(), indent=indent+1)
        res += sprintln("body:", indent=indent+1)
        res += self.body.string(indent+2)
        return res

class Function:
    def __init__(self):
        self.id = None
        self.rtype = None
        self.params: list[Parameter] = []
        self.body = None
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.rtype, self.params, self.body]

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

class Class:
    def __init__(self):
        self.id = None
        self.params: list = []
        self.body: list = []
        self.properties: list = []
        self.methods: list = []
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return [self.params, self.body, self.properties, self.methods]

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

class BlockStatement:
    def __init__(self):
        self.statements = []
        self.folded = False

    def toggle_fold(self):
        self.folded = not self.folded
    def child_nodes(self) -> str | list:
        if self.folded:
            return "..."
        return self.statements

    def string(self, indent = 0):
        res = sprintln("block:", indent=indent)
        for s in self.statements:
            res += s.string(indent+1)
        return res

class Program:
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
