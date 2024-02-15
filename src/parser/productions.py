from src.lexer.token import Token

'''
All productions must have an as_iter() method
'''

class Program:
    statements: list[Token] = []

    def print(self):
        for statement in self.statements:
            print(statement)
