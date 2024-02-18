'''
All productions must have an __str__() method
'''

class PrefixExpression:
    def __init__(self):
        self.op = None
        self.right = None

    def __str__(self):
        return f"{self.op} {self.right}"

class InfixExpression:
    def __init__(self):
        self.left = None
        self.op = None
        self.right = None
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

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

class ArrayLiteral:
    def __init__(self):
        self.elements = []
    def __str__(self):
        result = "{"
        for e in self.elements:
            result += f"{e}, "
        return result[:-2] + "}"

class ArrayDeclaration:
    def __init__(self):
        self.id = None
        self.dtype = None
        self.value = None
        self.size = None
        self.length = None
        self.is_const: bool = False

    def __str__(self, indent = 0):
        result =  f"declare: {self.id}\n"
        result += f"{' ' * (indent+4)}type: {self.dtype}\n"
        if self.value:
            result += f"{' ' * (indent+4)}value: {self.value}\n"
        if self.size is not None:
            result += f"{' ' * (indent+4)}size: {self.size}\n"
        if self.length is not None:
            result += f"{' ' * (indent+4)}length: {self.length}\n"
        if self.is_const:
            result += f"{' ' * (indent+4)}constant\n"
        return result

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

