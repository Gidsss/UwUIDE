from src.lexer.token import TokenType
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
        if not (res := self.compile_global_names()):
            return None
        self.global_names = res

    def compile_global_names(self) -> dict[str, tuple[Token, GlobalType]] | None:
        '''
        returns a global_names dict with the names of all globals in the program
        returns None if there are any errors
        '''
        global_names: dict[str, tuple[Token, GlobalType]] = {}
        for global_dec in self.program.globals:
            try:
                global_names[global_dec.id.string()]
                self.errors.append(DuplicateDefinitionError(
                    *global_names[global_dec.id.string()],
                    global_dec.id,
                    GlobalType.IDENTIFIER,
                ))
            except KeyError:
                global_names[global_dec.id.string()] = (global_dec.id, GlobalType.IDENTIFIER)
        for func in self.program.functions:
            try:
                global_names[func.id.string()]
                self.errors.append(DuplicateDefinitionError(
                    *global_names[func.id.string()],
                    func.id,
                    GlobalType.FUNCTION,
                ))
            except KeyError:
                global_names[func.id.string()] = (func.id, GlobalType.FUNCTION)
        for cwass in self.program.classes:
            try:
                global_names[cwass.id.string()]
                self.errors.append(DuplicateDefinitionError(
                    *global_names[cwass.id.string()],
                    cwass.id,
                    GlobalType.CLASS,
                ))
            except KeyError:
                global_names[cwass.id.string()] = (cwass.id, GlobalType.CLASS)

        if self.errors:
            return None
        else:
            return global_names

    def analyze_function(self, fn: Function) -> None:
        '''
        must pass in a fn production
        if error, will not raise. just append to errors
        '''
        local_defs: dict[str, tuple[Token, GlobalType]] = self.global_names.copy()
        # parse params
        # parse statements

        raise NotImplementedError

    def analyze_class(self, cwass: Class) -> None:
        '''
        must pass in a class production
        if error, will not raise. just append to errors
        '''
        # parse params
        # parse methods (use self.analyze_function)
        raise NotImplementedError

    def analyze_param(self, param: Parameter) -> None:
        '''
        must pass in a param production
        will return a param id to be used for local_defs dict
        '''
        raise NotImplementedError

    def analyze_return(self, ret: ReturnStatement, expected_type: TokenType) -> None:
        raise NotImplementedError
