'''
All productions must have an __str__() method
'''

def INDENT(n=0) -> str:
    return "    " * n

class ReturnStatement:
    def __init__(self):
        self.expr = None
    def print(self, indent = 1):
        print(f"{INDENT(indent)} return {self.__str__()}")
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
        print(f"string fmt: ")
        print(f"{INDENT(indent+1)}", end='')
        self.start.print(indent)
        if self.exprs:
            print(f"{INDENT(indent+1)}", end='')
            self.exprs[0].print(indent)
        for m,e in zip(self.mid, self.exprs[1:]):
            print(f"{INDENT(indent+1)}", end='')
            m.print(indent)
            print(f"{INDENT(indent+1)}", end='')
            e.print(indent)

        print(f"{INDENT(indent+1)}", end='')
        self.end.print(indent)


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
        self.is_const: bool = False

    def print(self, indent = 1):
        print(f"{INDENT(indent)} declare array: ", end='')
        self.id.print(indent)
        print(f"{INDENT(indent+1)} type: ", end='')
        self.dtype.print(indent+1)
        if self.is_const:
            print(f"{INDENT(indent+1)} constant")
        if self.value:
            print(f"{INDENT(indent+1)} value:")
            self.value.print(indent+2)

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
        print(f"{INDENT(indent)} assign: ", end='')
        self.id.print(indent)
        print(f"{INDENT(indent+1)} value: ", end='')
        self.value.print(indent)
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
        print(f"{INDENT(indent+1)} type: ", end='')
        self.dtype.print(indent+1)
        if self.value:
            print(f"{INDENT(indent+1)} value: ", end='')
            self.value.print(indent+1)
        if self.is_const:
            print(f"{INDENT(indent+1)} constant")

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
        print(f"{INDENT(indent+1)}")
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

class WhileLoop:
    def __init__(self):
        self.condition = None
        self.body = None
        self.is_do = False
    def print(self, indent = 1):
        print(f"{INDENT(indent)}{f'do' if self.is_do else ''} while statement:")
        print(f"{INDENT(indent+1)} condition: ", end='')
        self.condition.print(indent)
        print(f"{INDENT(indent+1)} body:")
        self.body.print(indent+2)

class ForLoop:
    def __init__(self):
        self.init = None # can be declaration or just an ident
        self.condition = None
        self.update = None
        self.body = None
    def print(self, indent = 1):
        print(f"{INDENT(indent)} for statement:")
        print(f"{INDENT(indent+1)} init: ", end='')
        if isinstance(self.init, Declaration) or isinstance(self.init, Assignment):
            print()
            self.init.print(indent+2)
        else:
            self.init.print(indent)

        print(f"{INDENT(indent+1)} condition: ", end='')
        self.condition.print(indent)
        print(f"{INDENT(indent+1)} update: ", end='')
        self.update.print(indent)
        print(f"{INDENT(indent+1)} body:")
        self.body.print(indent+2)

class Print:
    def __init__(self):
        self.values = []
    def print(self, indent = 1):
        print(f"{INDENT(indent)} print:")
        for v in self.values:
            print(f"{INDENT(indent+1)} ", end='')
            v.print(indent+1)
        print()

class Input:
    def __init__(self):
        self.value = None
    def print(self, indent = 1):
        print(f"{INDENT(indent)} input: ", end='')
        self.value.print(indent)

class Function:
    def __init__(self):
        self.id = None
        self.rtype = None
        self.params: list[Parameter] = []
        self.body = None

    def print(self, indent = 1):
        print(f"{INDENT(indent)} function: ", end='')
        self.id.print(indent)
        print(f"{INDENT(indent + 1)} rtype: ", end='')
        self.rtype.print(indent)

        if self.params:
            print(f"{INDENT(indent + 1)} parameters:")
            for param in self.params:
                param.print(indent+2)
        else:
            print(f"{INDENT(indent + 1)} parameters: None")


        print(f"{INDENT(indent + 1)} body:")
        self.body.print(indent + 2)

class Parameter:
    def __init__(self):
        self.id = None
        self.dtype = None

    def print(self, indent = 1):
        print(f"{INDENT(indent)} param: ", end="")
        self.id.print(indent)
        print(f"{INDENT(indent+1)} dtype: ", end='')
        self.dtype.print(indent)

class Class:
    def __init__(self):
        self.id = None
        self.params: list = []
        self.body: list = []
        self.properties: list = []
        self.methods: list = []

class BlockStatement:
    def __init__(self):
        self.statements = []
    def print(self, indent = 1):
        print(f"{INDENT(indent)} block:")
        for s in self.statements:
            s.print(indent+1)

class Program:
    'the root node of the syntax tree'
    def __init__(self):
        self.mainuwu = None
        self.globals: list = []
        self.functions: list = []
        self.classes: list = []

    def print(self, indent = 1):
        print("MAINUWU:")
        self.mainuwu.print(indent)
        print("\nGLOBALS:")
        for g in self.globals:
            g.print(1)
            print()
        print("\nFUNCTIONS:")
        for fn in self.functions:
            fn.print(1)
            print()
        print("\nCLASSES:")
        for c in self.classes:
            print(f"{' ' * (indent*4)}{c}")
            print()
