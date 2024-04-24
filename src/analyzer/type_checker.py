from copy import deepcopy
from .error_handler import GlobalType
from src.analyzer.error_handler import *
from src.lexer.token import Token, UniqueTokenType
from src.parser.productions import *

class TypeChecker:
    def __init__(self, program: Program):
        self.program = program
        self.errors = []

        # maps global names to their Declaration (if any), the type's token, and GlobalType for error messages
        self.global_defs: dict[str, tuple[Declaration, Token, GlobalType]] = {}
        self.class_signatures: dict[str, tuple[Declaration, Token, GlobalType]] = {}
        self.class_method_param_types: dict[str, list[Token]] = {}
        self.function_param_types: dict[str, list[Token]] = {}
        self.class_param_types: dict[str, list[Token]] = {}
        self.return_list: list[TokenType] = []
        self.compile_global_types()
        self.check_program()

    def compile_global_types(self):
        '''
        populates the self.global_types dict with the unique global names
        any duplicates will be appended to error
        '''
        for global_dec in self.program.globals:
            self.global_defs[global_dec.id.flat_string()] = global_dec, global_dec.dtype, GlobalType.IDENTIFIER
        for func in self.program.functions:
            self.global_defs[func.id.flat_string()] = Declaration(), func.rtype, GlobalType.FUNCTION
            self.function_param_types[func.id.flat_string()] = [param.dtype for param in func.params]
        for cwass in self.program.classes:
            self.global_defs[cwass.id.flat_string()] = (Declaration(), cwass.id, GlobalType.CLASS)
            self.class_param_types[cwass.id.flat_string()] = [param.dtype for param in cwass.params]
            for param in cwass.params:
                self.class_signatures[f"{cwass.id.flat_string()}.{param.id.flat_string()}"] = (param, param.dtype, GlobalType.CLASS_PROPERTY)
            for prop in cwass.properties:
                self.class_signatures[f"{cwass.id.flat_string()}.{prop.id.flat_string()}"] = (prop, prop.dtype, GlobalType.CLASS_PROPERTY)
            for method in cwass.methods:
                self.class_signatures[f"{cwass.id.flat_string()}.{method.id.flat_string()}"] = (Declaration(), method.rtype, GlobalType.CLASS_METHOD)
                self.class_method_param_types[f"{cwass.id.flat_string()}.{method.id.flat_string()}"] = [param.dtype for param in method.params]
        self.compile_std_types()

    def compile_std_types(self):
        self.builtin_signatures: set[str] = {
            'senpai.len',
            'senpai.reversed',
            'senpai.has',
            'senpai.upper',
            'senpai.lower',

            'array_type.len',
            'array_type.reverse',
            'array_type.append',
            'array_type.has',
        }
        self.class_signatures.update(
            {
                'senpai.len': (Declaration(), Token('chan', TokenType.CHAN), GlobalType.CLASS_METHOD),
                'senpai.reversed': (Declaration(), Token('senpai', TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.has': (Declaration(), Token('sama', TokenType.SAMA), GlobalType.CLASS_METHOD),
                'senpai.upper': (Declaration(), Token('senpai', TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.lower': (Declaration(), Token('senpai', TokenType.SENPAI), GlobalType.CLASS_METHOD),

                'array_type.len': (Declaration(), Token('chan', TokenType.CHAN), GlobalType.CLASS_METHOD),
                'array_type.reverse': (Declaration(), Token('san', TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.has': (Declaration(), Token('sama', TokenType.SAMA), GlobalType.CLASS_METHOD),
                'array_type.append': (Declaration(), Token('san', TokenType.SAN), GlobalType.CLASS_METHOD),
            },
        )
        self.class_method_param_types.update(
            {
                'senpai.len': [],
                'senpai.reversed': [],
                'senpai.has': [Token('senpai', TokenType.SENPAI)],
                'senpai.upper': [],
                'senpai.lower': [],

                'array_type.len': [],
                'array_type.reverse': [],
                'array_type.append': [Token('elem', TokenType.ARRAY_ELEMENT)],
                'array_type.has': [Token('elem', TokenType.ARRAY_ELEMENT)],
            }
        )

    def check_program(self) -> None:
        assert self.program.mainuwu
        self.check_function(self.program.mainuwu, self.global_defs.copy())
        for func in self.program.functions: self.check_function(func, self.global_defs)
        for cwass in self.program.classes: self.check_class(cwass, self.global_defs.copy())

    def check_function(self, func: Function, local_defs: dict[str, tuple[Declaration, Token, GlobalType]], cwass: str|None = None) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        self.compile_params(func.params, local_defs)
        self.check_body(func.body, func.rtype, local_defs.copy())
        if len(self.return_list) == 0 and func.rtype.flat_string() != 'san':
            self.errors.append(NoReturnStatement(func, cwass=cwass))
        self.return_list.clear()

    def check_class(self, cwass: Class, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        self.compile_params(cwass.params, local_defs)
        for prop in cwass.properties:
            self.check_declaration(prop, local_defs)
        for method in cwass.methods:
            self.check_function(method, local_defs, cwass=cwass.id.flat_string())

    def compile_params(self, params: list[Declaration], local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        for param in params:
            local_defs[param.id.flat_string()] = (param, param.dtype, GlobalType.IDENTIFIER)

    def check_body(self, body: BlockStatement, return_type: Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        for statement in body.statements:
            match statement:
                case Print():
                    self.check_print(statement, local_defs)
                case Input():
                    self.check_input(statement, local_defs)
                case Declaration():
                    self.check_declaration(statement, local_defs)
                case Assignment():
                    self.check_assignment(statement, local_defs)
                case IfStatement():
                    self.check_if(statement, return_type, local_defs)
                case WhileLoop():
                    self.check_while_loop(statement, return_type, local_defs)
                case ForLoop():
                    self.check_for_loop(statement, return_type, local_defs.copy())
                case ReturnStatement():
                    self.check_return(statement, return_type, local_defs)
                case FnCall():
                    self.evaluate_fn_call(statement, local_defs)
                case ClassAccessor():
                    self.check_and_evaluate_class_accessor(statement, local_defs)
                case _:
                    raise ValueError(f"Unknown statement: {statement}")

    def check_print(self, print: Print, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        for val in print.values:
            self.evaluate_value(val, local_defs)

    def check_input(self, input: Input, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        self.evaluate_value(input.expr, local_defs)

    def check_if(self, if_stmt: IfStatement | ElseIfStatement, return_type: Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]], else_if=False) -> None:
        self.evaluate_value(if_stmt.condition, local_defs)
        self.check_body(if_stmt.then, return_type, local_defs.copy())
        if else_if: return
        assert isinstance(if_stmt, IfStatement)
        for elif_stmt in if_stmt.else_if:
            self.check_if(elif_stmt, return_type, local_defs, else_if=True)
        if if_stmt.else_block:
            self.check_body(if_stmt.else_block, return_type, local_defs.copy())

    def check_while_loop(self, while_loop: WhileLoop, return_type: Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        self.evaluate_value(while_loop.condition, local_defs)
        self.check_body(while_loop.body, return_type, local_defs.copy())

    def check_for_loop(self, for_loop: ForLoop, return_type: Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        'pass in a copy of local defs when calling this'
        match for_loop.init:
            case Declaration():
                self.check_declaration(for_loop.init, local_defs)
                decl, dono_token, global_type = local_defs[for_loop.init.id.flat_string()]
            case Assignment():
                self.check_assignment(for_loop.init, local_defs)
                decl, dono_token, global_type = local_defs[self.extract_id(for_loop.init.id).flat_string()]
            case Token():
                self.evaluate_token(for_loop.init, local_defs)
                match for_loop.init.token:
                    case Token():
                        decl, dono_token, global_type = Declaration(), Token(), GlobalType.IDENTIFIER
                    case UniqueTokenType():
                        decl, dono_token, global_type = local_defs[for_loop.init.flat_string()]
                    case _:
                        raise ValueError(f"Unknown token: {for_loop.init}")
            case IdentifierProds():
                self.evaluate_ident_prods(for_loop.init, local_defs)
                _, _, decl, dono_token, global_type = self.extract_last_id(for_loop.init, local_defs)

        if decl.dono_token.exists():
            token = self.extract_id(for_loop.init.id)
            self.errors.append(
                ReassignedConstantError(
                    token = token,
                    defined_token = dono_token,
                    header = f"Constant in for loop initializer: {token.flat_string()}",
                    token_msg = "Tried to use constant in a for loop initializer",
                )
            )

        self.evaluate_value(for_loop.condition, local_defs)
        self.evaluate_value(for_loop.update, local_defs)
        self.check_body(for_loop.body, return_type, local_defs.copy())

    def check_return(self, ret: ReturnStatement, return_type: Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        actual_type = self.evaluate_value(ret.expr, local_defs)
        if actual_type == TokenType.SAN and return_type.token != TokenType.SAN:
            self.errors.append(
                ReturnTypeMismatchError(
                    expected=return_type,
                    return_stmt = ret,
                    actual_type=actual_type,
                )
            )
            return
        elif not self.is_similar_type(actual_type.flat_string(), return_type.flat_string(), ret.expr):
            self.errors.append(
                ReturnTypeMismatchError(
                    expected=return_type,
                    return_stmt = ret,
                    actual_type=actual_type,
                )
            )
        self.return_list.append(actual_type)

    def check_declaration(self, decl: Declaration, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        self.check_value(decl.value, decl.dtype, local_defs, decl=decl)

    def check_assignment(self, assign: Assignment, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        signature, token, decl, dono_token, global_type = self.extract_last_id(assign.id, local_defs)
        try:
            original_def = local_defs[signature][0]
        except KeyError:
            original_def = self.class_signatures[signature][0]
            if signature in self.builtin_signatures:
                original_def = None
        if decl.dono_token.exists():
            signature = self.extract_id(assign.id)
            self.errors.append(
                ReassignedConstantError(
                    token = signature,
                    defined_token = dono_token,
                    header = f"Reassigning constant: {signature.flat_string()}",
                    token_msg = "Tried to reassign here",
                )
            )
            return
        elif global_type in [GlobalType.FUNCTION, GlobalType.CLASS_METHOD]:
            self.errors.append(
                FunctionAssignmentError(
                    original=original_def.id if original_def else None,
                    assignment=token,
                    class_signature=signature,
                )
            )
        self.check_value(assign.value, decl.dtype, local_defs, assignment=True, decl=decl, assign=assign)

    def check_value(self, value: Value, expected_type: Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]],
                    assignment: bool = False, decl: Declaration = Declaration(), assign: Assignment = Assignment()) -> None:
        'if `assignment` is true, its an assignment. if false, its a declaration'
        self.expr_err_count = 0

        match expected_type.token:
            case TokenType():
                actual_type = self.evaluate_value(value, local_defs)
                match value:
                    case Input():
                        if not value.concats: actual_type_str = "inpwt"
                        else: actual_type_str = "senpai"
                    case _: actual_type_str = actual_type.flat_string()
                if not self.is_similar_type(actual_type_str, expected_type.flat_string(), value):
                    self.errors.append(
                        TypeMismatchError(
                            title="Assignment" if assignment else "Declaration",
                            expected=expected_type,
                            actual_val=value,
                            actual_type=actual_type,
                            context=assign if assignment else decl,
                        )
                    )
            case UniqueTokenType():
                match value:
                    case ClassConstructor():
                        actual_type = UniqueTokenType() # placeholder, will not be used in this case
                        self.check_class_constructor(value, local_defs)
                    case _:
                        actual_type = self.evaluate_value(value, local_defs)
                        if not self.is_similar_type(actual_type.flat_string(), expected_type.flat_string(), value):
                            self.errors.append(
                                TypeMismatchError(
                                    title="Assignment" if assignment else "Declaration",
                                    expected=expected_type,
                                    actual_val=value,
                                    actual_type=actual_type,
                                    context=assign if assignment else decl,
                                )
                            )
        # (DECLARATION & ASSIGNMENT) uninitialize identifiers if any errors occured in evaluating value
        if self.expr_err_count > 0 and expected_type != TokenType.SAN:
            decl_new = deepcopy(decl)
            decl_new.initialized = False
            decl_new.value = Value()
            local_defs[decl_new.id.flat_string()] = (decl_new, decl_new.dtype, GlobalType.IDENTIFIER)

        # (ASSIGNMENT) initialize uninitialized identifiers
        elif not decl.initialized and actual_type != TokenType.SAN:
            decl_new = deepcopy(decl)
            decl_new.initialized = True
            local_defs[decl_new.id.flat_string()] = (decl_new, decl_new.dtype, GlobalType.IDENTIFIER)

        # (DECLARATION & ASSIGNMENT) initialize identifiers with assigned values
        else:
            local_defs[decl.id.flat_string()] = (decl, decl.dtype, GlobalType.IDENTIFIER)

        if assignment:
            assign.dtype = actual_type
        self.expr_err_count = 0

    def evaluate_value(self, value: Value | Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        match value:
            case Token():
                return self.evaluate_token(value, local_defs)
            case Expression():
                return self.evaluate_expression(value, local_defs)
            case IdentifierProds():
                return self.evaluate_ident_prods(value, local_defs)
            case Iterable():
                return self.evaluate_iterable(value, local_defs)
            case _:
                if value.flat_string() != None: raise ValueError(f"Unknown value: {value.flat_string()}")
                return TokenType.SAN

    def evaluate_expression(self, expr: Expression, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        match expr:
            case PrefixExpression():
                right = self.evaluate_value(expr.right, local_defs)
                if right not in self.math_operands():
                    definition = None
                    if isinstance(expr.right, Token) and isinstance(expr.right.token, UniqueTokenType):
                        definition = local_defs[expr.right.flat_string()][0]
                    self.errors.append(
                        PrePostFixOperandError(
                            header=f"Non-Math Prefix Operand: '{expr.right.flat_string()}'",
                            op=expr.op,
                            val=expr.right,
                            val_definition=definition.dtype if definition else None,
                            val_type=right,
                        )
                    )
                    self.expr_err_count += 1
                return right
            case InfixExpression():
                left = self.evaluate_value(expr.left, local_defs)
                right = self.evaluate_value(expr.right, local_defs)

                if expr.op.token in self.math_operators():
                    if not (left in self.math_operands() and right in self.math_operands()):
                        left_definition, right_definition = None, None
                        if isinstance(expr.left, Token) and isinstance(expr.left.token, UniqueTokenType):
                            left_definition = local_defs[expr.left.flat_string()][0]
                        if isinstance(expr.right, Token) and isinstance(expr.right.token, UniqueTokenType):
                            right_definition = local_defs[expr.right.flat_string()][0]
                        self.errors.append(
                            InfixOperandError(
                                header="Non-Math Infix Operand",
                                op=expr.op,
                                left=(expr.left, left_definition.dtype if left_definition else None),
                                right=(expr.right, right_definition.dtype if right_definition else None),
                                left_type=left if left not in self.math_operands() else None,
                                right_type=right if right not in self.math_operands() else None,
                            )
                        )
                        self.expr_err_count += 1
                    if left == TokenType.KUN or right == TokenType.KUN:
                        return TokenType.KUN
                    else:
                        return TokenType.CHAN
                elif expr.op.token in self.comparison_operators():
                    if not (left in self.math_operands() and right in self.math_operands()):
                        left_definition, right_definition = None, None
                        if isinstance(expr.left, Token) and isinstance(expr.left.token, UniqueTokenType):
                            left_definition = local_defs[expr.left.flat_string()][0]
                        if isinstance(expr.right, Token) and isinstance(expr.right.token, UniqueTokenType):
                            right_definition = local_defs[expr.right.flat_string()][0]
                        self.errors.append(
                            InfixOperandError(
                                header="Non-Comparison Infix Operand: ",
                                op=expr.op,
                                left=(expr.left, left_definition.dtype if left_definition else None),
                                right=(expr.right, right_definition.dtype if right_definition else None),
                                left_type=left if left not in self.math_operands() else None,
                                right_type=right if right not in self.math_operands() else None,
                            )
                        )
                        self.expr_err_count += 1
                    return TokenType.SAMA
                elif expr.op.token in self.equality_operators():
                    return TokenType.SAMA
                else:
                    raise ValueError(f"Unknown operator: {expr.op}")
            case PostfixExpression():
                left = self.evaluate_value(expr.left, local_defs)
                if left not in self.math_operands():
                        definition = None
                        if isinstance(expr.left, Token) and isinstance(expr.left.token, UniqueTokenType):
                            definition = local_defs[expr.left.flat_string()][0]
                        self.errors.append(
                            PrePostFixOperandError(
                                header=f"Non-Math Postfix Operand: '{expr.left.flat_string()}'",
                                op=expr.op,
                                val=expr.left,
                                val_definition=definition.dtype if definition else None,
                                val_type=left,
                                postfix=True,
                            )
                        )
                        self.expr_err_count += 1
                return left
            case _:
                raise ValueError(f"Unknown expression: {expr}")

    def evaluate_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        match ident_prod:
            case IndexedIdentifier():
                for idx in ident_prod.index:
                    self.evaluate_value(idx, local_defs)
                match ident_prod.id:
                    case Token():
                        arr_type = self.evaluate_token(ident_prod.id, local_defs)
                    case FnCall():
                        arr_type = self.evaluate_fn_call(ident_prod.id, local_defs)
                    case _:
                        raise ValueError(f"Unknown identifier production for indexed identifier: {ident_prod}")
                if not self.is_accessible(arr_type):
                    token = self.extract_id(ident_prod.id)
                    type_definition = local_defs[token.flat_string()][0]
                    self.errors.append(
                        NonIterableIndexingError(
                            token=token,
                            type_definition=type_definition.dtype,
                            token_type=arr_type,
                            usage=ident_prod.flat_string(),
                        )
                    )
                    return TokenType.SAN
                return arr_type.to_unit_type()
            case FnCall():
                return self.evaluate_fn_call(ident_prod, local_defs)
            case ClassConstructor():
                self.check_class_constructor(ident_prod, local_defs)
                return ident_prod.id.token
            case ClassAccessor():
                return self.check_and_evaluate_class_accessor(ident_prod, local_defs)
            case _:
                raise ValueError(f"Unknown identifier production: {ident_prod}")

    def check_and_evaluate_class_accessor(self, accessor: ClassAccessor, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        # check that the accessor is of type class
        id = self.extract_id(accessor).flat_string()
        match accessor.id:
            case Token() | FnCall() | ClassAccessor():
                class_type = local_defs[id][0].dtype
                if not class_type.is_unique_type() and not self.is_accessible(class_type.token):
                    self.errors.append(
                        NonClassAccessError(
                            id=self.extract_id(accessor),
                            id_definition=class_type,
                            usage=accessor.flat_string(),
                        )
                    )
            case IndexedIdentifier():
                class_type = local_defs[id][0].dtype
                if not self.is_accessible(class_type.token):
                    token = self.extract_id(accessor.id)
                    type_definition = local_defs[token.flat_string()][0]
                    self.errors.append(
                        NonIterableIndexingError(
                            token=token,
                            type_definition=type_definition.dtype,
                            token_type=class_type.token,
                            usage=accessor.id.flat_string(),
                        )
                    )
                if not class_type.is_unique_type():
                    self.errors.append(
                        NonClassAccessError(
                            id=self.extract_id(accessor),
                            id_definition=class_type,
                            usage=accessor.flat_string(),
                        )
                    )
                class_type = class_type.to_unit_type()
            case _: raise ValueError(f"Unknown class accessor: {accessor}")

        match accessor.accessed:
            case Token():
                accessed = accessor.accessed
                member_signature = f"{class_type.flat_string()}.{accessed.flat_string()}"
                if not (res := self.class_signatures.get(member_signature)):
                    self.errors.append(
                        UndefinedClassMember(
                            class_type.flat_string(),
                            accessed,
                            GlobalType.CLASS_PROPERTY,
                        )
                    )
                    return TokenType.SAN
                return_type, _, member_type = res
                if member_type != GlobalType.CLASS_PROPERTY:
                    self.errors.append(
                        UndefinedClassMember(
                            class_type.flat_string(),
                            accessed,
                            GlobalType.CLASS_PROPERTY,
                            actual_definition=(return_type.id, member_type),
                        )
                    )
                    return TokenType.SAN
                return return_type.id.token
            case FnCall():
                accessed = accessor.accessed.id
                return self.evaluate_method_call(class_type, accessor.accessed, local_defs)
            case IndexedIdentifier():
                accessed = accessor.accessed.id
                match accessed:
                    case Token():
                        member_signature = f"{class_type.flat_string()}.{accessed.flat_string()}"
                        if not (res := self.class_signatures.get(member_signature)):
                            self.errors.append(
                                UndefinedClassMember(
                                    class_type.flat_string(),
                                    accessed,
                                    GlobalType.CLASS_PROPERTY,
                                )
                            )
                            return TokenType.SAN
                        return_type, _, member_type = res
                        if member_type != GlobalType.CLASS_PROPERTY:
                            self.errors.append(
                                UndefinedClassMember(
                                    class_type.flat_string(),
                                    accessed,
                                    GlobalType.CLASS_PROPERTY,
                                    actual_definition=(return_type.id, member_type),
                                )
                            )
                            return TokenType.SAN
                        if not self.is_accessible(return_type.id.token):
                            token = self.extract_id(accessed)
                            type_definition = self.class_signatures[member_signature][0]
                            self.errors.append(
                                NonIterableIndexingError(
                                    token=token,
                                    type_definition=type_definition.id,
                                    token_type=return_type.id.token,
                                    usage=accessed.flat_string(),
                                )
                            )
                            return TokenType.SAN
                        return return_type.id.token
                    case FnCall():
                        return self.evaluate_method_call(class_type, accessed, local_defs)
                    case _:
                        raise ValueError(f"Unknown class accessor: {accessor}")
            case ClassAccessor():
                return self.check_and_evaluate_class_accessor(accessor.accessed, local_defs)
            case _:
                raise ValueError(f"Unknown class accessor: {accessor}")

    def evaluate_iterable(self, collection: Iterable, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        match collection:
            case ArrayLiteral():
                flat_arr, units_type = self.expect_homogenous(collection, local_defs)
                for val in flat_arr:
                    self.evaluate_value(val, local_defs)
                ret = deepcopy(units_type).to_arr_type()
                return ret
            case StringFmt():
                for val in collection.exprs:
                    self.evaluate_value(val, local_defs)
                for concat in collection.concats:
                    self.evaluate_iterable(concat, local_defs)
                return TokenType.SENPAI
            case Input():
                self.evaluate_value(collection.expr, local_defs)
                for concat in collection.concats:
                    self.evaluate_iterable(concat, local_defs)
                return TokenType.SENPAI
            case StringLiteral():
                for concat in collection.concats:
                    self.evaluate_iterable(concat, local_defs)
                return TokenType.SENPAI
            case _:
                raise ValueError(f"Unknown collection: {collection}")

    def evaluate_method_call(self, class_type: Token, fn_call: FnCall, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        class_id_str = class_type.flat_string() if not class_type.token.is_arr_type() else 'array_type'
        if (res := self.class_signatures.get(f"{class_id_str}.{fn_call.id.flat_string()}")) is None:
            self.errors.append(
                UndefinedClassMember(
                    class_type.flat_string(),
                    fn_call.id,
                    GlobalType.CLASS_METHOD,
                )
            )
            return TokenType.SAN
        _, return_type, member_type = res
        if member_type != GlobalType.CLASS_METHOD:
            self.errors.append(
                UndefinedClassMember(
                    class_type.flat_string(),
                    fn_call.id,
                    GlobalType.CLASS_METHOD,
                    actual_definition=(return_type, member_type),
                )
            )
            return TokenType.SAN

        method_signature = f"{class_id_str}.{fn_call.id.flat_string()}"
        expected_types = self.class_method_param_types[method_signature]
        all_defs = self.class_signatures.copy()
        all_defs.update(local_defs)
        self.check_call_args(GlobalType.CLASS_METHOD, method_signature, fn_call.id,
                             fn_call.args, expected_types, all_defs, class_type.token)
        return return_type.token

    def check_call_args(self, global_type: GlobalType, call_str: str, id: Token, call_args: list[Value], expected_types: list[Token],
                        local_defs: dict[str, tuple[Declaration, Token, GlobalType]], self_type: TokenType = TokenType.EOF) -> None:
        actual_types: list[TokenType] = []
        matches: list[bool] = []
        for arg, expected in zip(call_args, expected_types):
            match arg:
                case Token():
                    match arg.token:
                        case UniqueTokenType():
                            actual_def = local_defs[arg.flat_string()][0]
                            actual = actual_def.dtype.token
                            if not actual_def.initialized: actual = TokenType.SAN
                        case TokenType():
                            actual = self.evaluate_token(arg, local_defs)
                case _:
                    actual = self.evaluate_value(arg, local_defs)
            actual_types.append(actual)
            if expected.token == TokenType.ARRAY_ELEMENT:
                matches.append(self.is_element_of_expected(actual, self_type if self_type.exists() else expected.token, arg))
            else:
                matches.append(self.is_similar_type(actual.flat_string(), expected.flat_string(), arg, is_call=True))

        if not all(matches) or len(call_args) != len(expected_types):
            expected_types_str: list[str] = [f"{e.token}" if e.token != TokenType.ARRAY_ELEMENT else f"{self_type.to_unit_type()} or {self_type.to_arr_type()}" for e in expected_types ]
            self.errors.append(
                MismatchedCallArgType(
                    global_type=global_type,
                    call_str=call_str if not self_type.exists() else call_str.replace("array_type", self_type.flat_string()),
                    id=id,
                    id_definition=local_defs[call_str][1] if call_str not in self.builtin_signatures else None,
                    expected_types=expected_types_str,
                    args=call_args,
                    actual_types=actual_types,
                    matches=matches
                )
            )

    def evaluate_fn_call(self, fn_call: FnCall, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        expected_types = self.function_param_types[fn_call.id.flat_string()]
        self.check_call_args(GlobalType.FUNCTION, fn_call.id.flat_string(), fn_call.id, fn_call.args, expected_types, local_defs)
        return local_defs[fn_call.id.flat_string()][1].token

    def check_class_constructor(self, class_constructor: ClassConstructor, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> None:
        expected_types = self.class_param_types[class_constructor.id.flat_string()]
        self.check_call_args(GlobalType.CLASS, class_constructor.id.flat_string(), class_constructor.id, class_constructor.args, expected_types, local_defs)

    def evaluate_token(self, token: Token, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> TokenType:
        match token.token:
            case TokenType.STRING_LITERAL: return TokenType.SENPAI
            case TokenType.INT_LITERAL: return TokenType.CHAN
            case TokenType.FLOAT_LITERAL: return TokenType.KUN
            case TokenType.FAX | TokenType.CAP: return TokenType.SAMA
            case TokenType.NUWW: return TokenType.SAN
            case UniqueTokenType():
                decl = local_defs[token.flat_string()][0]
                if not decl.initialized:
                    return TokenType.SAN
                return decl.dtype.token
            case _: raise ValueError(f"Unknown token: {token}")

    ## HELPER METHODS FOR OPERATORS AND OPERANDS
    def math_operands(self) -> list[TokenType]:
        return [TokenType.CHAN, TokenType.KUN, TokenType.SAMA]
    def math_operators(self) -> list[TokenType]:
        return [TokenType.ADDITION_SIGN, TokenType.DASH, TokenType.MULTIPLICATION_SIGN,
                TokenType.DIVISION_SIGN, TokenType.MODULO_SIGN]
    def comparison_operators(self) -> list[TokenType]:
        return [TokenType.LESS_THAN_SIGN, TokenType.GREATER_THAN_SIGN,
                TokenType.LESS_THAN_OR_EQUAL_SIGN, TokenType.GREATER_THAN_OR_EQUAL_SIGN]
    def equality_operators(self) -> list[TokenType]:
        return [TokenType.EQUALITY_OPERATOR, TokenType.INEQUALITY_OPERATOR,
                TokenType.AND_OPERATOR, TokenType.OR_OPERATOR]
    
    ## HELPER METHODS FOR EVALUATING ARRAYS
    def expect_homogenous(self, arr: ArrayLiteral, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]) -> tuple[list[Value], TokenType]:
        flat_arr = self.flatten_array(arr.elements)
        types: list[TokenType] = []
        for val in flat_arr:
            match val:
                case Token():
                    types.append(self.evaluate_token(val, local_defs))
                case Expression():
                    types.append(self.evaluate_expression(val, local_defs))
                case IdentifierProds():
                    types.append(self.evaluate_ident_prods(val, local_defs))
                case Iterable():
                    types.append(self.evaluate_iterable(val, local_defs))
                case _:
                    raise ValueError(f"Unknown array value type: {val.flat_string()}")
        type_list = [t.flat_string() for t in types]
        if len(set(type_list)) > 1:
            self.errors.append(
                HeterogeneousArrayError(arr, flat_arr, type_list)
            )
            return [], TokenType.SAN
        return flat_arr, types.pop() if types else TokenType.SAN_ARR

    def flatten_array(self, arr: list[Value]) -> list[Value]:
        res = []
        for item in arr:
            if isinstance(item, list):
                res += self.flatten_array(item)
            elif isinstance(item, ArrayLiteral):
                res += self.flatten_array(item.elements)
            else:
                res.append(item)
        return res

    def is_similar_type(self, actual_type: str, expected_type: str, val: Value, is_call: bool = False) -> bool:
        'determines if two types are similar'
        # nuww is an ok val for any type if and only if its not for a call
        condition_2 = (actual_type == 'san') if not is_call else False
        if (actual_type == expected_type 
            or condition_2): return True

        assert actual_type != expected_type
        match expected_type:
            # num types are convertible between each other
            case "chan" | "kun":
                match actual_type:
                    # inpwts with no concats can be converted to num types
                    case "chan" | "kun" | "sama" | "inpwt": return True
                    case _: return False
            # inpwt is inherently senpai
            case "senpai":
                match actual_type:
                    case "senpai" | "inpwt": return True
                    case _: return False
            # all types are convertible to bool
            case "sama": return True
            case _:
                # all array types can accept san[]
                if expected_type[-2:] == '[]':
                    if actual_type == "san[]":
                        if isinstance(val, ArrayLiteral):
                            if len(val.elements) == 0: return True
                            else: return False
                        else: return False

                # every other type needs exact match
                return False

    def is_element_of_expected(self, actual_type: TokenType, expected_type: TokenType, val: Value) -> bool:
        'determines if a type is self'
        actual, actual_arr, actual_unit = actual_type.flat_string(), actual_type.to_arr_type().flat_string(), actual_type.to_unit_type().flat_string()
        expected = expected_type.flat_string()
        if (actual == expected
            or actual_arr == expected
            or actual_unit == expected
            ): return True

        if ("san[]" in [actual, actual_arr]
            and isinstance(val, ArrayLiteral)
            and len(val.elements) == 0):
            return True

        return False

    def is_accessible(self, actual_type: TokenType) -> bool:
        'determines if a type is accessable'
        return actual_type.is_arr_type() or actual_type == TokenType.SENPAI

    ## HELPER METHODS TO EXTRACT TYPES
    def extract_id(self, accessor: Token | FnCall | IndexedIdentifier | ClassAccessor) -> Token:
        'gets the very first id of a class accessor'
        match accessor:
            case Token():
                return accessor
            case FnCall():
                return accessor.id
            case IndexedIdentifier():
                match accessor.id:
                    case Token():
                        return accessor.id
                    case FnCall():
                        return accessor.id.id
                    case _:
                        raise ValueError(f"Unknown class accessor: {accessor}")
            case ClassAccessor():
                return self.extract_id(accessor.id)
            case _:
                raise ValueError(f"Unknown class accessor: {accessor}")

    def extract_last_id(self, val: Token | FnCall | IndexedIdentifier | ClassAccessor, local_defs: dict[str, tuple[Declaration, Token, GlobalType]]
                        ) -> tuple[str, Token, Declaration, Token, GlobalType]:
        match val:
            case Token():
                return val.string(), val, *local_defs[val.flat_string()]
            case FnCall():
                return val.id.string(), val.id, *local_defs[val.id.flat_string()]
            case IndexedIdentifier():
                match val.id:
                    case Token():
                        return val.id.string(), val.id, *local_defs[val.id.flat_string()]
                    case FnCall():
                        return val.id.id.string(), val.id.id, *local_defs[val.id.id.flat_string()]
                    case _:
                        raise ValueError(f"Unknown class accessor: {val}")
            case ClassAccessor():
                class_type = local_defs[val.id.flat_string()][0]
                val_tmp = val
                while isinstance(val_tmp, ClassAccessor):
                    match val_tmp.accessed:
                        case Token():
                            accessed = f"{class_type.id.flat_string()}.{val_tmp.accessed.flat_string()}"
                            return accessed, val_tmp.accessed, *self.class_signatures[accessed]
                        case FnCall():
                            accessed =f"{class_type.id.flat_string()}.{val_tmp.accessed.id.flat_string()}" 
                            return accessed, val_tmp.accessed.id, *self.class_signatures[accessed]
                        case IndexedIdentifier():
                            match val_tmp.accessed.id:
                                case Token():
                                    accessed = f"{class_type.id.flat_string()}.{val_tmp.accessed.id.flat_string()}"
                                    return accessed, val_tmp.accessed.id, *self.class_signatures[accessed]
                                case FnCall():
                                    accessed = f"{class_type.id.flat_string()}.{val_tmp.accessed.id.id.flat_string()}"
                                    return accessed, val_tmp.accessed.id.id, *self.class_signatures[accessed]
                                case _:
                                    raise ValueError(f"Unknown class accessor: {val}")
                        case ClassAccessor():
                            val_tmp = val_tmp.accessed
                        case _:
                            raise ValueError(f"Unknown class accessor: {val}")
                raise Exception("should not reach here")
            case _:
                raise ValueError(f"Unknown class accessor: {val}")
