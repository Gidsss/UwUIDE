from src.lexer.token import TokenType, UniqueTokenType
from src.analyzer.error_handler import DuplicateDefinitionError, FunctionAssignmentError, GlobalType, NonFunctionIdCall, UndefinedError
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
        assert self.program.mainuwu
        for global_dec in self.program.globals:
            self.analyze_declaration(global_dec, self.global_names)
        self.analyze_function(self.program.mainuwu, self.global_names.copy())
        for func in self.program.functions:
            self.analyze_function(func, self.global_names.copy())
        for cwass in self.program.classes:
            self.analyze_class(cwass)

    def compile_global_names(self) -> None:
        '''
        populates the self.global_names dict with the unique global names
        any duplicates will be appended to error
        '''
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

    def analyze_function(self, fn: Function, local_defs: dict[str, tuple[Token, GlobalType]],
                         *,
                         cwass=False) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        for p in fn.params:
            self.analyze_param(p, local_defs, cwass=cwass)
        assert isinstance(fn.body, BlockStatement)
        self.analyze_body(fn.body, local_defs.copy(), cwass=cwass)

    def analyze_class(self, cwass: Class) -> None:
        local_defs: dict[str, tuple[Token, GlobalType]] = self.global_names.copy()
        self.compile_class_methods(cwass, local_defs)
        for p in cwass.params:
            self.analyze_param(p, local_defs, cwass=True)
        for prop in cwass.properties:
            self.analyze_declaration(prop, local_defs, cwass=True)
        for method in cwass.methods:
            self.analyze_function(method, local_defs.copy(), cwass=True)

    def compile_class_methods(self, cwass: Class, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for method in cwass.methods:
            if f"{cwass.id.flat_string()}.{method.id.string()}" in local_defs:
                self.errors.append(DuplicateDefinitionError(
                    *local_defs[f"{cwass.id.flat_string()}.{method.id.string()}"],
                    method.id,
                    GlobalType.CLASS_METHOD,
                ))
            else:
                local_defs[f"{cwass.id.flat_string()}.{method.id.string()}"] = (method.id, GlobalType.CLASS_METHOD)

    def analyze_param(self, param: Declaration, local_defs: dict[str, tuple[Token, GlobalType]],
                      *,
                      cwass=False) -> None:
        if param.id.string() in local_defs:
            self.errors.append(DuplicateDefinitionError(
                *local_defs[param.id.string()],
                param.id,
                GlobalType.IDENTIFIER if not cwass else GlobalType.CLASS_PROPERTY,
            ))
        else:
            local_defs[param.id.string()] = (param.id, GlobalType.IDENTIFIER)

    def analyze_args(self, args: list[Value], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for arg in args:
            self.analyze_value(arg, local_defs)

    def analyze_body(self, body: BlockStatement, local_defs: dict[str, tuple[Token, GlobalType]],
                     *,
                     cwass=False) -> None:
        '''
        when you're calling analyze_body(), make sure to pass in a copy of local_defs
        '''
        for stmt in body.statements:
            match stmt:
                case Print():
                    self.analyze_print(stmt, local_defs)
                case Input():
                    self.analyze_input(stmt, local_defs)
                case Declaration():
                    self.analyze_declaration(stmt, local_defs, cwass=cwass, in_body=True)
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
                case IdentifierProds():
                    self.analyze_ident_prods(stmt, local_defs)
                case Break():
                    pass
                case Comment():
                    pass
                case _:
                    raise ValueError(f"Unknown statement: {stmt}")

    ## IN BODY ANALYZERS
    def analyze_print(self, print_stmt: Print, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for val in print_stmt.values:
            self.analyze_value(val, local_defs)

    def analyze_input(self, input_stmt: Input, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.analyze_value(input_stmt.expr, local_defs)

    def analyze_if(self, if_stmt: IfStatement | ElseIfStatement, local_defs: dict[str, tuple[Token, GlobalType]], else_if: bool = False) -> None:
        self.analyze_value(if_stmt.condition, local_defs)
        self.analyze_body(if_stmt.then, local_defs.copy())
        if else_if: return
        assert isinstance(if_stmt, IfStatement)
        for elif_stmt in if_stmt.else_if:
            self.analyze_if(elif_stmt, local_defs, else_if=True)
        if if_stmt.else_block:
            self.analyze_body(if_stmt.else_block, local_defs.copy())

    def analyze_declaration(self, decl: Declaration, local_defs: dict[str, tuple[Token, GlobalType]],
                            *,
                            cwass=False, in_body=False) -> None:
        self.expect_unique_token(decl.id,
                                 GlobalType.IDENTIFIER if not cwass else (
                                 GlobalType.CLASS_PROPERTY if not in_body else GlobalType.LOCAL_CLASS_ID),
                                 local_defs)
        match decl.dtype.token:
            case TokenType():
                pass
            case UniqueTokenType():
                self.expect_defined_token(decl.dtype.to_unit_type(), GlobalType.CLASS, local_defs)
            case _:
                raise ValueError(f"Unknown dtype: {decl.dtype}")
        self.analyze_value(decl.value, local_defs)

    def analyze_assignment(self, assign: Assignment, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match assign.id:
            case Token():
                self.expect_defined_token(assign.id, GlobalType.IDENTIFIER, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(assign.id, local_defs)
            case _:
                raise ValueError(f"Unknown assignment left hand side: {assign.id}")
        self.analyze_value(assign.value, local_defs)

    def analyze_while_loop(self, while_loop: WhileLoop, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.analyze_value(while_loop.condition, local_defs)
        self.analyze_body(while_loop.body, local_defs.copy())

    def analyze_for_loop(self, for_loop: ForLoop, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        when calling analyze_for_loop(), make sure to pass in a copy of local_defs
        '''
        match for_loop.init:
            case Assignment():
                self.analyze_assignment(for_loop.init, local_defs)
            case Declaration():
                self.analyze_declaration(for_loop.init, local_defs)
            case Token():
                self.expect_defined_token(for_loop.init, GlobalType.IDENTIFIER, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(for_loop.init, local_defs)
            case _:
                raise ValueError(f"Unknown for loop init: {for_loop.init}")
        self.analyze_value(for_loop.condition, local_defs)
        self.analyze_value(for_loop.update, local_defs)
        self.analyze_body(for_loop.body, local_defs.copy())

    def analyze_return(self, ret: ReturnStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.analyze_value(ret.expr, local_defs)

    ## OTHER ANALYZERS
    def analyze_value(self, value: Value | Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match value:
            case Token():
                self.expect_defined_token(value, GlobalType.IDENTIFIER, local_defs)
            case Expression():
                self.analyze_expression(value, local_defs)
            case IdentifierProds():
                self.analyze_ident_prods(value, local_defs)
            case Iterable():
                self.analyze_iterable(value, local_defs)
            case _:
                if value.string() != None: raise ValueError(f"Unknown value: {value.string()}")
    def analyze_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Token, GlobalType]],
                            access_depth: int = 0) -> None:
        match ident_prod:
            case IndexedIdentifier():
                match ident_prod.id:
                    case Token():
                        self.expect_defined_token(ident_prod.id, GlobalType.IDENTIFIER, local_defs)
                    case FnCall():
                        self.analyze_fn_call(ident_prod.id, local_defs)
                self.analyze_array_indices(ident_prod.index, local_defs)
            case FnCall():
                self.analyze_fn_call(ident_prod, local_defs)
            case ClassConstructor():
                self.analyze_class_constructor(ident_prod, local_defs)
            case ClassAccessor():
                if access_depth == 0:
                    match ident_prod.id:
                        case Token():
                            self.expect_defined_token(ident_prod.id, GlobalType.IDENTIFIER, local_defs)
                        case FnCall():
                            self.analyze_fn_call(ident_prod.id, local_defs)
                match ident_prod.accessed:
                    case FnCall():
                        for arg in ident_prod.accessed.args:
                            self.analyze_value(arg, local_defs)
                    case IndexedIdentifier():
                        self.analyze_array_indices(ident_prod.accessed.index, local_defs)
                    case ClassAccessor():
                        self.analyze_ident_prods(ident_prod.accessed, local_defs, access_depth=access_depth+1)
            case _:
                raise ValueError(f"Unknown identifier production: {ident_prod}")

    def analyze_fn_call(self, fn_call: FnCall, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        if fn_call.id.string() in local_defs:
            if not local_defs[fn_call.id.string()][1] == GlobalType.FUNCTION:
                self.errors.append(NonFunctionIdCall(
                    local_defs[fn_call.id.string()][0],
                    fn_call.id,
                ))
        else:
            self.errors.append(UndefinedError(
                fn_call.id,
                GlobalType.FUNCTION,
            ))
        self.analyze_args(fn_call.args, local_defs)

    def analyze_class_constructor(self, class_constructor: ClassConstructor, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        if class_constructor.id.flat_string() in local_defs and local_defs[class_constructor.id.flat_string()][1] == GlobalType.CLASS:
            pass
        else:
            self.errors.append(UndefinedError(
                class_constructor.id,
                GlobalType.CLASS,
            ))
        self.analyze_args(class_constructor.args, local_defs)

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
            self.analyze_value(elem, local_defs)
    
    def analyze_array_indices(self, index_list: list[Value], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for idx in index_list:
            self.analyze_value(idx, local_defs)
    
    def analyze_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match expr:
            case PrefixExpression():
                self.analyze_value(expr.right, local_defs)
            case PostfixExpression():
                self.analyze_value(expr.left, local_defs)
            case InfixExpression():
                self.analyze_value(expr.left, local_defs)
                self.analyze_value(expr.right, local_defs)
            case _:
                raise ValueError(f"Unknown expression: {expr}")

    def analyze_string_fmt(self, string_fmt: StringFmt, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        try not to use this method directly.
        use analyze_iterable instead
        '''
        for expr in string_fmt.exprs:
            self.analyze_value(expr, local_defs)

        for concat in string_fmt.concats:
            match concat:
                case StringFmt() | Input() | StringLiteral():
                    self.analyze_iterable(concat, local_defs)
                case _:
                    raise ValueError(f"Unknown concat: {concat}")


    ## HELPER METHODS
    def expect_defined_token(self, token: Token, global_type: GlobalType, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        '''
        checks whether the token is defined in the scope
        if not, appends to errors
        '''
        match token.token:
            case TokenType.STRING_LITERAL | TokenType.INT_LITERAL | TokenType.FLOAT_LITERAL | TokenType.FAX | TokenType.CAP | TokenType.NUWW:
                pass
            case UniqueTokenType():
                if token.string() in local_defs:
                    if not local_defs[token.string()][1] in (
                        GlobalType.IDENTIFIER, GlobalType.CLASS_PROPERTY, GlobalType.LOCAL_CLASS_ID, GlobalType.CLASS):
                        self.errors.append(FunctionAssignmentError(
                            local_defs[token.string()][0],
                            token,
                        ))
                else:
                    self.errors.append(UndefinedError(
                        token,
                        global_type,
                    ))
            case _:
                raise ValueError(f"Unknown token: {token}")
    def expect_unique_token(self, token: Token, global_type: GlobalType, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
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
                        global_type,
                    ))
                else:
                    local_defs[token.string()] = (token, global_type)
            case _:
                raise ValueError(f"Unknown token: {token}")
