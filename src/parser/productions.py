'''
All productions must have an as_iter() method
'''

class Declaration:
    id = None
    dtype = None
    value = None
    is_const: bool = False

    def __str__(self, indent = 0):
        result =  f"declare: {self.id.lexeme}\n"
        result += f"{' ' * (indent+4)}type: {self.dtype.lexeme}\n"
        if self.value:
            result += f"{' ' * (indent+4)}value: {self.value.lexeme}\n"
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
