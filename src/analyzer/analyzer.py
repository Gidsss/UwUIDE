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
        for cwass in self.program.classes:
            self.analyze_class(cwass)

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
        local_defs: dict[str, tuple[Token, GlobalType]] = self.global_names.copy()
        for p in fn.params:
            self.analyze_param(p, local_defs)
        assert isinstance(fn.body, BlockStatement)
        self.analyze_body(fn.body, local_defs)

    def analyze_class(self, cwass: Class) -> None:
        local_defs: dict[str, tuple[Token, GlobalType]] = self.global_names.copy()
        for p in cwass.params:
            self.analyze_param(p, local_defs)
        for prop in cwass.properties:
            self.analyze_declaration(prop, local_defs)
        for method in cwass.methods:
            self.analyze_function(method)

    def analyze_param(self, param: Parameter, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
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
        for arg in args:
            match arg:
                case Expression():
                    self.analyze_expression(arg, local_defs)
                case IdentifierProds():
                    self.analyze_ident_prods(arg, local_defs)
                case Collection():
                    self.analyze_collection(arg, local_defs)
                case Token():
                    self.expect_defined_token(arg, local_defs)

    def analyze_body(self, body: BlockStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        when you're calling analyze_body(), make sure to pass in a copy of local_defs
        '''
        for stmt in body.statements:
            match stmt:
                case Print():
                    self.analyze_print(stmt, local_defs)
                case Input():
                    self.analyze_input(stmt, local_defs)
                case Declaration() | ArrayDeclaration():
                    self.analyze_declaration(stmt, local_defs)
                case Assignment():
                    self.analyze_assignment(stmt, local_defs)
                case IfStatement():
                    self.analyze_if(stmt, local_defs)
                case WhileLoop():
                    self.analyze_while_loop(stmt, local_defs)
                case ForLoop():
                    self.analyze_for_loop(stmt, local_defs.copy())
                case ReturnStatement():
                    self.analyze_return(stmt, local_defs)
                case _:
                    raise ValueError(f"Unknown statement: {stmt}")

    ## IN BODY ANALYZERS
    def analyze_print(self, print_stmt: Print, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for val in print_stmt.values:
            match val:
                case Expression():
                    self.analyze_expression(val, local_defs)
                case IdentifierProds():
                    self.analyze_ident_prods(val, local_defs)
                case Collection():
                    self.analyze_collection(val, local_defs)
                case Token():
                    self.expect_defined_token(val, local_defs)

    def analyze_input(self, input_stmt: Input, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match input_stmt.expr:
            case Expression():
                self.analyze_expression(input_stmt.expr, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(input_stmt.expr, local_defs)
            case Collection():
                self.analyze_collection(input_stmt.expr, local_defs)
            case Token():
                self.expect_defined_token(input_stmt.expr, local_defs)

    def analyze_if(self, if_stmt: IfStatement | ElseIfStatement, local_defs: dict[str, tuple[Token, GlobalType]], else_if: bool = False) -> None:
        self.analyze_expression(if_stmt.condition, local_defs)
        self.analyze_body(if_stmt.then, local_defs.copy())
        if else_if: return
        assert isinstance(if_stmt, IfStatement)
        for elif_stmt in if_stmt.else_if:
            self.analyze_if(elif_stmt, local_defs, else_if=True)
        if if_stmt.else_block:
            self.analyze_body(if_stmt.else_block, local_defs.copy())

    def analyze_declaration(self, decl: Declaration | ArrayDeclaration, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.expect_unique_token(decl.id, local_defs)
        match decl.value:
            case Expression():
                self.analyze_expression(decl.value, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(decl.value, local_defs)
            case Collection():
                self.analyze_collection(decl.value, local_defs)
            case Token():
                self.expect_defined_token(decl.value, local_defs)

    def analyze_assignment(self, assign: Assignment, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match assign.id:
            case Token():
                self.expect_defined_token(assign.id, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(assign.id, local_defs)
            case _:
                raise ValueError(f"Unknown assignment left hand side: {assign.id}")
        match assign.value:
            case Expression():
                self.analyze_expression(assign.value, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(assign.value, local_defs)
            case Collection():
                self.analyze_collection(assign.value, local_defs)
            case Token():
                self.expect_defined_token(assign.value, local_defs)

    def analyze_while_loop(self, while_loop: WhileLoop, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.analyze_expression(while_loop.condition, local_defs)
        self.analyze_body(while_loop.body, local_defs.copy())

    def analyze_for_loop(self, for_loop: ForLoop, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        when calling analyze_for_loop(), make sure to pass in a copy of local_defs
        '''
        match for_loop.init:
            case Assignment():
                self.analyze_assignment(for_loop.init, local_defs)
            case Declaration() | ArrayDeclaration():
                self.analyze_declaration(for_loop.init, local_defs)
            case Token():
                self.expect_defined_token(for_loop.init, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(for_loop.init, local_defs)
            case _:
                raise ValueError(f"Unknown for loop init: {for_loop.init}")
        self.analyze_expression(for_loop.condition, local_defs)
        self.analyze_expression(for_loop.update, local_defs)
        self.analyze_body(for_loop.body, local_defs.copy())

    def analyze_return(self, ret: ReturnStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match ret.expr:
            case Token():
                self.expect_defined_token(ret.expr, local_defs)
            case Expression():
                self.analyze_expression(ret.expr, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(ret.expr, local_defs)
            case Collection():
                self.analyze_collection(ret.expr, local_defs)
            case _:
                raise ValueError(f"Unknown return expression: {ret.expr}")

    ## OTHER ANALYZERS
    def analyze_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Token, GlobalType]],
                            access_depth: int = 1) -> None:
        match ident_prod:
            case IndexedIdentifier():
                match ident_prod.id:
                    case Token():
                        self.expect_defined_token(ident_prod.id, local_defs)
                    case FnCall():
                        raise NotImplementedError
                self.analyze_array_indices(ident_prod.index, local_defs)
            case FnCall():
                match ident_prod.id:
                    case Token():
                        self.expect_defined_token(ident_prod.id, local_defs)
                self.analyze_args(ident_prod.args, local_defs)
            case ClassConstructor():
                self.analyze_args(ident_prod.args, local_defs)
            case ClassAccessor():
                if access_depth > 0:
                    match ident_prod.id:
                        case Token():
                            self.expect_defined_token(ident_prod.id, local_defs)
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
        '''
        this is for array literals and string fmt
        try not to use analyze_array_literal or analyze_string_fmt directly and instead use this function
        '''
        match collection:
            case ArrayLiteral():
                self.analyze_array_literal(collection, local_defs)
            case StringFmt():
                self.analyze_string_fmt(collection, local_defs)
            case Input():
                self.analyze_input(collection, local_defs)
            case _:
                raise ValueError(f"Unknown collection: {collection}")

    def analyze_array_literal(self, array_literal: ArrayLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        try not to use this method directly.
        use analyze_collection instead
        '''
        for elem in array_literal.elements:
            match elem:
                case Token():
                    self.expect_defined_token(elem, local_defs)
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
                    self.expect_defined_token(idx, local_defs)
    
    def analyze_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match expr:
            case PrefixExpression():
                match expr.right:
                    case Expression():
                        self.analyze_expression(expr.right, local_defs)
                    case Collection():
                        self.analyze_collection(expr.right, local_defs)
                    case IdentifierProds():
                        self.analyze_ident_prods(expr.right, local_defs)
                    case Token():
                        self.expect_defined_token(expr.right, local_defs)
            case PostfixExpression():
                match expr.left:
                    case Expression():
                        self.analyze_expression(expr.left, local_defs)
                    case Collection():
                        self.analyze_collection(expr.left, local_defs)
                    case IdentifierProds():
                        self.analyze_ident_prods(expr.left, local_defs)
                    case Token():
                        self.expect_defined_token(expr.left, local_defs)
            case InfixExpression():
                match expr.left:
                    case Expression():
                        self.analyze_expression(expr.left, local_defs)
                    case Collection():
                        self.analyze_collection(expr.left, local_defs)
                    case IdentifierProds():
                        self.analyze_ident_prods(expr.left, local_defs)
                    case Token():
                        self.expect_defined_token(expr.left, local_defs)
                match expr.right:
                    case Expression():
                        self.analyze_expression(expr.right, local_defs)
                    case Collection():
                        self.analyze_collection(expr.right, local_defs)
                    case IdentifierProds():
                        self.analyze_ident_prods(expr.right, local_defs)
                    case Token():
                        self.expect_defined_token(expr.right, local_defs)
            case _:
                raise ValueError(f"Unknown expression: {expr}")

    def analyze_string_fmt(self, string_fmt: StringFmt, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        try not to use this method directly.
        use analyze_collection instead
        '''
        for expr in string_fmt.exprs:
            match expr:
                case Expression():
                    self.analyze_expression(expr, local_defs)
                case IdentifierProds():
                    self.analyze_ident_prods(expr, local_defs)
                case Token():
                    self.expect_defined_token(expr, local_defs)

    ## HELPER METHODS
    def expect_defined_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        checks whether the token is defined in the scope
        if not, appends to errors
        '''
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
    def expect_unique_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        checks whether the token is not yet defined in the scope
        if already defined (duplicate), appends to errors
        '''
        match token.token:
            case UniqueTokenType():
                if token.string() in local_defs:
                    self.errors.append(DuplicateDefinitionError(
                        *local_defs[token.string()],
                        token,
                        GlobalType.LOCAL_DEF,
                    ))
                else:
                    local_defs[token.string()] = (token, GlobalType.LOCAL_DEF)
            case _:
                raise ValueError(f"Unknown token: {token}")
