# BASE CLASS
class Type:
    def __init__(self, _): raise NotImplementedError
    # SHAPE
    def __len__(self): raise NotImplementedError
    def __repr__(self) -> str: raise NotImplementedError
    def __nonzero__(self): raise NotImplementedError
    # OPERATOR OVERLOADING
    def __eq__(self, _) -> bool: raise NotImplementedError
    def __ne__(self, _) -> bool: raise NotImplementedError
    # TYPE CONVERSION
    def __bool__(self): raise NotImplementedError
    def __str__(self): raise NotImplementedError
    def __int__(self): raise NotImplementedError
    def __float__(self): raise NotImplementedError

# NUMBERS
class Int(Type): ...
class Float(Type): ...
class Bool(Type): ...

# ITERABLES
class String(Type): ...
class Array(Type): ...
