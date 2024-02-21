'''
All productions must have an __str__() method
'''

def IndentFmt(indent, *val):
    return f"    " * indent + " ".join(val) + "\n"

def INDENT(n=0) -> str:
    return "    " * n

class ReturnStatement:
    def __init__(self):
        self.expr = None

    def string(self, indent = 1):
        return IndentFmt(indent, f"return {self.expr.string()}")
    def __len__(self):
        return 1

class PrefixExpression:
    def __init__(self):
        self.op = None
        self.right = None

    def string(self, _ = 1):
        return IndentFmt(0, f"prefix: {self.op.string()} {self.right.string()}")[:-1]
    def __len__(self):
        return 1

class InfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
        self.right = None

    def string(self, _ = 1):
        return IndentFmt(0, f"infix: {self.left.string()} {self.op.string()} {self.right.string()}")[:-1]
    def __len__(self):
        return 1

class PostfixExpression:
    def __init__(self):
        self.left = None
        self.op = None

    def string(self, _ = 1):
        return IndentFmt(0, f"postfix: {self.left.string()} {self.op.string()}")[:-1]
    def __len__(self):
        return 1

class StringFmt:
    def __init__(self):
        self.start = None
        self.mid = []
        self.exprs = []
        self.end = None

    def string(self, indent = 1):
        res = IndentFmt(0, "string fmt:")
        res += IndentFmt(indent+1, f"{self.start.string()}")
        for val in self.mid_expr_iter():
            res += IndentFmt(indent+1, val.string())
        res += IndentFmt(indent+1, self.end.string())
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
    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)

class ArrayDeclaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False

    def string(self, indent = 1):
        res = IndentFmt(indent, "declare array:", self.id.string())
        res += IndentFmt(indent+1, f"type:", self.dtype.string())
        if self.is_const:
            res += IndentFmt(indent+1, "constant")
        if self.value:
            res += IndentFmt(indent+1, "value:")
            res += IndentFmt(indent+2, self.value.string())
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

class Assignment:
    def __init__(self):
        self.id = None
        self.value = None
    def string(self, indent = 1):
        res = IndentFmt(indent, "assign:", self.id.string())
        res += IndentFmt(indent+1, "value:", self.value.string())
        return res
    def __len__(self):
        return 1

class Declaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False

    def string(self, indent = 1):
        res = IndentFmt(indent, "declare:", self.id.string())
        res += IndentFmt(indent+1, "type:", self.dtype.string())
        if self.is_const:
            res += IndentFmt(indent+1, "constant")
        if self.value:
            res += IndentFmt(indent+1, "value:", self.value.string(indent+1))
        return res

class FnCall:
    def __init__(self):
        self.id = None
        self.args = []

    def string(self, _ = 1):
        return IndentFmt(0, f"call: {self.id.string()}({', '.join([a.string() for a in self.args])})")
    def __len__(self):
        return 1

class IfExpression:
    def __init__(self):
        self.condition = None
        self.then = None
        self.else_if: list[ElseIfExpression] = []
        self.else_block = None

    def string(self, indent = 1):
        res = IndentFmt(indent, "if statement:")
        res += IndentFmt(indent+1, "condition:", self.condition.string())
        res += IndentFmt(indent+1, "then:")
        res += self.then.string(indent+2)
        for e in self.else_if:
            res += IndentFmt(indent+1, "else if statement:")
            res += IndentFmt(indent+2, "condition:", e.condition.string())
            res += IndentFmt(indent+2, "then:")
            res += e.then.string(indent+3)
        if self.else_block:
            res += IndentFmt(indent+1, "else:")
            res += self.else_block.string(indent+2)
        return res

class ElseIfExpression:
    def __init__(self):
        self.condition = None
        self.then = None

class WhileLoop:
    def __init__(self):
        self.condition = None
        self.body = None
        self.is_do = False
    def string(self, indent = 1):
        res = IndentFmt(indent, f"{f'do' if self.is_do else ''} while statement:")
        res += IndentFmt(indent+1, "condition:", self.condition.string())
        res += IndentFmt(indent+1, "body:")
        res += self.body.string(indent+2)
        return res

class ForLoop:
    def __init__(self):
        self.init = None # can be declaration or just an ident
        self.condition = None
        self.update = None
        self.body = None
    def string(self, indent = 1):
        res = IndentFmt(indent, "for statement:")
        res += IndentFmt(indent+1, "init: ", self.init.string())
        res += IndentFmt(indent+1, "condition: ", self.condition.string())
        res += IndentFmt(indent+1, "update: ", self.update.string())
        res += IndentFmt(indent+1, "body:")
        res += self.body.string(indent+2)
        return res

class Print:
    def __init__(self):
        self.values = []
    def string(self, indent = 1):
        res = IndentFmt(indent, "print:")
        for v in self.values:
            res += IndentFmt(indent+1, v.string())
        return res

class Input:
    def __init__(self):
        self.value = None
    def string(self, indent = 1):
        res = IndentFmt(indent, "input:", self.value.string())
        return res
    def print(self, indent = 1):
        print(f"{INDENT(indent)} input: ", end='')
        self.value.print(indent)

class Function:
    def __init__(self):
        self.id = None
        self.rtype = None
        self.params: list[Parameter] = []
        self.body = None

    def string(self, indent = 1):
        res = IndentFmt(indent, "function:", self.id.string())
        res += IndentFmt(indent+1, "rtype:", self.rtype.string())
        if self.params:
            res += IndentFmt(indent+1, "parameters:")
            for param in self.params:
                res += IndentFmt(indent+2, param.string(indent+2))[:-1]
        else:
            res += IndentFmt(indent+1, "parameters: None")
        res += IndentFmt(indent+1, "body:")
        res += self.body.string(indent+2)
        return res

class Parameter:
    def __init__(self):
        self.id = None
        self.dtype = None

    def string(self, indent = 1):
        res = IndentFmt(0, "param:", self.id.string())
        res += IndentFmt(indent+1, "dtype:", self.dtype.string())
        return res

class Class:
    def __init__(self):
        self.id = None
        self.params: list = []
        self.body: list = []
        self.properties: list = []
        self.methods: list = []
    def string(self, indent = 1):
        res = IndentFmt(indent, "class:", self.id.string())
        if self.params:
            res += IndentFmt(indent+1, "parameters:")
            for param in self.params:
                res += IndentFmt(indent+2, param.string(indent+2))[:-1]
        if self.properties:
            res += IndentFmt(indent+1, "properties:")
            for prop in self.properties:
                res += prop.string(indent+2)
        if self.methods:
            res += IndentFmt(indent+1, "methods:")
            for method in self.methods:
                res += method.string(indent+2)
        if self.body:
            res += IndentFmt(indent+1, "body:")
            res += self.body.string(indent+2)
        return res

class BlockStatement:
    def __init__(self):
        self.statements = []
    def string(self, indent = 1):
        res = IndentFmt(indent, "block:")
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

    def __str__(self):
        res = "MAINUWU:\n"
        res += self.mainuwu.string()
        res += "\nGLOBALS:\n"
        for g in self.globals:
            res += g.string()
        res += "\nFUNCTIONS:\n"
        for fn in self.functions:
            res += fn.string()
        res += "\nCLASSES:\n"
        for c in self.classes:
            res += c.string()
        return res
