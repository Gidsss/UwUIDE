from src.lexer.token import Token

'''
All productions must have an as_iter() method
'''

class Declaration:
    id: Token
    dtype: Token
    value: Token

class Function:
    id: Token
    rtype: Token
    params: list = []
    body: list = []

class Class:
    id: Token
    params: list = []
    body: list = []
    properties: list = []
    methods: list = []


class Program:
    statements: list[Token] = []

    def print(self):
        for statement in self.statements:
            print(statement.token)
