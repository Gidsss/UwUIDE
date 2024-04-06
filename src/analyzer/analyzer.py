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
        any duplicates will be appended to error
        '''
        self.global_names: dict[str, tuple[Token, GlobalType]] = {}
        for global_dec in self.program.globals:
            if global_dec.id.string() in self.global_names:
                self.errors.append(DuplicateDefinitionError(
                    *self.global_names[global_dec.id.string()],
                    global_dec.id,
                    GlobalType.IDENTIFIER,
                ))
            else:
                self.global_names[global_dec.id.string()] = (global_dec.id, GlobalType.IDENTIFIER)
        for func in self.program.functions:
            if func.id.string() in self.global_names:
                self.errors.append(DuplicateDefinitionError(
                    *self.global_names[func.id.string()],
                    func.id,
                    GlobalType.FUNCTION,
                ))
            else:
                self.global_names[func.id.string()] = (func.id, GlobalType.FUNCTION)
        for cwass in self.program.classes:
            if cwass.id.string() in self.global_names:
                self.errors.append(DuplicateDefinitionError(
                    *self.global_names[cwass.id.string()],
                    cwass.id,
                    GlobalType.CLASS,
                ))
            else:
                self.global_names[cwass.id.string()] = (cwass.id, GlobalType.CLASS)

    def analyze_function(self, fn: Function) -> None:
        '''
        must pass in a fn production
        if error, will not raise. just append to errors
        '''
        local_defs: dict[str, tuple[Token, GlobalType]] = self.global_names.copy()
        for p in fn.params:
            self.analyze_param(p, local_defs)
        assert isinstance(fn.body, BlockStatement)
        self.analyze_body(fn.body, local_defs)

    def analyze_class(self, cwass: Class) -> None:
        '''
        must pass in a class production
        if error, will not raise. just append to errors
        '''
        # parse params
        # parse methods (use self.analyze_function)
        raise NotImplementedError

    def analyze_body(self, body: BlockStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
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
                    self.analyze_return(stmt, local_defs)
                case _:
                    raise ValueError(f"Unknown statement: {stmt}")

    def analyze_param(self, param: Parameter, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        must pass in a param production
        will return a param id to be used for local_defs dict
        '''
        assert isinstance(param.id, Token)
        if param.id.string() in local_defs:
            self.errors.append(DuplicateDefinitionError(
                *local_defs[param.id.string()],
                param.id,
                GlobalType.LOCAL_DEF,
            ))
        else:
            local_defs[param.id.string()] = (param.id, GlobalType.LOCAL_DEF)

    def analyze_args(self, args: list[Production], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        must pass in a list of args in a fn/method call
        returns true if no errors in analysis, false otherwise
        '''
        for arg in args:
            match arg:
                case Expression():
                    self.analyze_expression(arg, local_defs)
                case IdentifierProds():
                    self.analyze_ident_prods(arg, local_defs)
                case Collection():
                    self.analyze_collection(arg, local_defs)
                case Token():
                    self.analyze_token(arg, local_defs)

    def analyze_return(self, ret: ReturnStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        must pass in a return production
        if error, will not raise. just append to errors
        return true if no errors, false otherwise
        '''
        match ret.expr:
            case Token():
                self.analyze_token(ret.expr, local_defs)
            case Expression():
                self.analyze_expression(ret.expr, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(ret.expr, local_defs)
            case Collection():
                self.analyze_collection(ret.expr, local_defs)
            case _:
                raise ValueError(f"Unknown return expression: {ret.expr}")

    def analyze_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Token, GlobalType]],
                            access_depth: int = 1) -> None:
        match ident_prod:
            case IndexedIdentifier():
                match ident_prod.id:
                    case Token():
                        self.analyze_token(ident_prod.id, local_defs)
                    case FnCall():
                        raise NotImplementedError
                self.analyze_array_indices(ident_prod.index, local_defs)
            case FnCall():
                match ident_prod.id:
                    case Token():
                        self.analyze_token(ident_prod.id, local_defs)
                self.analyze_args(ident_prod.args, local_defs)
            case ClassConstructor():
                self.analyze_args(ident_prod.args, local_defs)
            case ClassAccessor():
                if access_depth > 0:
                    match ident_prod.id:
                        case Token():
                            self.analyze_token(ident_prod.id, local_defs)
                        case FnCall():
                            self.analyze_ident_prods(ident_prod.id, local_defs)
                match ident_prod.accessed:
                    case FnCall():
                        self.analyze_args(ident_prod.accessed.args, local_defs)
                    case IndexedIdentifier():
                        self.analyze_array_indices(ident_prod.accessed.index, local_defs)
                    case ClassAccessor():
                        self.analyze_ident_prods(ident_prod.accessed, local_defs, access_depth=access_depth+1)
            case _:
                raise ValueError(f"Unknown identifier production: {ident_prod}")

    def analyze_collection(self, collection: Collection, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match collection:
            case ArrayLiteral():
                self.analyze_array_literal(collection, local_defs)
            case StringFmt():
                self.analyze_string_fmt(collection, local_defs)
            case _:
                raise ValueError(f"Unknown collection: {collection}")

    def analyze_array_literal(self, array_literal: ArrayLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for elem in array_literal.elements:
            match elem:
                case Token():
                    self.analyze_token(elem, local_defs)
                case Expression():
                    self.analyze_expression(elem, local_defs)
                case IdentifierProds():
                    self.analyze_ident_prods(elem, local_defs)
                case Collection():
                    self.analyze_collection(elem, local_defs)
                case _:
                    raise ValueError(f"Unknown array element: {elem}")
    
    def analyze_array_indices(self, index_list: list[Production], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for idx in index_list:
            match idx:
                case Expression():
                    self.analyze_expression(idx, local_defs)
                case IdentifierProds():
                    self.analyze_ident_prods(idx, local_defs)
                case Token():
                    self.analyze_token(idx, local_defs)
    
    def analyze_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match expr:
            case PrefixExpression():
                match expr.right:
                    case Expression():
                        self.analyze_expression(expr.right, local_defs)
                    case Collection():
                        self.analyze_collection(expr.right, local_defs)
                    case Token():
                        self.analyze_token(expr.right, local_defs)
            case PostfixExpression():
                match expr.left:
                    case Expression():
                        self.analyze_expression(expr.left, local_defs)
                    case Collection():
                        self.analyze_collection(expr.right, local_defs)
                    case Token():
                        self.analyze_token(expr.left, local_defs)
            case InfixExpression():
                match expr.left:
                    case Expression():
                        self.analyze_expression(expr.left, local_defs)
                    case Collection():
                        self.analyze_collection(expr.right, local_defs)
                    case Token():
                        self.analyze_token(expr.left, local_defs)
                match expr.right:
                    case Expression():
                        self.analyze_expression(expr.right, local_defs)
                    case Collection():
                        self.analyze_collection(expr.right, local_defs)
                    case Token():
                        self.analyze_token(expr.right, local_defs)
            case _:
                raise ValueError(f"Unknown expression: {expr}")

    def analyze_string_fmt(self, string_fmt: StringFmt, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for expr in string_fmt.exprs:
            match expr:
                case Expression():
                    self.analyze_expression(expr, local_defs)
                case IdentifierProds():
                    self.analyze_ident_prods(expr, local_defs)
                case Token():
                    self.analyze_token(expr, local_defs)

    def analyze_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match token.token:
            case TokenType.STRING_LITERAL | TokenType.INT_LITERAL | TokenType.FLOAT_LITERAL | TokenType.FAX | TokenType.CAP | TokenType.NUWW:
                pass
            case UniqueTokenType():
                if token.string() in local_defs:
                    pass
                else:
                    self.errors.append(UndefinedError(
                        token,
                    ))
            case _:
                raise ValueError(f"Unknown token: {token}")
