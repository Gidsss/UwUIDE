'''
All productions must have an __str__() method
'''

def INDENT(n=0) -> str:
    result = "|"
    for _ in range(n):
        result += "  " + "|"
    return result + "__"

class ReturnStatement:
    def __init__(self):
        self.expr = None
    def print(self, indent = 1):
        print(f"return {self.__str__()}")
    def __str__(self):
        return f"{self.expr}"
    def __len__(self):
        return 1

class PrefixExpression:
    def __init__(self):
        self.op = None
        self.right = None
    def print(self, indent = 1):
        print(f"prefix: {self.__str__()}")
    def __str__(self):
        return f"({self.op} {self.right})"
    def __len__(self):
        return 1

class InfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
        self.right = None
    def print(self, indent = 1):
        print(f"infix: {self.__str__()}")
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"
    def __len__(self):
        return 1

class PostfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
    def print(self, indent = 1):
        print(f"postfix: {self.__str__()}")
    def __str__(self):
        return f"{self.left} {self.op}"
    def __len__(self):
        return 1

class StringFmt:
    def __init__(self):
        self.start = None
        self.mid = []
        self.exprs = []
        self.end = None
    def print(self, indent = 1):
        print(f"string fmt: {self.__str__()}")
    def __str__(self):
        return f"{self.start}{''.join([f'{m}{e}' for m,e in zip(self.mid, self.exprs)])}{self.end}"
    def __len__(self):
        return 1

class ArrayLiteral:
    def __init__(self):
        self.elements = []
    def print(self, indent = 1):
        print(f"{INDENT(indent)} array: {self.__str__()}")
    def __str__(self):
        return f"[{', '.join([str(e) for e in self.elements])}]"
    def __len__(self):
        return len(self.elements)
    def __iter__(self):
        return iter(self.elements)

class ArrayDeclaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.size = []
        self.length = []
        self.dimension = 0
        self.is_const: bool = False

    def print(self, indent = 1):
        print(f"{INDENT(indent)} declare array: ", end='')
        self.id.print(indent)
        print(f"{INDENT(indent)} type: ", end='')
        self.dtype.print(indent)
        if self.is_const:
            print(f"{INDENT(indent)} constant")
        if self.dimension:
            print(f"{INDENT(indent)} dimension: {self.dimension}")
        if self.size:
            print(f"{INDENT(indent)} size:")
            for s in self.size:
                print(f"{INDENT(indent+1)} ", end='')
                s.print(indent+1)
        if self.value:
            print(f"{INDENT(indent)} value:")
            self.value.print(indent+1)
        if self.length:
            print(f"{INDENT(indent)} length:")
            for l in self.length:
                print(f"{INDENT(indent+1)} {l}")

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

        tmp = self.value
        compute_lengths(tmp, 0)

class Assignment:
    def __init__(self):
        self.id = None
        self.value = None
    def print(self, indent = 1):
        print(f"assign: {self.__str__()}")
    def __str__(self):
        return f"{self.id} = {self.value}"
    def __len__(self):
        return 1

class Declaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False

    def print(self, indent = 1):
        print(f"{INDENT(indent)} declare: ", end='')
        self.id.print(indent)
        print(f"{INDENT(indent)} type: ", end='')
        self.dtype.print(indent)
        if self.value:
            print(f"{INDENT(indent)} value: ", end='')
            self.value.print(indent)
        if self.is_const:
            print(f"{INDENT(indent)} constant")

class FnCall:
    def __init__(self):
        self.id = None
        self.args = []

    def print(self, _ = 1):
        print(f"call: {self.__str__()}")
    def __str__(self):
        return f"{self.id}({', '.join([str(a) for a in self.args])})"
    def __len__(self):
        return 1

class IfExpression:
    def __init__(self):
        self.condition = None
        self.then = None
        self.else_if: list[ElseIfExpression] = []
        self.else_block = None

    def print(self, indent = 1):
        print(f"{INDENT(indent)} if statement:")
        print(f"{INDENT(indent+1)} condition: ", end='')
        self.condition.print(indent)
        print(f"{INDENT(indent+1)} then:")
        self.then.print(indent+2)
        for e in self.else_if:
            print(f"{INDENT(indent+1)} else if statement:")
            print(f"{INDENT(indent+2)} condition: ", end='')
            e.condition.print(indent+2)
            print(f"{INDENT(indent+2)} then:")
            e.then.print(indent+2)
        if self.else_block:
            print(f"{INDENT(indent+1)} else:")
            self.else_block.print(indent+2)

class ElseIfExpression:
    def __init__(self):
        self.condition = None
        self.then = None

class BlockStatement:
    def __init__(self):
        self.statements = []
    def print(self, indent = 1):
        print(f"{INDENT(indent)} block:")
        for s in self.statements:
            s.print(indent+1)

class Function:
    def __init__(self):
        self.id = None
        self.rtype = None
        self.params: list = []
        self.body: list = []

class Class:
    def __init__(self):
        self.id = None
        self.params: list = []
        self.body: list = []
        self.properties: list = []
        self.methods: list = []

class Program:
    'the root node of the syntax tree'
    def __init__(self):
        self.globals: list = []
        self.functions: list = []
        self.classes: list = []

    def print(self, indent = 1):
        print("globals:")
        for g in self.globals:
            g.print(0)
        print("functions:")
        for fn in self.functions:
            print(f"{' ' * (indent*4)}{fn}")
        print("classes:")
        for c in self.classes:
            print(f"{' ' * (indent*4)}{c}")
