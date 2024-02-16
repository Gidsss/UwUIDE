'''
All productions must have an __str__() method
'''

class PrefixExpression:
    prefix_tok = None
    op = None
    right = None
    def __str__(self):
        return f"{self.op}, {self.right.lexeme}"

class ExpressionStatement:
    expression = None

class ArrayLiteral:
    elements = []
    def __str__(self):
        result = "{"
        for e in self.elements:
            result += f"{e.lexeme}, "
        return result[:-2] + "}"

class ArrayDeclaration:
    id = None
    dtype = None
    value = None
    size = None
    length = None
    is_const: bool = False

    def __str__(self, indent = 0):
        result =  f"declare: {self.id.lexeme}\n"
        result += f"{' ' * (indent+4)}type: {self.dtype.lexeme}\n"
        if self.value:
            result += f"{' ' * (indent+4)}value: {self.value.expression}\n"
        if self.size:
            result += f"{' ' * (indent+4)}size: {self.size}\n"
        if self.length:
            result += f"{' ' * (indent+4)}length: {self.length}\n"
        if self.is_const:
            result += f"{' ' * (indent+4)}constant\n"
        return result

class Declaration:
    id = None
    dtype = None
    value = None
    is_const: bool = False

    def __str__(self, indent = 0):
        result =  f"declare: {self.id.lexeme}\n"
        result += f"{' ' * (indent+4)}type: {self.dtype.lexeme}\n"
        if self.value and self.value.expression:
            result += f"{' ' * (indent+4)}value: {self.value.expression}\n"
        if self.is_const:
            result += f"{' ' * (indent+4)}constant\n"
        return result

class Function:
    id = None
    rtype = None
    params: list = []
    body: list = []

class Class:
    id = None
    params: list = []
    body: list = []
    properties: list = []
    methods: list = []

class Program:
    statements: list = []

    def print(self):
        for statement in self.statements:
            print(statement)
