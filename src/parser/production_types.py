from abc import ABC, abstractmethod
from src.lexer import Token

### BASE CLASS
class Production(ABC): ... # to avoid undefined Production error in type hint
class Production(ABC):
    @abstractmethod
    def string(self, indent = 0) -> str: ...
    @abstractmethod
    def header(self) -> str: ...
    @abstractmethod
    def child_nodes(self) -> None | dict[str, Production | Token]: ...
    @abstractmethod
    def python_string(self, indent = 0, cwass=False) -> str: ...
    @abstractmethod
    def formatted_string(self, indent=0) -> str: ...

class Statement(Production):
    'for productions that can be in blocks'
    def string(self, indent = 0) -> str: ...
    def header(self) -> str: ...
    def child_nodes(self) -> None | dict[str, Production | Token]: ...
    def python_string(self, indent = 0, cwass=False) -> str: ...
    def formatted_string(self, indent=0) -> str: ...

class Value(Production):
    'for productions that evaluate to a value'
    def string(self, indent = 0) -> str: ...
    def header(self) -> str: ...
    def child_nodes(self) -> None | dict[str, Production | Token]: ...
    def flat_string(self) -> str: ...
    def python_string(self, indent = 0, cwass=False) -> str: ...
    def formatted_string(self, indent=0) -> str: ...

class ValueRequirements(Value):
    'interface for Value'
    @abstractmethod
    def flat_string(self) -> str: ...
class Expression(ValueRequirements):
    '''
    for values that have operands
    eg. id + id, id - id, fn_call() * id, id[1] / id
    '''
    def string(self, indent = 0) -> str: ...
    def header(self) -> str: ...
    def child_nodes(self) -> None | dict[str, Production | Token]: ...
    def flat_string(self) -> str: ...
    def python_string(self, indent = 0, cwass=False) -> str: ...
    def formatted_string(self, indent=0) -> str: ...

class Unit(ValueRequirements):
    '''
    for values that don't have operands
    eg. identifier, identifier[2], "string", ident.property
    fnCall(), "string | fmt | !"
    '''
    def string(self, indent = 0) -> str: ...
    def header(self) -> str: ...
    def child_nodes(self) -> None | dict[str, Production | Token]: ...
    def flat_string(self) -> str: ...
    def python_string(self, indent = 0, cwass=False) -> str: ...
    def formatted_string(self, indent=0) -> str: ...

class Iterable(ValueRequirements):
    '''
    for Units that can: contain other Productions, and/or be subsliced
    eg. arrays, string fmts, and string literals
    '''
    def string(self, indent = 0) -> str: ...
    def header(self) -> str: ...
    def child_nodes(self) -> None | dict[str, Production | Token]: ...
    def flat_string(self) -> str: ...
    def python_string(self, indent = 0, cwass=False) -> str: ...
    def formatted_string(self, indent=0) -> str: ...

class IdentifierProds(ValueRequirements):
    '''
    for Units that are identifiers
    eg. identifiers, identifier[2], fnCall(), ident.property
    '''
    def string(self, indent = 0) -> str: ...
    def header(self) -> str: ...
    def child_nodes(self) -> None | dict[str, Production | Token]: ...
    def flat_string(self) -> str: ...
    def python_string(self, indent = 0, cwass=False) -> str: ...
    def formatted_string(self, indent=0) -> str: ...
