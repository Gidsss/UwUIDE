'''
All productions must have an __str__() method
'''

class ReturnStatement:
    def __init__(self):
        self.expr = None
    def __str__(self):
        return f"return {self.expr}"
    def __len__(self):
        return 1

class PrefixExpression:
    def __init__(self):
        self.op = None
        self.right = None

    def __str__(self):
        return f"{self.op} {self.right}"
    def __len__(self):
        return 1

class InfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
        self.right = None
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"
    def __len__(self):
        return 1

class PostfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
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

    def __str__(self):
        result = f"\"{self.start.lexeme[1:-1]}"
        for m,e in zip(self.mid, self.exprs):
            result += f"| {e} |"
            result += f"{m.lexeme[1:-1]}"
        if self.exprs:
            result += f"| {self.exprs[-1]} |"
        result += f"{self.end.lexeme[1:-1]}\""
        return result
    def __len__(self):
        return 1

class ArrayLiteral:
    def __init__(self):
        self.elements = []
    def __str__(self):
        result = "{"
        for e in self.elements:
            result += f"{e}, "
        return result[:-2] + "}"
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

    def __str__(self, indent = 0):
        result =  f"declare: {self.id}\n"
        result += f"{' ' * (indent+4)}type: {self.dtype}\n"
        if self.value:
            result += f"{' ' * (indent+4)}value: {self.value}\n"
        if self.size:
            result += f"{' ' * (indent+4)}size: {{"
            for i,s in enumerate(self.size):
                if i == len(self.size) - 1:
                    result += f"{s}"
                else:
                    result += f"{s}, "
            result += "}\n"
        if self.length:
            result += f"{' ' * (indent+4)}length: {self.length}\n"
        result += f"{' ' * (indent+4)}dimension: {self.dimension}\n"
        if self.is_const:
            result += f"{' ' * (indent+4)}constant\n"
        return result

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

class Declaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.is_const: bool = False

    def __str__(self, indent = 0):
        result =  f"declare: {self.id}\n"
        result += f"{' ' * (indent+4)}type: {self.dtype}\n"
        if self.value and self.value:
            result += f"{' ' * (indent+4)}value: {self.value}\n"
        if self.is_const:
            result += f"{' ' * (indent+4)}constant\n"
        return result

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

    def __str__(self):
        result = "globals:\n"
        for g in self.globals:
            result += f"{g}\n"
        result += "functions:\n"
        for fn in self.functions:
            result += f"{fn}\n"
        result += "classes:\n"
        for c in self.classes:
            result += f"{c}\n"
        return result

