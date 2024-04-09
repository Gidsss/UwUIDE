from src.lexer.token import TokenType, UniqueTokenType
from src.analyzer.error_handler import DuplicateDefinitionError, GlobalType, UndefinedError
from src.parser.productions import *

class ClassAnalyzer:
    def __init__(self, cwass: Class) -> None:
        self.cwass: Class = cwass
        self.errors = []
        self.warnings = []

        self.class_members: dict[str, tuple[Token, GlobalType]] = {}
        self.compile_class_members()
        self.analyze_program()

    def analyze_program(self) -> None:
        for method in self.cwass.methods:
            self.analyze_method(method)

    def compile_class_members(self) -> None:
        '''
        populates the self.class_members dict with the unique class members
        any duplicates will be appended to error
        '''
        for param in self.cwass.params:
            if param.id.string() in self.class_members:
                self.errors.append(DuplicateDefinitionError(
                    *self.class_members[param.id.string()],
                    param.id,
                    GlobalType.CLASS_PROPERTY,
                ))
            else:
                self.class_members[param.id.string()] = (param.id, GlobalType.CLASS_PROPERTY)
        for prop in self.cwass.properties:
            if prop.id.string() in self.class_members:
                self.errors.append(DuplicateDefinitionError(
                    *self.class_members[prop.id.string()],
                    prop.id,
                    GlobalType.CLASS_PROPERTY,
                ))
            else:
                self.class_members[prop.id.string()] = (prop.id, GlobalType.CLASS_PROPERTY)
        for method in self.cwass.methods:
            if method.id.string() in self.class_members:
                self.errors.append(DuplicateDefinitionError(
                    *self.class_members[method.id.string()],
                    method.id,
                    GlobalType.CLASS_METHOD,
                ))
            else:
                self.class_members[method.id.string()] = (method.id, GlobalType.CLASS_METHOD)

    def analyze_method(self, fn: Function) -> None:
        local_defs: dict[str, tuple[Token, GlobalType]] = self.class_members.copy()
        for p in fn.params:
            self.analyze_param(p, local_defs)
        assert isinstance(fn.body, BlockStatement)
        self.analyze_body(fn.body, local_defs)

    def analyze_class(self, cwass: Class) -> None:
        local_defs: dict[str, tuple[Token, GlobalType]] = self.class_members.copy()
        for p in cwass.params:
            self.analyze_param(p, local_defs)
        for prop in cwass.properties:
            self.analyze_declaration(prop, local_defs)
        for method in cwass.methods:
            self.analyze_method(method)

    def analyze_param(self, param: Parameter, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        assert isinstance(param.id, Token)
        if param.id.string() in local_defs:
            self.errors.append(DuplicateDefinitionError(
                *local_defs[param.id.string()],
                param.id,
                GlobalType.LOCAL_CLASS_ID,
            ))
        else:
            local_defs[param.id.string()] = (param.id, GlobalType.CLASS_PROPERTY)

    def analyze_args(self, args: list[Value], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for arg in args:
            match arg:
                case Value():
                    self.analyze_value(arg, local_defs)
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
                case FnCall():
                    self.analyze_ident_prods(stmt, local_defs)
                case _:
                    raise ValueError(f"Unknown statement: {stmt}")

    ## IN BODY ANALYZERS
    def analyze_print(self, print_stmt: Print, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for val in print_stmt.values:
            match val:
                case Value():
                    self.analyze_value(val, local_defs)
                case Token():
                    self.expect_defined_token(val, local_defs)

    def analyze_input(self, input_stmt: Input, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match input_stmt.expr:
            case Value():
                self.analyze_value(input_stmt.expr, local_defs)
            case Token():
                self.expect_defined_token(input_stmt.expr, local_defs)

    def analyze_if(self, if_stmt: IfStatement | ElseIfStatement, local_defs: dict[str, tuple[Token, GlobalType]], else_if: bool = False) -> None:
        match if_stmt.condition:
            case Value():
                self.analyze_value(if_stmt.condition, local_defs)
            case Token():
                self.expect_defined_token(if_stmt.condition, local_defs)
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
            case Value():
                self.analyze_value(decl.value, local_defs)
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
            case Value():
                self.analyze_value(assign.value, local_defs)
            case Token():
                self.expect_defined_token(assign.value, local_defs)

    def analyze_while_loop(self, while_loop: WhileLoop, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match while_loop.condition:
            case Value():
                self.analyze_value(while_loop.condition, local_defs)
            case Token():
                self.expect_defined_token(while_loop.condition, local_defs)
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
        match for_loop.condition:
            case Value():
                self.analyze_value(for_loop.condition, local_defs)
            case Token():
                self.expect_defined_token(for_loop.condition, local_defs)
        match for_loop.update:
            case Value():
                self.analyze_value(for_loop.update, local_defs)
            case Token():
                self.expect_defined_token(for_loop.update, local_defs)
        self.analyze_body(for_loop.body, local_defs.copy())

    def analyze_return(self, ret: ReturnStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match ret.expr:
            case Token():
                self.expect_defined_token(ret.expr, local_defs)
            case Value():
                self.analyze_value(ret.expr, local_defs)
            case _:
                raise ValueError(f"Unknown return expression: {ret.expr}")

    ## OTHER ANALYZERS
    def analyze_value(self, value: Value, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match value:
            case Token():
                self.expect_defined_token(value, local_defs)
            case Expression():
                self.analyze_expression(value, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(value, local_defs)
            case Iterable():
                self.analyze_iterable(value, local_defs)
            case _:
                raise ValueError(f"Unknown value: {value}")
    def analyze_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Token, GlobalType]],
                            access_depth: int = 1) -> None:
        match ident_prod:
            case IndexedIdentifier():
                match ident_prod.id:
                    case Token():
                        self.expect_defined_token(ident_prod.id, local_defs)
                    case FnCall():
                        self.analyze_fn_call(ident_prod.id, local_defs)
                self.analyze_array_indices(ident_prod.index, local_defs)
            case FnCall():
                self.analyze_fn_call(ident_prod, local_defs)
            case ClassConstructor():
                self.analyze_args(ident_prod.args, local_defs)
            case ClassAccessor():
                if access_depth > 0:
                    match ident_prod.id:
                        case Token():
                            self.expect_defined_token(ident_prod.id, local_defs)
                        case FnCall():
                            self.analyze_fn_call(ident_prod.id, local_defs)
                match ident_prod.accessed:
                    case FnCall():
                        self.analyze_args(ident_prod.accessed.args, local_defs)
                    case IndexedIdentifier():
                        self.analyze_array_indices(ident_prod.accessed.index, local_defs)
                    case ClassAccessor():
                        self.analyze_ident_prods(ident_prod.accessed, local_defs, access_depth=access_depth+1)
            case _:
                raise ValueError(f"Unknown identifier production: {ident_prod}")

    def analyze_fn_call(self, fn_call: FnCall, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        if fn_call.id.string() in local_defs and local_defs[fn_call.id.string()][1] == GlobalType.FUNCTION:
            pass
        else:
            self.errors.append(UndefinedError(
                fn_call.id,
                GlobalType.FUNCTION,
            ))
        self.analyze_args(fn_call.args, local_defs)

    def analyze_iterable(self, collection: Iterable, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        this is for array literals, string fmt, and string literals
        try not to use analyze_array_literal, analyze_string_fmt, or analyze_string_literal directly.
        use this method instead.
        '''
        match collection:
            case ArrayLiteral():
                self.analyze_array_literal(collection, local_defs)
            case StringFmt():
                self.analyze_string_fmt(collection, local_defs)
            case Input():
                self.analyze_input(collection, local_defs)
            case StringLiteral():
                self.analyze_string_literal(collection, local_defs)
            case _:
                raise ValueError(f"Unknown collection: {collection}")

    def analyze_string_literal(self, str_lit: StringLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        try not to use this method directly.
        use analyze_iterable instead
        '''
        for concat in str_lit.concats:
            match concat:
                case StringFmt():
                    self.analyze_string_fmt(concat, local_defs)
                case Input():
                    self.analyze_input(concat, local_defs)
                case StringLiteral():
                    self.analyze_string_literal(concat, local_defs)

    def analyze_array_literal(self, array_literal: ArrayLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        try not to use this method directly.
        use analyze_iterable instead
        '''
        for elem in array_literal.elements:
            match elem:
                case Token():
                    self.expect_defined_token(elem, local_defs)
                case Value():
                    self.analyze_value(elem, local_defs)
                case _:
                    raise ValueError(f"Unknown array element: {elem}")
    
    def analyze_array_indices(self, index_list: list[Value], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for idx in index_list:
            match idx:
                case Value():
                    self.analyze_value(idx, local_defs)
                case Token():
                    self.expect_defined_token(idx, local_defs)
                case _:
                    raise ValueError(f"Unknown array index: {idx}")
    
    def analyze_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match expr:
            case PrefixExpression():
                match expr.right:
                    case Value():
                        self.analyze_value(expr.right, local_defs)
                    case Token():
                        self.expect_defined_token(expr.right, local_defs)
            case PostfixExpression():
                match expr.left:
                    case Value():
                        self.analyze_value(expr.left, local_defs)
                    case Token():
                        self.expect_defined_token(expr.left, local_defs)
            case InfixExpression():
                match expr.left:
                    case Value():
                        self.analyze_value(expr.left, local_defs)
                    case Token():
                        self.expect_defined_token(expr.left, local_defs)
                match expr.right:
                    case Value():
                        self.analyze_value(expr.right, local_defs)
                    case Token():
                        self.expect_defined_token(expr.right, local_defs)
            case _:
                raise ValueError(f"Unknown expression: {expr}")

    def analyze_string_fmt(self, string_fmt: StringFmt, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        try not to use this method directly.
        use analyze_iterable instead
        '''
        for expr in string_fmt.exprs:
            match expr:
                case Value():
                    self.analyze_value(expr, local_defs)
                case Token():
                    self.expect_defined_token(expr, local_defs)

        for concat in string_fmt.concats:
            match concat:
                case StringFmt() | Input() | StringLiteral():
                    self.analyze_iterable(concat, local_defs)
                case _:
                    raise ValueError(f"Unknown concat: {concat}")


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
                        GlobalType.IDENTIFIER,
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
                        GlobalType.IDENTIFIER,
                    ))
                else:
                    local_defs[token.string()] = (token, GlobalType.IDENTIFIER)
            case _:
                raise ValueError(f"Unknown token: {token}")
