from src.lexer.token import Token

'''
All productions must have an as_iter() method
'''

TREE_INDENT = "|__ "

class Fwunc:
    id: Token
    dtype: Token
    params: list[Token]
    body: list[Token]

    def __str__(self, indent: int = 0):
        result =  f"{' ' * indent}fwunc {self.id.lexeme}\n"
        result += f"{' ' * indent}|__ return type: {self.dtype.lexeme}\n"
        result += f"{' ' * indent}|__ params:"
        if self.params:
            result += "\n"
            for param in self.params:
                result += f"{' ' * (indent+4)}|__ {param.lexeme}\n"
        else:
            result += f" no params\n"

        result += f"{' ' * indent}|__ body:"
        if self.body:
            result += "\n"
            for stmt in self.body:
                result += f"{' ' * (indent+4)}|__ {stmt.lexeme}\n"
        else:
            result += f" no body\n"

        return result

class Cwass:
    id: Token
    params: list[Token]
    properties: list[Token]
    methods: list[Fwunc]
    body: list[Token]

    def __str__(self, indent: int = 0):
        result =  f"{' ' * indent}cwass {self.id.lexeme}\n"
        result += f"{' ' * indent}|__ params:"
        if self.params:
            result += "\n"
            for param in self.params:
                result += f"{' ' * (indent+4)}|__ {param.lexeme}\n"
        else:
            result += f" no params\n"

        result += f"{' ' * indent}|__ properties:"
        if self.properties:
            result += "\n"
            for prop in self.properties:
                result += f"{' ' * (indent+4)}|__ {prop.lexeme}\n"
        else:
            result += f" no properties\n"

        result += f"{' ' * indent}|__ methods:"
        if self.methods:
            result += "\n"
            for method in self.methods:
                result += f"{' ' * (indent+4)}|__ {method}\n"
        else:
            result += f" no methods\n"

        result += f"{' ' * indent}|__ body:"
        if self.body:
            result += "\n"
            for stmt in self.body:
                result += f"{' ' * (indent+4)}|__ {stmt.lexeme}\n"
        else:
            result += f" no body\n"

        return result

class GwobawDec:
    pass

class Program:
    fwuncs: list[Fwunc] = []
    cwass: list[Cwass] = []
    gwobaws: list[GwobawDec] = []

    def print(self):
        print("Fwuncs:")
        for fwunc in self.fwuncs:
            print(fwunc)
        # todo
        print("Cwass:")
        # todo
        print("Gwobaws:")
        # todo
