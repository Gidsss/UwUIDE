from src.analyzer.error_handler import DuplicateDefinitionError, GlobalType
from src.parser.productions import *

class MemberAnalyzer:
    def __init__(self, program: Program | None) -> None:
        if not program:
            raise Exception("Program is empty!")

        self.program: Program = program
        self.errors = []
        self.warnings = []

        self.global_names: dict[str, tuple[Token, GlobalType]] = {}
        self.analyze_program()

    def analyze_program(self) -> None:
        for global_dec in self.program.globals:
            try:
                self.global_names[global_dec.id.string()]
                self.errors.append(DuplicateDefinitionError(
                    *self.global_names[global_dec.id.string()],
                    global_dec.id,
                    GlobalType.IDENTIFIER,
                ))
            except KeyError:
                self.global_names[global_dec.id.string()] = (global_dec.id, GlobalType.IDENTIFIER)
        for func in self.program.functions:
            try:
                self.global_names[func.id.string()]
                self.errors.append(DuplicateDefinitionError(
                    *self.global_names[func.id.string()],
                    func.id,
                    GlobalType.FUNCTION,
                ))
            except KeyError:
                self.global_names[func.id.string()] = (func.id, GlobalType.FUNCTION)
        self.analyze_functions()
        for cwass in self.program.classes:
            try:
                self.global_names[cwass.id.string()]
                self.errors.append(DuplicateDefinitionError(
                    *self.global_names[cwass.id.string()],
                    cwass.id,
                    GlobalType.CLASS,
                ))
            except KeyError:
                self.global_names[cwass.id.string()] = (cwass.id, GlobalType.CLASS)
        self.analyze_classes()

    def analyze_functions(self) -> None:
        raise NotImplementedError

    def analyze_classes(self) -> None:
        raise NotImplementedError
