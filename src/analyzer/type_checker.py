from copy import deepcopy
from .error_handler import GlobalType
from src.analyzer.error_handler import *
from src.lexer.token import Token, UniqueTokenType
from src.parser.productions import *

class IdProd(Enum):
    TOKEN = 0
    FN_CALL = 1
    INDEXED_ID = 2
class Signature:
    def __init__(
        self,
        decl: Declaration = Declaration(),
        dtype: Token = Token(),
        global_type: GlobalType = GlobalType.IDENTIFIER
    ):
        self.decl = decl
        self.dtype = dtype
        self.global_type = global_type
    def items(self):
        return (self.decl, self.dtype, self.global_type)

class TypeChecker:
    def __init__(self, program: Program):
        self.program = program
        self.errors = []

        # Declaration, data type Token, GlobalType
        self.global_defs: dict[str, Signature] = {}
        self.class_signatures: dict[str, Signature] = {}

        # map of function/method name to list of param data types
        self.function_param_types: dict[str, list[Token]] = {}
        self.class_method_param_types: dict[str, list[Token]] = {}

        # map class constructor name to list of param data types
        self.class_param_types: dict[str, list[Token]] = {}

        # shared state
        ## used for checking if a function has return statements
        self.return_list: list[Token] = []
        ## used for indicating that fn calls should be
        ## checked if it is a method call first
        self.in_class_type: Token = Token()

        self.compile_global_types()
        self.check_program()

    def compile_global_types(self):
        '''
        populates the self.global_types dict with the unique global names
        any duplicates will be appended to error
        '''
        for global_dec in self.program.globals:
            self.global_defs[global_dec.id.flat_string()] = Signature(global_dec, global_dec.dtype, GlobalType.IDENTIFIER)
        for func in self.program.functions:
            self.global_defs[func.id.flat_string()] = Signature(Declaration(), func.rtype, GlobalType.FUNCTION)
            self.function_param_types[func.id.flat_string()] = [param.dtype for param in func.params]
        for cwass in self.program.classes:
            self.global_defs[cwass.id.flat_string()] = Signature(Declaration(), cwass.id, GlobalType.CLASS)
            self.class_param_types[cwass.id.flat_string()] = [param.dtype for param in cwass.params]
            for param in cwass.params:
                self.class_signatures[f"{cwass.id.flat_string()}.{param.id.flat_string()}"] = Signature(param, param.dtype, GlobalType.CLASS_PROPERTY)
            for prop in cwass.properties:
                self.class_signatures[f"{cwass.id.flat_string()}.{prop.id.flat_string()}"] = Signature(prop, prop.dtype, GlobalType.CLASS_PROPERTY)
            for method in cwass.methods:
                self.class_signatures[f"{cwass.id.flat_string()}.{method.id.flat_string()}"] = Signature(Declaration(), method.rtype, GlobalType.CLASS_METHOD)
                self.class_method_param_types[f"{cwass.id.flat_string()}.{method.id.flat_string()}"] = [param.dtype for param in method.params]
        self.compile_std_types()
        self.compile_std_fns()

    def compile_std_types(self):
        self.builtin_signatures: set[str] = {
            'chan.abs',
            'chan.pow',
            'chan.sqrt',
            'chan.isNegative',
            'chan.isPositive',
            'chan.float',

            'kun.abs',
            'kun.pow',
            'kun.sqrt',
            'kun.isNegative',
            'kun.isPositive',
            'kun.ceil',
            'kun.floor',
            'kun.int',

            'senpai.len',
            'senpai.reversed',
            'senpai.has',
            'senpai.upper',
            'senpai.lower',
            'senpai.concat',
            'senpai.prepend',
            'senpai.count',
            'senpai.endswith',
            'senpai.startswith',
            'senpai.index',
            'senpai.replace',
            'senpai.strip',
            'senpai.split',
            'senpai.swapcase',
            'senpai.title',
            'senpai.first',
            'senpai.last',
            'senpai.substr',
            'senpai.from',
            'senpai.upTo',

            'array_type.len',
            'array_type.reverse',
            'array_type.append',
            'array_type.has',
            'array_type.clear',
            'array_type.count',
            'array_type.extend',
            'array_type.index',
            'array_type.pop',
            'array_type.prepend',
            'array_type.prextend',
            'array_type.dimension',
            'array_type.first',
            'array_type.flatten',
            'array_type.join',
            'array_type.last',
            'array_type.replace',
            'array_type.shift',
        }
        self.class_signatures.update(
            {
                'chan.abs': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'chan.pow': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'chan.sqrt': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'chan.isNegative': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'chan.isPositive': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'chan.float': Signature(Declaration(), Token.from_type(TokenType.KUN), GlobalType.CLASS_METHOD),

                'kun.abs': Signature(Declaration(), Token.from_type(TokenType.KUN), GlobalType.CLASS_METHOD),
                'kun.pow': Signature(Declaration(), Token.from_type(TokenType.KUN), GlobalType.CLASS_METHOD),
                'kun.sqrt': Signature(Declaration(), Token.from_type(TokenType.KUN), GlobalType.CLASS_METHOD),
                'kun.isNegative': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'kun.isPositive': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'kun.ceil': Signature(Declaration(), Token.from_type(TokenType.KUN), GlobalType.CLASS_METHOD),
                'kun.floor': Signature(Declaration(), Token.from_type(TokenType.KUN), GlobalType.CLASS_METHOD),
                'kun.int': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),

                'senpai.len': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'senpai.reversed': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.has': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'senpai.upper': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.lower': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.concat': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.prepend': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.count': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'senpai.endswith': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'senpai.startswith': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'senpai.index': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'senpai.replace': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.strip': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.split': Signature(Declaration(), Token.from_type(TokenType.SENPAI_ARR), GlobalType.CLASS_METHOD),
                'senpai.swapcase': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.title': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.first': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.last': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.substr': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.from': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'senpai.upTo': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),

                'array_type.len': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'array_type.reverse': Signature(Declaration(), Token.from_type(TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.has': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.CLASS_METHOD),
                'array_type.append': Signature(Declaration(), Token.from_type(TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.clear': Signature(Declaration(), Token.from_type(TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.count': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'array_type.extend': Signature(Declaration(), Token.from_type(TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.index': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'array_type.pop': Signature(Declaration(), Token.from_type(TokenType.ARRAY_ELEMENT), GlobalType.CLASS_METHOD),
                'array_type.prepend': Signature(Declaration(), Token.from_type(TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.prextend': Signature(Declaration(), Token.from_type(TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.dimension': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.CLASS_METHOD),
                'array_type.first': Signature(Declaration(), Token.from_type(TokenType.GEN_ARRAY), GlobalType.CLASS_METHOD),
                'array_type.flatten': Signature(Declaration(), Token.from_type(TokenType.ONE_D_ARRAY), GlobalType.CLASS_METHOD),
                'array_type.join': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.CLASS_METHOD),
                'array_type.last': Signature(Declaration(), Token.from_type(TokenType.GEN_ARRAY), GlobalType.CLASS_METHOD),
                'array_type.replace': Signature(Declaration(), Token.from_type(TokenType.SAN), GlobalType.CLASS_METHOD),
                'array_type.shift': Signature(Declaration(), Token.from_type(TokenType.ARRAY_ELEMENT), GlobalType.CLASS_METHOD),
            },
        )
        self.class_method_param_types.update(
            {
                'chan.abs': [],
                'chan.pow': [Token.from_type(TokenType.NUMBER)],
                'chan.sqrt': [],
                'chan.isNegative': [],
                'chan.isPositive': [],
                'chan.float': [],

                'kun.abs': [],
                'kun.pow': [Token.from_type(TokenType.NUMBER)],
                'kun.sqrt': [],
                'kun.isNegative': [],
                'kun.isPositive': [],
                'kun.ceil': [],
                'kun.floor': [],
                'kun.int': [],

                'senpai.len': [],
                'senpai.reversed': [],
                'senpai.has': [Token.from_type(TokenType.SENPAI)],
                'senpai.upper': [],
                'senpai.lower': [],
                'senpai.concat': [Token.from_type(TokenType.SENPAI)],
                'senpai.prepend': [Token.from_type(TokenType.SENPAI)],
                'senpai.count': [Token.from_type(TokenType.SENPAI)],
                'senpai.endswith': [Token.from_type(TokenType.SENPAI)],
                'senpai.startswith': [Token.from_type(TokenType.SENPAI)],
                'senpai.index': [Token.from_type(TokenType.SENPAI)],
                'senpai.replace': [Token.from_type(TokenType.SENPAI), Token.from_type(TokenType.SENPAI)],
                'senpai.strip': [],
                'senpai.split': [],
                'senpai.swapcase': [],
                'senpai.title': [],
                'senpai.first': [Token.from_type(TokenType.CHAN)],
                'senpai.last': [Token.from_type(TokenType.CHAN)],
                'senpai.substr': [Token.from_type(TokenType.CHAN), Token.from_type(TokenType.CHAN)],
                'senpai.from': [Token.from_type(TokenType.SENPAI)],
                'senpai.upTo': [Token.from_type(TokenType.SENPAI)],

                'array_type.len': [],
                'array_type.reverse': [],
                'array_type.append': [Token.from_type(TokenType.ARRAY_ELEMENT)],
                'array_type.has': [Token.from_type(TokenType.ARRAY_ELEMENT)],
                'array_type.clear': [],
                'array_type.count': [Token.from_type(TokenType.ARRAY_ELEMENT)],
                'array_type.extend': [Token.from_type(TokenType.GEN_ARRAY)],
                'array_type.index': [Token.from_type(TokenType.ARRAY_ELEMENT)],
                'array_type.pop': [],
                'array_type.prepend': [Token.from_type(TokenType.ARRAY_ELEMENT)],
                'array_type.prextend': [Token.from_type(TokenType.GEN_ARRAY)],
                'array_type.dimension': [],
                'array_type.first': [Token.from_type(TokenType.CHAN)],
                'array_type.flatten': [],
                'array_type.join': [Token.from_type(TokenType.SENPAI)],
                'array_type.last': [Token.from_type(TokenType.CHAN)],
                'array_type.replace': [Token.from_type(TokenType.ARRAY_ELEMENT), Token.from_type(TokenType.ARRAY_ELEMENT)],
                'array_type.shift': [],
            }
        )

    def compile_std_fns(self):
        self.global_defs.update({
            'randomInt': Signature(Declaration(), Token.from_type(TokenType.CHAN), GlobalType.FUNCTION),
            'randomFloat': Signature(Declaration(), Token.from_type(TokenType.KUN), GlobalType.FUNCTION),
            'randomString': Signature(Declaration(), Token.from_type(TokenType.SENPAI), GlobalType.FUNCTION),
            'randomBool': Signature(Declaration(), Token.from_type(TokenType.SAMA), GlobalType.FUNCTION),
        })
        self.function_param_types.update({
            'randomInt': [Token.from_type(TokenType.NUMBER), Token.from_type(TokenType.NUMBER)],
            'randomFloat': [Token.from_type(TokenType.NUMBER), Token.from_type(TokenType.NUMBER)],
            'randomBool': [],
            'randomString': [Token.from_type(TokenType.NUMBER)],
        })

    def check_program(self) -> None:
        assert self.program.mainuwu
        self.check_function(self.program.mainuwu, self.global_defs.copy())
        for func in self.program.functions: self.check_function(func, self.global_defs)
        for cwass in self.program.classes: self.check_class(cwass, self.global_defs.copy())

    def check_function(self, func: Function, local_defs: dict[str, Signature], cwass: str|None = None) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        self.compile_params(func.params, local_defs)
        self.check_body(func.body, func.rtype, local_defs.copy())
        if len(self.return_list) == 0 and func.rtype.flat_string() != 'san':
            self.errors.append(NoReturnStatement(func, cwass=cwass))
        self.return_list.clear()

    def check_class(self, cwass: Class, local_defs: dict[str, Signature]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        self.in_class_type = cwass.id
        self.compile_params(cwass.params, local_defs)
        for prop in cwass.properties:
            self.check_declaration(prop, local_defs)
        for method in cwass.methods:
            self.check_function(method, local_defs, cwass=cwass.id.flat_string())
        self.in_class_type = Token()

    def compile_params(self, params: list[Declaration], local_defs: dict[str, Signature]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        for param in params:
            local_defs[param.id.flat_string()] = Signature(param, param.dtype, GlobalType.IDENTIFIER)

    def check_body(self, body: BlockStatement, return_type: Token, local_defs: dict[str, Signature]) -> None:
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
                case Break(): pass
                case _: raise ValueError(f"Unknown statement: {statement}")

    def check_print(self, print: Print, local_defs: dict[str, Signature]) -> None:
        for val in print.values: self.evaluate_value(val, local_defs)

    def check_input(self, input: Input, local_defs: dict[str, Signature]) -> None:
        self.evaluate_value(input.expr, local_defs)

    def check_if(self, if_stmt: IfStatement | ElseIfStatement, return_type: Token, local_defs: dict[str, Signature], else_if=False) -> None:
        self.evaluate_value(if_stmt.condition, local_defs)
        self.check_body(if_stmt.then, return_type, local_defs.copy())
        if else_if: return
        assert isinstance(if_stmt, IfStatement)
        for elif_stmt in if_stmt.else_if:
            self.check_if(elif_stmt, return_type, local_defs, else_if=True)
        if if_stmt.else_block:
            self.check_body(if_stmt.else_block, return_type, local_defs.copy())

    def check_while_loop(self, while_loop: WhileLoop, return_type: Token, local_defs: dict[str, Signature]) -> None:
        self.evaluate_value(while_loop.condition, local_defs)
        self.check_body(while_loop.body, return_type, local_defs.copy())

    def check_for_loop(self, for_loop: ForLoop, return_type: Token, local_defs: dict[str, Signature]) -> None:
        'pass in a copy of local defs when calling this'
        match for_loop.init:
            case Declaration():
                self.check_declaration(for_loop.init, local_defs)
                signature = local_defs[for_loop.init.id.flat_string()]
            case Assignment():
                self.check_assignment(for_loop.init, local_defs)
                signature = local_defs[self.extract_id(for_loop.init.id).flat_string()]
            case Token():
                self.evaluate_token(for_loop.init, local_defs)
                match for_loop.init.token:
                    case Token(): signature = Signature()
                    case UniqueTokenType():
                        signature = local_defs[for_loop.init.flat_string()]
                    case _:
                        raise ValueError(f"Unknown token: {for_loop.init}")
            case IdentifierProds():
                self.evaluate_ident_prods(for_loop.init, local_defs)
                signature = self.extract_last_id(for_loop.init, local_defs)[2]

        if signature.decl.dono_token.exists():
            token = self.extract_id(for_loop.init.id)
            self.errors.append(
                ReassignedConstantError(
                    token = token,
                    defined_token = signature.decl.dono_token,
                    header = f"Constant in for loop initializer: {token.flat_string()}",
                    token_msg = "Tried to use constant in a for loop initializer",
                )
            )

        self.evaluate_value(for_loop.condition, local_defs)
        self.evaluate_value(for_loop.update, local_defs)
        self.check_body(for_loop.body, return_type, local_defs.copy())

    def check_return(self, ret: ReturnStatement, return_type: Token, local_defs: dict[str, Signature]) -> None:
        actual_type = self.evaluate_value(ret.expr, local_defs)
        if actual_type.type_is(TokenType.SAN) and not return_type.type_is(TokenType.SAN):
            self.errors.append(
                ReturnTypeMismatchError(
                    expected=return_type,
                    return_stmt = ret,
                    actual_type=actual_type,
                )
            )
            return
        elif not self.is_similar_type(actual_type, return_type, ret.expr):
            self.errors.append(
                ReturnTypeMismatchError(
                    expected=return_type,
                    return_stmt = ret,
                    actual_type=actual_type,
                )
            )
        self.return_list.append(actual_type)

    def check_declaration(self, decl: Declaration, local_defs: dict[str, Signature]) -> None:
        self.check_value(decl.value, decl.dtype, local_defs, decl=decl)

    def check_assignment(self, assign: Assignment, local_defs: dict[str, Signature]) -> None:
        last_id, token, _ = self.extract_last_id(assign.id, local_defs)
        defined = True
        if last_id in local_defs:
            signature = local_defs[last_id]
            class_member = False
        else:
            signature = self.class_signatures[last_id]
            if last_id in self.builtin_signatures or not signature.decl.id.exists():
                defined = False
            class_member = True

        if signature.decl.dono_token.exists():
            last_id = self.extract_id(assign.id)
            self.errors.append(
                ReassignedConstantError(
                    token = last_id,
                    defined_token = signature.decl.dono_token,
                    header = f"Reassigning constant: {last_id.flat_string()}",
                    token_msg = "Tried to reassign here",
                )
            )
            return
        elif signature.global_type in [GlobalType.FUNCTION, GlobalType.CLASS_METHOD]:
            self.errors.append(
                FunctionAssignmentError(
                    original=signature.decl.id if defined else None,
                    assignment=token,
                    class_signature=last_id,
                )
            )
        last_prod, id_prod_type = self.extract_last_id_prod(assign.id, local_defs)
        id_is_subscripting_string = (id_prod_type == IdProd.INDEXED_ID and signature.dtype.type_is_in([TokenType.SENPAI, TokenType.SENPAI_ARR])
                                and not (
                                    signature.dtype.type_is(TokenType.SENPAI_ARR)
                                    and isinstance(last_prod, IndexedIdentifier)
                                    and len(last_prod.index) <= signature.dtype.dimension()
                                )
                            )
        if id_is_subscripting_string:
            assert isinstance(last_prod, IndexedIdentifier)
            self.errors.append(
                SubstringAssignmentError(
                    id_prod=assign.id,
                    indexed_id = last_prod,
                    dimension = signature.decl.dtype.dimension(),
                    val = assign.value,
                    defined_token = signature.decl.dono_token,
                )
            )
            return

        self.check_value(assign.value, signature.dtype, local_defs, assignment=True, decl=signature.decl, assign=assign,
                         class_member=class_member, indexed_id=id_prod_type == IdProd.INDEXED_ID)

    def check_value(self, value: Value, expected_type: Token, local_defs: dict[str, Signature],
                    assignment: bool = False, decl: Declaration = Declaration(), assign: Assignment = Assignment(),
                    indexed_id=False, class_member=False) -> None:
        'if `assignment` is true, its an assignment. if false, its a declaration'
        self.expr_err_count = 0

        match expected_type.token:
            case TokenType():
                actual_type = self.evaluate_value(value, local_defs)
                match value:
                    case Input():
                        if not value.concats: actual_type_new = Token.from_type(TokenType.INPWT) # "inpwt"
                        else: actual_type_new = Token.from_type(TokenType.SENPAI)
                    case _: actual_type_new = actual_type
                if not self.is_similar_type(actual_type_new, expected_type, value, indexing=indexed_id):
                    self.errors.append(
                        TypeMismatchError(
                            title="Assignment" if assignment else "Declaration",
                            expected=expected_type,
                            actual_val=value,
                            actual_type=actual_type,
                            context=assign if assignment else decl,
                            indexing=indexed_id,
                        )
                    )
            case UniqueTokenType():
                match value:
                    case ClassConstructor():
                        actual_type = Token()
                        self.check_class_constructor(value, local_defs)
                    case _:
                        actual_type = self.evaluate_value(value, local_defs)
                        if not self.is_similar_type(actual_type, expected_type, value, indexing=indexed_id):
                            self.errors.append(
                                TypeMismatchError(
                                    title="Assignment" if assignment else "Declaration",
                                    expected=expected_type,
                                    actual_val=value,
                                    actual_type=actual_type,
                                    context=assign if assignment else decl,
                                    indexing=indexed_id,
                                )
                            )
        # (DECLARATION & ASSIGNMENT) uninitialize identifiers if any errors occured in evaluating value
        if self.expr_err_count > 0 and not expected_type.type_is(TokenType.SAN):
            decl_new = deepcopy(decl)
            decl_new.initialized = False
            decl_new.value = Value()
            if class_member:
                repr = f"{expected_type.flat_string()}.{decl_new.id.flat_string()}"
                self.class_signatures[repr] = Signature(decl_new, decl_new.dtype, GlobalType.IDENTIFIER)
            else:
                local_defs[decl_new.id.flat_string()] = Signature(decl_new, decl_new.dtype, GlobalType.IDENTIFIER)

        # (ASSIGNMENT) initialize uninitialized identifiers
        elif not decl.initialized and not actual_type.type_is(TokenType.SAN):
            decl_new = deepcopy(decl)
            decl_new.initialized = True
            if class_member:
                repr = f"{expected_type.flat_string()}.{decl_new.id.flat_string()}"
                self.class_signatures[repr] = Signature(decl_new, decl_new.dtype, GlobalType.IDENTIFIER)
            else:
                local_defs[decl_new.id.flat_string()] = Signature(decl_new, decl_new.dtype, GlobalType.IDENTIFIER)

        # (DECLARATION & ASSIGNMENT) initialize identifiers with assigned values
        else:
            if class_member:
                repr = f"{expected_type.flat_string()}.{decl.id.flat_string()}"
                self.class_signatures[repr] = Signature(decl, decl.dtype, GlobalType.IDENTIFIER)
            else:
                local_defs[decl.id.flat_string()] = Signature(decl, decl.dtype, GlobalType.IDENTIFIER)

        if assignment: assign.dtype = actual_type
        self.expr_err_count = 0

    def evaluate_value(self, value: Value | Token, local_defs: dict[str, Signature]) -> Token:
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
                return Token.from_type(TokenType.SAN)

    def evaluate_expression(self, expr: Expression, local_defs: dict[str, Signature]) -> Token:
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
                                left_type=left if left.token not in self.math_operands() else Token(),
                                right_type=right if right.token not in self.math_operands() else Token(),
                            )
                        )
                        self.expr_err_count += 1
                    if left == TokenType.KUN or right == TokenType.KUN:
                        return Token.from_type(TokenType.KUN)
                    else:
                        return Token.from_type(TokenType.CHAN)
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
                                left_type=left if left.token not in self.math_operands() else Token(),
                                right_type=right if right.token not in self.math_operands() else Token(),
                            )
                        )
                        self.expr_err_count += 1
                    return Token.from_type(TokenType.SAMA)
                elif expr.op.token in self.equality_operators():
                    return Token.from_type(TokenType.SAMA)
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

    def evaluate_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, Signature]) -> Token:
        match ident_prod:
            case IndexedIdentifier():
                self.check_indexed_id_indices(ident_prod, local_defs)
                match ident_prod.id:
                    case Token():
                        arr_type = self.evaluate_token(ident_prod.id, local_defs)
                    case FnCall():
                        id_type = local_defs[self.extract_id(ident_prod).flat_string()][1]
                        arr_type = self.evaluate_fn_call(ident_prod.id, local_defs, self_type=id_type)
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
                    return Token.from_type(TokenType.SAN)
                if (not arr_type.to_unit_type(len(ident_prod.index)).type_is(TokenType.SENPAI)
                    and arr_type.dimension() < len(ident_prod.index)):
                    self.errors.append(
                        NonIterableIndexingError(
                            token=self.extract_id(ident_prod.id),
                            type_definition=arr_type,
                            token_type=arr_type.to_unit_type(len(ident_prod.index)),
                            usage=ident_prod.flat_string(),
                        )
                    )
                    return Token.from_type(TokenType.SAN)
                return arr_type.to_unit_type(len(ident_prod.index))
            case FnCall():
                return self.evaluate_fn_call(ident_prod, local_defs)
            case ClassConstructor():
                self.check_class_constructor(ident_prod, local_defs)
                return Token.from_type(ident_prod.id.token)
            case ClassAccessor():
                return self.check_and_evaluate_class_accessor(ident_prod, local_defs)
            case _:
                raise ValueError(f"Unknown identifier production: {ident_prod}")

    def check_indexed_id_indices(self, indexed_id: IndexedIdentifier, local_defs: dict[str, Signature]) -> None:
        dtypes: list[Token] = []
        ok: list[bool] = []
        for idx in indexed_id.index:
            dtype = self.evaluate_value(idx, local_defs)
            dtypes.append(dtype)
            ok.append(self.is_similar_type(dtype, Token.from_type(TokenType.CHAN), idx, as_index=True))
        if not all(ok):
            self.errors.append(
                NonNumberIndex(
                    indexed_id=indexed_id,
                    indices=indexed_id.index,
                    actual_types=dtypes,
                    ok=ok,
                )
            )

    def check_and_evaluate_class_accessor(
            self, accessor: ClassAccessor, local_defs: dict[str, Signature],
            *, class_type: Token = Token(), parent_type: Token = Token(),
        ) -> Token:

        # type check accessor
        id = self.extract_id(accessor).flat_string()
        match accessor.id:
            case Token():
                try: definition, class_type, global_type = self.class_signatures[f"{parent_type}.{id}"].items()
                except: definition, class_type, global_type = local_defs[id].items()
                if not self.is_accessible(class_type):
                    self.errors.append(
                        NonClassAccessError(
                            id=self.extract_id(accessor),
                            id_definition=class_type,
                            usage=accessor.flat_string(),
                        )
                    )
                elif not definition.initialized and global_type in [GlobalType.CLASS_PROPERTY, GlobalType.IDENTIFIER]:
                    self.errors.append(
                        NonClassAccessError(
                            id=self.extract_id(accessor),
                            id_definition=class_type,
                            usage=accessor.flat_string(),
                            initialized=False
                        )
                    )
            case FnCall():
                if parent_type.exists(): class_type = self.evaluate_method_call(parent_type, accessor.id, local_defs)
                else: class_type = self.evaluate_fn_call(accessor.id, local_defs)
            case IndexedIdentifier():
                try: definition, class_type, global_type = self.class_signatures[f"{parent_type}.{id}"].items()
                except: definition, class_type, global_type = local_defs[id].items()
                if class_type.dimension() < len(accessor.id.index):
                    token = self.extract_id(accessor.id)
                    type_definition = local_defs[token.flat_string()].decl.dtype
                    self.errors.append(
                        NonIterableIndexingError(
                            token=token,
                            type_definition=type_definition,
                            token_type=class_type,
                            usage=accessor.id.flat_string(),
                        )
                    )
                if not self.is_accessible(class_type):
                    self.errors.append(
                        NonClassAccessError(
                            id=self.extract_id(accessor),
                            id_definition=class_type,
                            usage=accessor.flat_string(),
                        )
                    )
                class_type = class_type.to_unit_type(len(accessor.id.index))
            case ClassAccessor():
                match (res := self.extract_id_prod(accessor.id)):
                    case Token(): pass
                    case FnCall():
                        if parent_type.exists(): self.evaluate_method_call(parent_type, res, local_defs)
                        else: self.evaluate_fn_call(res, local_defs)
                    case IndexedIdentifier(): self.check_indexed_id_indices(res, local_defs)

        # type check accessed
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
                    return Token.from_type(TokenType.SAN)
                if res.global_type != GlobalType.CLASS_PROPERTY:
                    self.errors.append(
                        UndefinedClassMember(
                            class_type.flat_string(),
                            accessed,
                            GlobalType.CLASS_PROPERTY,
                            actual_definition=(res.decl.id, res.global_type),
                        )
                    )
                    return Token.from_type(TokenType.SAN)
                return res.dtype
            case FnCall():
                accessed = accessor.accessed.id
                return self.evaluate_method_call(class_type, accessor.accessed, local_defs)
            case IndexedIdentifier():
                self.check_indexed_id_indices(accessor.accessed, local_defs)
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
                            return Token.from_type(TokenType.SAN)
                        if res.global_type != GlobalType.CLASS_PROPERTY:
                            self.errors.append(
                                UndefinedClassMember(
                                    class_type.flat_string(),
                                    accessed,
                                    GlobalType.CLASS_PROPERTY,
                                    actual_definition=(res.dtype, res.global_type),
                                )
                            )
                            return Token.from_type(TokenType.SAN)
                        if not self.is_accessible(res.dtype):
                            token = self.extract_id(accessed)
                            type_definition = self.class_signatures[member_signature].decl
                            self.errors.append(
                                NonIterableIndexingError(
                                    token=token,
                                    type_definition=type_definition.id,
                                    token_type=res.dtype,
                                    usage=accessed.flat_string(),
                                )
                            )
                            return Token.from_type(TokenType.SAN)
                        return res.dtype.to_unit_type()
                    case FnCall():
                        return self.evaluate_method_call(class_type, accessed, local_defs).to_unit_type()
                    case _:
                        raise ValueError(f"Unknown class accessor: {accessor}")
            case ClassAccessor():
                id = self.extract_id(accessor.accessed.id)
                member_signature = f"{class_type.flat_string()}.{id.flat_string()}"
                if (res := self.class_signatures.get(member_signature)) is None:
                    self.errors.append(
                        UndefinedClassMember(
                            class_type.flat_string(),
                            id,
                            GlobalType.CLASS_PROPERTY,
                        )
                    )
                    return Token.from_type(TokenType.SAN)
                return self.check_and_evaluate_class_accessor(
                    accessor.accessed, local_defs,
                    class_type=res.dtype, parent_type=class_type,
                )
            case _:
                raise ValueError(f"Unknown class accessor: {accessor}")

    def evaluate_iterable(self, collection: Iterable, local_defs: dict[str, Signature]) -> Token:
        match collection:
            case ArrayLiteral(): return self.expect_homogenous(collection, local_defs)
            case StringFmt():
                for val in collection.exprs:
                    self.evaluate_value(val, local_defs)
                for concat in collection.concats:
                    self.evaluate_iterable(concat, local_defs)
                return Token.from_type(TokenType.SENPAI)
            case Input():
                self.evaluate_value(collection.expr, local_defs)
                for concat in collection.concats:
                    self.evaluate_iterable(concat, local_defs)
                return Token.from_type(TokenType.SENPAI)
            case StringLiteral():
                for concat in collection.concats:
                    self.evaluate_iterable(concat, local_defs)
                return Token.from_type(TokenType.SENPAI)
            case _:
                raise ValueError(f"Unknown collection: {collection}")

    def evaluate_method_call(self, class_type: Token, fn_call: FnCall, local_defs: dict[str, Signature]) -> Token:
        class_id_str = class_type.flat_string() if not class_type.token.is_arr_type() else 'array_type'
        if (res := self.class_signatures.get(f"{class_id_str}.{fn_call.id.flat_string()}")) is None:
            self.errors.append(
                UndefinedClassMember(
                    class_type.flat_string(),
                    fn_call.id,
                    GlobalType.CLASS_METHOD,
                )
            )
            return Token.from_type(TokenType.SAN)
        if res.global_type != GlobalType.CLASS_METHOD:
            self.errors.append(
                UndefinedClassMember(
                    class_type.flat_string(),
                    fn_call.id,
                    GlobalType.CLASS_METHOD,
                    actual_definition=(res.dtype, res.global_type),
                )
            )
            return Token.from_type(TokenType.SAN)

        method_signature = f"{class_id_str}.{fn_call.id.flat_string()}"
        expected_types = self.class_method_param_types[method_signature]
        all_defs = self.class_signatures.copy()
        all_defs.update(local_defs)
        self.check_call_args(GlobalType.CLASS_METHOD, method_signature, fn_call.id,
                             fn_call.args, expected_types, all_defs, class_type)

        match res.dtype.token:
            case TokenType.GEN_ARRAY: return class_type
            case TokenType.ARRAY_ELEMENT: return class_type.to_unit_type()
            case TokenType.ONE_D_ARRAY:
                while class_type.dimension() > 1: class_type = class_type.to_unit_type()
                return class_type
            case _: return res.dtype

    def check_call_args(self, global_type: GlobalType, call_str: str, id: Token, call_args: list[Value], expected_types: list[Token],
                        local_defs: dict[str, Signature], self_type: Token= Token()) -> None:
        actual_types: list[Token] = []
        matches: list[bool] = []
        for arg, expected in zip(call_args, expected_types):
            match arg:
                case Token():
                    match arg.token:
                        case UniqueTokenType():
                            actual_def = local_defs[arg.flat_string()].decl
                            actual = actual_def.dtype
                            if not actual_def.initialized: actual = Token.from_type(TokenType.SAN)
                        case TokenType():
                            actual = self.evaluate_token(arg, local_defs)
                case _:
                    actual = self.evaluate_value(arg, local_defs)
            actual_types.append(actual)
            match expected.token:
                case TokenType.ARRAY_ELEMENT:
                    matches.append(self.is_element_of_expected(actual, self_type if self_type.exists() else expected, arg))
                case TokenType.GEN_ARRAY:
                    matches.append(self.is_similar_type(actual, self_type if self_type.exists() else expected, arg))
                case TokenType.NUMBER:
                    matches.append(self.is_similar_type(actual, Token.from_type(TokenType.CHAN), arg))
                case _:
                    matches.append(self.is_similar_type(actual, expected, arg, is_call=True))

        if not all(matches) or len(call_args) != len(expected_types):
            expected_types_str: list[str] = []
            for e in expected_types:
                match e.token:
                    case TokenType.ARRAY_ELEMENT:
                        expected_types_str.append(f"{self_type.to_unit_type()}")
                    case TokenType.GEN_ARRAY:
                        expected_types_str.append(f"{self_type}")
                    case TokenType.NUMBER:
                        expected_types_str.append("chan, kun, or sama")
                    case _:
                        expected_types_str.append(f"{e}")
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

    def evaluate_fn_call(self, fn_call: FnCall, local_defs: dict[str, Signature],
                         *, self_type: Token = Token()) -> Token:
        if self.in_class_type.exists():
            fn_call.need_self = True
            expected_types = self.class_method_param_types[f"{self.in_class_type.flat_string()}.{fn_call.id.flat_string()}"]
            ret_type = self.class_signatures[f"{self.in_class_type.flat_string()}.{fn_call.id.flat_string()}"][1]
        else:
            expected_types = self.function_param_types[fn_call.id.flat_string()]
            ret_type = local_defs[fn_call.id.flat_string()][1]
        self.check_call_args(GlobalType.FUNCTION, fn_call.id.flat_string(), fn_call.id, fn_call.args, expected_types, local_defs)
        match ret_type:
            case TokenType.GEN_ARRAY:
                return self_type if self_type.exists() else Token.from_type(TokenType.SAN)
            case TokenType.ARRAY_ELEMENT:
                return self_type.to_unit_type() if self_type.exists() else Token.from_type(TokenType.SAN)
            case TokenType.ONE_D_ARRAY:
                if self_type.exists():
                    while self_type.dimension() > 1: self_type = self_type.to_unit_type()
                    return self_type
                else: return Token.from_type(TokenType.SAN)
            case _: return ret_type

    def check_class_constructor(self, class_constructor: ClassConstructor, local_defs: dict[str, Signature]) -> None:
        expected_types = self.class_param_types[class_constructor.id.flat_string()]
        self.check_call_args(GlobalType.CLASS, class_constructor.id.flat_string(), class_constructor.id, class_constructor.args, expected_types, local_defs)

    def evaluate_token(self, token: Token, local_defs: dict[str, Signature]) -> Token:
        match token.token:
            case TokenType.STRING_LITERAL: ret = TokenType.SENPAI
            case TokenType.INT_LITERAL: ret = TokenType.CHAN
            case TokenType.FLOAT_LITERAL: ret = TokenType.KUN
            case TokenType.FAX | TokenType.CAP: ret = TokenType.SAMA
            case TokenType.NUWW: ret = TokenType.SAN
            case UniqueTokenType():
                decl = local_defs[token.flat_string()].decl
                if not decl.initialized:
                    return Token.from_type(TokenType.SAN)
                return decl.dtype
            case _: raise ValueError(f"Unknown token: {token}")
        return Token.from_type(ret)

    ## HELPER METHODS FOR OPERATORS AND OPERANDS
    def math_operands(self) -> list[Token]:
        return list(map(lambda x: Token.from_type(x), [TokenType.CHAN, TokenType.KUN, TokenType.SAMA]))
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
    def expect_homogenous(self, arr: ArrayLiteral, local_defs: dict[str, Signature]) -> Token:
        types: list[Token] = [self.evaluate_value(val, local_defs) for val in arr.elements]
        type_list = [t.flat_string() for t in types]
        if len(set(type_list)) > 1:
            self.errors.append(
                HeterogeneousArrayError(arr, arr.elements, type_list)
            )
            return Token.from_type(TokenType.SAN)
        return types.pop().to_arr_type() if types else Token.from_type(TokenType.SAN_ARR)

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

    def is_similar_type(self, actual_type: Token, expected_type: Token, val: Value,
                         *, is_call = False, as_index=False, indexing=False) -> bool:
        'determines if two types are similar'
        # nuww is an ok val for any type if and only if its not for a call
        condition_2 = (actual_type == Token.from_type(TokenType.SAN)) if not is_call and not as_index else False
        if (actual_type == expected_type
            or condition_2):
            return True

        assert actual_type != expected_type
        match expected_type.lexeme:
            # num types are convertible between each other
            case "chan" | "kun":
                match actual_type.lexeme:
                    # inpwts with no concats can be converted to num types
                    case "chan" | "kun" | "sama": return True
                    case "inpwt": return True if not as_index else False
                    case _: return False
            # inpwt is inherently senpai
            case "senpai":
                match actual_type.lexeme:
                    case "senpai" | "inpwt": return True
                    case _: return False
            # all types are convertible to bool
            case "sama": return True
            case _:
                # all array types can accept its unit types
                if indexing and actual_type == expected_type.to_unit_type():
                    return True

                # all array types can accept san[]
                if expected_type.is_arr_type():
                    if actual_type.type_is(TokenType.SAN_ARR) and actual_type.dimension() >= 1:
                        if isinstance(val, ArrayLiteral):
                            if len(val.elements) == 0: return True
                            else: return False
                        else: return False

                # every other type needs exact match
                return False

    def is_element_of_expected(self, actual_type: Token, expected_type: Token, val: Value) -> bool:
        'determines if a type is a valid element of an expected type'
        if actual_type == expected_type.to_unit_type():
            return True

        if (expected_type.dimension() > 1
            and isinstance(val, ArrayLiteral)
            and len(val.elements) == 0):
            return True
        return False

    def is_accessible(self, actual_type: Token) -> bool:
        'determines if a type is accessable'
        return (
            actual_type.is_arr_type()
            or actual_type.is_unique_type()
            or actual_type.type_is(TokenType.SENPAI)
            or actual_type.type_is(TokenType.CHAN)
            or actual_type.type_is(TokenType.KUN)
        )

    ## HELPER METHODS TO EXTRACT TYPES
    def extract_id(self, accessor: Token | FnCall | IndexedIdentifier | ClassAccessor | IdentifierProds) -> Token:
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

    def extract_id_prod(self, accessor: Token | FnCall | IndexedIdentifier | ClassAccessor) -> Token | FnCall | IndexedIdentifier:
        'gets the very first id of a class accessor'
        match accessor:
            case Token():
                return accessor
            case FnCall():
                return accessor
            case IndexedIdentifier():
                return accessor
            case ClassAccessor():
                return self.extract_id_prod(accessor.id)
            case _:
                raise ValueError(f"Unknown class accessor: {accessor}")

    def extract_last_id(self, val: Token | FnCall | IndexedIdentifier | ClassAccessor, local_defs: dict[str, Signature]
                        ) -> tuple[str, Token, Signature]:
        'returns: signature, id token, definition, dono token, global type, id prod type'
        match val:
            case Token():
                return val.string(), val, local_defs[val.flat_string()]
            case FnCall():
                return val.id.string(), val.id, local_defs[val.id.flat_string()]
            case IndexedIdentifier():
                match val.id:
                    case Token():
                        return val.id.string(), val.id, local_defs[val.id.flat_string()]
                    case FnCall():
                        return val.id.id.string(), val.id.id, local_defs[val.id.id.flat_string()]
                    case _:
                        raise ValueError(f"Unknown class accessor: {val}")
            case ClassAccessor():
                val_tmp = val
                class_type = local_defs[self.extract_id(val_tmp.id).flat_string()].dtype
                while isinstance(val_tmp, ClassAccessor):
                    try: class_type = self.class_signatures[f"{class_type.flat_string()}.{self.extract_id(val_tmp.id).flat_string()}"].dtype
                    except: class_type = local_defs[self.extract_id(val_tmp.id).flat_string()].dtype

                    match val_tmp.accessed:
                        case Token():
                            accessed = f"{class_type.flat_string()}.{val_tmp.accessed.flat_string()}"
                            return accessed, val_tmp.accessed, self.class_signatures[accessed]
                        case FnCall():
                            accessed =f"{class_type.flat_string()}.{val_tmp.accessed.id.flat_string()}" 
                            return accessed, val_tmp.accessed.id, self.class_signatures[accessed]
                        case IndexedIdentifier():
                            match val_tmp.accessed.id:
                                case Token():
                                    accessed = f"{class_type.flat_string()}.{val_tmp.accessed.id.flat_string()}"
                                    return accessed, val_tmp.accessed.id, self.class_signatures[accessed]
                                case FnCall():
                                    accessed = f"{class_type.flat_string()}.{val_tmp.accessed.id.id.flat_string()}"
                                    return accessed, val_tmp.accessed.id.id, self.class_signatures[accessed]
                                case _:
                                    raise ValueError(f"Unknown class accessor: {val}")
                        case ClassAccessor():
                            val_tmp = val_tmp.accessed
                        case _:
                            raise ValueError(f"Unknown class accessor: {val}")
                raise Exception("should not reach here")
            case _:
                raise ValueError(f"Unknown class accessor: {val}")

    def extract_last_id_prod(self, val: Token | FnCall | IndexedIdentifier | ClassAccessor, local_defs: dict[str, Signature]
                        ) -> tuple[Token|FnCall|IndexedIdentifier, IdProd]:
        'returns: id prod, id prod type'
        match val:
            case Token():
                return val, IdProd.TOKEN
            case FnCall():
                return val, IdProd.FN_CALL
            case IndexedIdentifier():
                match val.id:
                    case Token():
                        return val, IdProd.INDEXED_ID
                    case FnCall():
                        return val, IdProd.INDEXED_ID
                    case _:
                        raise ValueError(f"Unknown class accessor: {val}")
            case ClassAccessor():
                val_tmp = val
                while isinstance(val_tmp, ClassAccessor):
                    match val_tmp.accessed:
                        case Token():
                            return val_tmp.accessed, IdProd.TOKEN
                        case FnCall():
                            return val_tmp.accessed, IdProd.FN_CALL
                        case IndexedIdentifier():
                            match val_tmp.accessed.id:
                                case Token():
                                    return val_tmp.accessed, IdProd.INDEXED_ID
                                case FnCall():
                                    return val_tmp.accessed, IdProd.INDEXED_ID
                                case _:
                                    raise ValueError(f"Unknown class accessor: {val}")
                        case ClassAccessor():
                            val_tmp = val_tmp.accessed
                        case _:
                            raise ValueError(f"Unknown class accessor: {val}")
                raise Exception("should not reach here")
            case _:
                raise ValueError(f"Unknown class accessor: {val}")
