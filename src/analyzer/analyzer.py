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
        self.compile_global_names()
        self.analyze_program()

    def analyze_program(self) -> None:
        for func in self.program.functions:
            self.analyze_function(func)

    def compile_global_names(self) -> None:
        '''
        populates the self.global_names dict with the unique global names
        '''
        self.global_names: dict[str, tuple[Token, GlobalType]] = {}
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

    def analyze_class(self, cwass: Class) -> bool:
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
            case Token():
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
            case Expression():
                return self.analyze_expression(ret.expr, local_defs)
            case IdentifierProds():
                return self.analyze_ident_prods(ret.expr, local_defs)
            case Collection():
                return self.analyze_collection(ret.expr, local_defs)
            case _:
                raise ValueError(f"Unknown return expression: {ret.expr}")

    def analyze_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        # check if defined in local def 
        if not ident_prod.id.string() in local_defs:
            self.errors.append(UndefinedError(
                ident_prod.id,
            ))
            return False

        match ident_prod:
            case IndexedIdentifier():
                raise NotImplementedError
            case FnCall():
                raise NotImplementedError
            case ClassConstructor():
                raise NotImplementedError
            case ClassAccessor():
                raise NotImplementedError
        return True

    def analyze_collection(self, collection: Collection, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        match collection:
            case ArrayLiteral():
                return self.analyze_array_literal(collection, local_defs)
            case StringFmt():
                return self.analyze_string_fmt(collection, local_defs)
            case _:
                raise ValueError(f"Unknown collection: {collection}")

    def analyze_array_literal(self, array_literal: ArrayLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        for elem in array_literal.elements:
            match elem:
                case Token():
                    match elem.token:
                        case UniqueTokenType():
                            if not elem.string() in local_defs:
                                self.errors.append(UndefinedError(
                                    elem,
                                ))
                                return False
                case Expression():
                    return self.analyze_expression(elem, local_defs)
                case IdentifierProds():
                    return self.analyze_ident_prods(elem, local_defs)
                case Collection():
                    return self.analyze_collection(elem, local_defs)
                case _:
                    raise ValueError(f"Unknown array element: {elem}")
        return True
    
    def analyze_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        raise NotImplementedError

    def analyze_string_fmt(self, string_fmt: StringFmt, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        raise NotImplementedError

    def analyze_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> bool:
        match token.token:
            case TokenType.STRING_LITERAL | TokenType.INT_LITERAL | TokenType.FLOAT_LITERAL | TokenType.FAX | TokenType.CAP | TokenType.NUWW:
                return True
            case UniqueTokenType():
                if token.string() in local_defs:
                    return True
                else:
                    self.errors.append(UndefinedError(
                        token,
                    ))
                    return False
            case _:
                raise ValueError(f"Unknown token: {token}")
