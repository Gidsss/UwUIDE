from src.lexer.token import TokenType, UniqueTokenType
from src.analyzer.error_handler import DuplicateDefinitionError, GlobalType, UndefinedError
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
        for func in self.program.functions:
            self.analyze_function(func)

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

    def analyze_function(self, fn: Function) -> bool:
        '''
        must pass in a fn production
        if error, will not raise. just append to errors
        '''
        local_defs: dict[str, tuple[Token, GlobalType]] = self.global_names.copy()
        # parse params
        for p in fn.params:
            if not self.analyze_param(p, local_defs):
                return False
        # parse statements
        assert isinstance(fn.body, BlockStatement)
        if not self.analyze_body(fn.body, local_defs):
            return False
        return True

    def analyze_class(self, cwass: Class) -> None:
        '''
        must pass in a class production
        if error, will not raise. just append to errors
        '''
        # parse params
        # parse methods (use self.analyze_function)
        raise NotImplementedError

    def analyze_body(self, body: BlockStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        for stmt in body.statements:
            match stmt:
                case Print():
                    raise NotImplementedError
                case Input():
                    raise NotImplementedError
                case Declaration() | ArrayDeclaration():
                    raise NotImplementedError
                case Assignment():
                    raise NotImplementedError
                case IfStatement():
                    raise NotImplementedError
                case ElseIfStatement():
                    raise NotImplementedError
                case ElseStatement():
                    raise NotImplementedError
                case WhileLoop():
                    raise NotImplementedError
                case ForLoop():
                    raise NotImplementedError
                case ReturnStatement():
                    if not self.analyze_return(stmt, local_defs):
                        return False
                case _:
                    raise ValueError(f"Unknown statement: {stmt}")
        return True

    def analyze_param(self, param: Parameter, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        '''
        must pass in a param production
        will return a param id to be used for local_defs dict
        '''
        assert isinstance(param.id, Token)
        try:
            local_defs[param.id.string()]
            self.errors.append(DuplicateDefinitionError(
                *local_defs[param.id.string()],
                param.id,
                GlobalType.LOCAL_ANY,
            ))
            return False
        except KeyError:
            local_defs[param.id.string()] = (param.id, GlobalType.LOCAL_ANY)
            return True

    def analyze_return(self, ret: ReturnStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        '''
        must pass in a return production
        if error, will not raise. just append to errors
        return true if no errors, false otherwise
        '''
        match ret.expr:
            case Expression():
                raise NotImplementedError
            case IdentifierProds():
                return self.analyze_ident_prods(ret.expr, local_defs)
            case Collection():
                return self.analyze_collection(ret.expr, local_defs)
            case Token():
                # raise Exception(ret.expr.token)
                match ret.expr.token:
                    case TokenType.STRING_LITERAL | TokenType.INT_LITERAL | TokenType.FLOAT_LITERAL | TokenType.FAX | TokenType.CAP | TokenType.NUWW:
                        return True
                    case UniqueTokenType():
                        # check if defined in local def 
                        if ret.expr.string() in local_defs:
                            return True
                        else:
                            self.errors.append(UndefinedError(
                                ret.expr,
                            ))
                            return False
            case _:
                raise ValueError(f"Unknown return expression: {ret.expr}")

