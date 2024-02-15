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

    def as_iter(self):
        yield f"{self.id.lexeme}"
        yield f"{TREE_INDENT}return type: {self.dtype.lexeme}"
        if self.params:
            yield f"{TREE_INDENT}params:"
            for param in self.params:
                yield f"{TREE_INDENT}{param.token}"
        if self.body:
            yield f"{TREE_INDENT}body:"
            for stmt in self.body:
                yield f"{TREE_INDENT}{stmt.token}"

class Cwass:
    id: Token
    params: list[Token]
    properties: list[Token]
    methods: list[Fwunc]
    body: list[Token]

    def as_iter(self):
        yield f"id: {self.id.lexeme}"
        if self.params:
            yield f"params:"
            for param in self.params:
                yield f"\t{param.token}"
        if self.body:
            yield f"body:"
            for stmt in self.body:
                yield f"\t{stmt.token}"
        if self.properties:
            yield f"properties:"
            for prop in self.properties:
                yield f"\t{prop.token}"
        if self.methods:
            yield f"methods:"
            for method in self.methods:
                yield f"\t{method}"

class GwobawDec:
    pass

class Program:
    fwuncs: list[Fwunc] = []
    cwass: list[Cwass] = []
    gwobaws: list[GwobawDec] = []

    def print(self):
        print("Fwuncs:")
        for fwunc in self.fwuncs:
            for j in fwunc.as_iter():
                print(j)
            print()
        print()

        print("Cwass:")
        # todo
        print("Gwobaws:")
        # todo
