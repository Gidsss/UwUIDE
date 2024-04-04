from enum import Enum
from src.parser.productions import *

class GlobalName(Enum):
    def __init__(self, name):
        self._name = name
    def __str__(self):
        return self._name

    IDENTIFIER = "IDENTIFIER"
    FUNCTION = "FUNCTION"
    CLASS = "CLASS"

class MemberAnalyzer:
    def __init__(self, program: Program | None) -> None:
        if not program:
            raise Exception("Program is empty!")

        self.program: Program = program
        self.errors = []
        self.warnings = []

        self.global_names: dict[str, GlobalName] = {}
        self.analyze_program()

    def analyze_program(self) -> None:
        for global_dec in self.program.globals:
            try:
                self.global_names[global_dec.id.string()]
                self.duplicate_global_error(global_dec.id, GlobalName.IDENTIFIER)
            except KeyError:
                self.global_names[global_dec.id.string()] = GlobalName.IDENTIFIER
        for func in self.program.functions:
            try:
                self.global_names[func.id.string()]
                self.duplicate_global_error(func.id, GlobalName.FUNCTION)
            except KeyError:
                self.global_names[func.id.string()] = GlobalName.FUNCTION
        for cls in self.program.classes:
            try:
                self.global_names[cls.id.string()]
                self.duplicate_global_error(cls.id, GlobalName.CLASS)
            except KeyError:
                self.global_names[cls.id.string()] = GlobalName.CLASS

    def analyze_functions(self) -> None:
        raise NotImplementedError

    def analyze_classes(self) -> None:
        raise NotImplementedError

    def duplicate_global_error(self, name: Token, dupe: GlobalName) -> None:
        msg = f"Duplicate global: {name}\n"
        msg += f"\tDefined as {self.global_names[name.string()]}\n"
        msg += f"\ttried to redefine as {('another ' if dupe == self.global_names[name.string()] else '') + dupe.name}\n"
        self.errors.append(msg)
