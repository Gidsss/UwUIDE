'''
TODO:
- add proper errors instead of printing
'''

from .error_handler import GlobalType
from src.analyzer.error_handler import *
from src.lexer.token import Token, UniqueTokenType
from src.parser.productions import *

class TypeChecker:
    def __init__(self, program: Program):
        self.program = program
        self.errors = []

        # maps global names to their type's token and GlobalType for error message
        self.global_defs: dict[str, tuple[Token, GlobalType]] = {}
        self.class_signatures: dict[str, tuple[Token, GlobalType]] = {}
        self.class_method_param_types: dict[str, list[Token]] = {}
        self.function_param_types: dict[str, list[Token]] = {}
        self.class_param_types: dict[str, list[Token]] = {}
        self.compile_global_types()
        self.check_program()

    def compile_global_types(self):
        '''
        populates the self.global_types dict with the unique global names
        any duplicates will be appended to error
        '''
        for global_dec in self.program.globals:
            self.global_defs[global_dec.id.string()] = (global_dec.dtype, GlobalType.IDENTIFIER)
        for func in self.program.functions:
            self.global_defs[func.id.string()] = (func.rtype, GlobalType.FUNCTION)
            self.function_param_types[func.id.string()] = [param.dtype for param in func.params]
        for cwass in self.program.classes:
            self.global_defs[cwass.id.string()] = (cwass.id, GlobalType.CLASS)
            self.class_param_types[cwass.id.string()] = [param.dtype for param in cwass.params]
            for param in cwass.params:
                self.class_signatures[f"{cwass.id.string()}.{param.id.string()}"] = (param.dtype, GlobalType.CLASS_PROPERTY)
            for prop in cwass.properties:
                self.class_signatures[f"{cwass.id.string()}.{prop.id.string()}"] = (prop.dtype, GlobalType.CLASS_PROPERTY)
            for method in cwass.methods:
                self.class_signatures[f"{cwass.id.string()}.{method.id.string()}"] = (method.rtype, GlobalType.CLASS_METHOD)
                self.class_method_param_types[f"{cwass.id.string()}.{method.id.string()}"] = [param.dtype for param in method.params]

    def check_program(self) -> None:
        assert self.program.mainuwu
        self.check_function(self.program.mainuwu, self.global_defs.copy())
        for func in self.program.functions: self.check_function(func, self.global_defs)
        # for cwass in self.program.classes: self.check_class(cwass, self.global_defs.copy())

    def check_function(self, func: Function, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        self.compile_params(func.params, local_defs)
        self.check_body(func.body, func.rtype, local_defs.copy())

    def check_class(self, cwass: Class, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        raise NotImplementedError

    def compile_params(self, params: list[Parameter], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        for param in params:
            local_defs[param.id.string()] = (param.dtype, GlobalType.IDENTIFIER)

    def check_body(self, body: BlockStatement, return_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        'make sure you pass in a copy of local_defs when calling this'
        for statement in body.statements:
            match statement:
                case Print():
                    self.check_print(statement, local_defs)
                case Input():
                    self.check_input(statement, local_defs)
                case Declaration() | ArrayDeclaration():
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

    def check_print(self, print: Print, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for val in print.values:
            self.evaluate_value(val, local_defs)

    def check_input(self, input: Input, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.evaluate_value(input.expr, local_defs)

    def check_if(self, if_stmt: IfStatement | ElseIfStatement, return_type: Token, local_defs: dict[str, tuple[Token, GlobalType]], else_if=False) -> None:
        self.evaluate_value(if_stmt.condition, local_defs)
        self.check_body(if_stmt.then, return_type, local_defs.copy())
        if else_if: return
        assert isinstance(if_stmt, IfStatement)
        for elif_stmt in if_stmt.else_if:
            self.check_if(elif_stmt, return_type, local_defs, else_if=True)
        if if_stmt.else_block:
            self.check_body(if_stmt.else_block, return_type, local_defs.copy())

    def check_while_loop(self, while_loop: WhileLoop, return_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.evaluate_value(while_loop.condition, local_defs)
        self.check_body(while_loop.body, return_type, local_defs.copy())

    def check_for_loop(self, for_loop: ForLoop, return_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        'pass in a copy of local defs when calling this'
        match for_loop.init:
            case Declaration() | ArrayDeclaration():
                self.check_declaration(for_loop.init, local_defs)
            case Assignment():
                self.check_assignment(for_loop.init, local_defs)
            case Token():
                self.evaluate_value(for_loop.init, local_defs)
            case IdentifierProds():
                self.evaluate_value(for_loop.init, local_defs)
        self.evaluate_value(for_loop.condition, local_defs)
        self.evaluate_value(for_loop.update, local_defs)
        self.check_body(for_loop.body, return_type, local_defs.copy())

    def check_return(self, ret: ReturnStatement, return_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        actual_type = self.evaluate_value(ret.expr, local_defs)
        if not self.is_similar_type(actual_type.flat_string(), return_type.flat_string()):
            print(f"ERROR: expected return type: {return_type}\n\tgot: {actual_type}")

    def check_declaration(self, decl: Declaration | ArrayDeclaration, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.check_value(decl.value, decl.dtype, local_defs)
        local_defs[decl.id.string()] = (decl.dtype, GlobalType.IDENTIFIER)

    def check_assignment(self, assign: Assignment, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        expected_type = local_defs[assign.id.string()][0]
        self.check_value(assign.value, expected_type, local_defs)

    def check_value(self, value: Value, expected_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match expected_type.token:
            case TokenType():
                actual_type = self.evaluate_value(value, local_defs)
                if not self.is_similar_type(actual_type.flat_string(), expected_type.flat_string()):
                    print(f"ERROR: expected type: {expected_type}\n\tgot: {actual_type}")
            case UniqueTokenType():
                match value:
                    case ClassConstructor():
                        self.check_class_constructor(value, local_defs)
                        for arg in value.args:
                            self.evaluate_value(arg, local_defs)
                    case _:
                        actual_type = self.evaluate_value(value, local_defs)
                        if actual_type.string() != expected_type.string():
                            print(f"ERROR: {expected_type} != {actual_type}")

    def evaluate_value(self, value: Value | Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
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
                if value.string() != None: raise ValueError(f"Unknown value: {value.string()}")
                return TokenType.SAN

    def evaluate_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        match expr:
            case PrefixExpression():
                right = self.evaluate_value(expr.right, local_defs)
                if not right in self.math_operands():
                    print(f"ERROR: {expr.right.flat_string()} ({right}) cannot be negative")
                return right
            case InfixExpression():
                left = self.evaluate_value(expr.left, local_defs)
                right = self.evaluate_value(expr.right, local_defs)

                if expr.op.token in self.math_operators():
                    if not (left in self.math_operands() and right in self.math_operands()):
                        tab_newline = '\n\t' # cuz \ is now allowed in f-strings
                        print(f"ERROR: {expr.left.string()} ({left}) {expr.op} {expr.right.string()} ({right}){tab_newline}"+
                            f"{f'{expr.left.flat_string()} ({left}) is not a math operand{tab_newline}' if left not in self.math_operands() else ''}"+
                            f"{f'{expr.right.flat_string()} ({right}) is not a math operand' if right not in self.math_operands() else ''}")
                    if left == TokenType.KUN or right == TokenType.KUN:
                        return TokenType.KUN
                    else:
                        return TokenType.CHAN
                elif expr.op.token in self.comparison_operators():
                    if not (left in self.math_operands() and right in self.math_operands()):
                        print(f"ERROR: {expr.left.flat_string()} ({left}) {expr.op} {expr.right.flat_string()} ({right})\n\t"+
                              f"{expr.left.flat_string() if left not in self.math_operands() else expr.right.flat_string()}"+
                              f"({left if left not in self.math_operands() else right}) is not a comparison operand")
                    return TokenType.SAMA
                elif expr.op.token in self.equality_operators():
                    return TokenType.SAMA
                else:
                    raise ValueError(f"Unknown operator: {expr.op}")
            case PostfixExpression():
                left = self.evaluate_value(expr.left, local_defs)
                if not(left in self.math_operands()):
                    print(f"ERROR: {expr.left.flat_string()} ({left}) cannot be incremented or decremented")
                return left
            case _:
                raise ValueError(f"Unknown expression: {expr}")

    def evaluate_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
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

    def check_and_evaluate_class_accessor(self, accessor: ClassAccessor, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        if not (res := local_defs.get(accessor.id.flat_string())):
            print(f"ERROR: '{accessor.id.flat_string()}' is not a class\n\t"
                  f"tried to use as class: {accessor.flat_string()}")
            return TokenType.SAN
        class_type, _ = res
        match accessor.accessed:
            case Token():
                accessed = accessor.accessed
                member_signature = f"{class_type}.{accessed.flat_string()}"
                if not (res := self.class_signatures.get(member_signature)):
                    print(f"ERROR: '{accessed.flat_string()}' is not a property of class '{class_type}'")
                    return TokenType.SAN
                return_type, member_type = res
                if member_type != GlobalType.CLASS_PROPERTY:
                    print(f"ERROR: {accessed.flat_string()} is not a property of class'{class_type}'\n\t"
                          f"{accessed.flat_string()} is a {member_type}")
                    return TokenType.SAN
                return return_type.token
            case FnCall():
                accessed = accessor.accessed.id
                member_signature = f"{class_type}.{accessed.flat_string()}"
                if not (res := self.class_signatures.get(member_signature)):
                    print(f"ERROR: '{accessed.flat_string()}' is not a method of class '{class_type}'")
                    return TokenType.SAN
                return_type, member_type = res
                if member_type != GlobalType.CLASS_METHOD:
                    print(f"ERROR: {accessed.flat_string()} is not a method of class '{class_type}'\n\t"
                          f"{accessed.flat_string()} is a {member_type}")
                    return TokenType.SAN
                return return_type.token
            case IndexedIdentifier():
                accessed = accessor.accessed.id
                match accessed:
                    case Token():
                        member_signature = f"{class_type}.{accessed.flat_string()}"
                        if not (res := self.class_signatures.get(member_signature)):
                            print(f"ERROR: '{accessed.flat_string()}' is not a property of class '{class_type}'")
                            return TokenType.SAN
                        return_type, member_type = res
                        if member_type != GlobalType.CLASS_PROPERTY:
                            print(f"ERROR: {accessed.flat_string()} is not a property of class'{class_type}'\n\t"
                                  f"{accessed.flat_string()} is a {member_type}")
                            return TokenType.SAN
                        if not return_type.is_arr_type():
                            print(f"ERROR: '{member_signature}' is not an array"
                                  f"\n\t'{member_signature}' is a {return_type}")
                            return TokenType.SAN
                        return return_type.token
                    case FnCall():
                        member_signature = f"{class_type}.{accessed.id.flat_string()}"
                        if not (res := self.class_signatures.get(member_signature)):
                            print(f"ERROR: '{accessed.flat_string()}' is not a method of class '{class_type}'")
                            return TokenType.SAN
                        return_type, member_type = res
                        if member_type != GlobalType.CLASS_METHOD:
                            print(f"ERROR: {accessed.flat_string()} is not a method of class '{class_type}'\n\t"
                                  f"{accessed.flat_string()} is a {member_type}")
                            return TokenType.SAN
                        if not return_type.is_arr_type():
                            print(f"ERROR: '{member_signature}()' does not return an array\n\t"
                                  f"'{member_signature}()' returns {return_type}")
                            return TokenType.SAN
                        return return_type.token
                    case _:
                        raise ValueError(f"Unknown class accessor: {accessor}")
            case ClassAccessor():
                return self.check_and_evaluate_class_accessor(accessor.accessed, local_defs)
            case _:
                raise ValueError(f"Unknown class accessor: {accessor}")

    def evaluate_iterable(self, collection: Iterable, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        match collection:
            case ArrayLiteral():
                flat_arr, units_type = self.expect_homogenous(collection, local_defs)
                for val in flat_arr:
                    self.evaluate_value(val, local_defs)
                return units_type.to_arr_type()
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

    def evaluate_fn_call(self, fn_call: FnCall, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        expected_types = self.function_param_types[fn_call.id.string()]
        if len(fn_call.args) != len(expected_types):
            print(f"ERROR: wrong number of args for fn {fn_call.id.string()}: expected {len(expected_types)}, got {len(fn_call.args)}")
        for arg, arg_type in zip(fn_call.args, expected_types):
            actual_type = self.evaluate_value(arg, local_defs)
            if not self.is_similar_type(actual_type.flat_string(), arg_type.flat_string()):
                print(f"ERROR: wrong param type for fn {fn_call.id.string()}\n\texpected: {arg_type.flat_string()}\n\tgot: {actual_type.flat_string()} -> {arg.flat_string()}")
        return local_defs[fn_call.id.string()][0].token

    def check_class_constructor(self, class_constructor: ClassConstructor, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        expected_types = self.class_param_types[class_constructor.id.string()]
        if len(expected_types) != len(class_constructor.args):
            print(f"ERROR: wrong number of args for class {class_constructor.id.string()}: expected {len(expected_types)}, got {len(class_constructor.args)}")
        for arg, arg_type in zip(class_constructor.args, expected_types):
            actual_type = self.evaluate_value(arg, local_defs)
            if not self.is_similar_type(actual_type.flat_string(), arg_type.flat_string()):
                print(f"ERROR: wrong param type for class {class_constructor.id.string()}\n\texpected: {arg_type.flat_string()}\n\tgot: {actual_type.flat_string()} -> {arg.flat_string()}")

    def evaluate_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        match token.token:
            case TokenType.STRING_LITERAL: return TokenType.SENPAI
            case TokenType.INT_LITERAL: return TokenType.CHAN
            case TokenType.FLOAT_LITERAL: return TokenType.KUN
            case TokenType.FAX | TokenType.CAP: return TokenType.SAMA
            case TokenType.NUWW: return TokenType.SAN
            case UniqueTokenType(): return local_defs[token.string()][0].token
            case _: raise ValueError(f"Unknown token: {token}")

    ## HELPER METHODS FOR OPERATORS AND OPERANDS
    def math_operands(self) -> list[TokenType]:
        return [TokenType.CHAN, TokenType.KUN, TokenType.SAMA, TokenType.SAN]
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
    def expect_homogenous(self, arr: ArrayLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> tuple[list[Value], TokenType]:
        flat_arr = self.flatten_array(arr.elements)
        types: set[TokenType] = set()
        for val in flat_arr:
            match val:
                case Token():
                    types.add(self.evaluate_token(val, local_defs))
                case Expression():
                    types.add(self.evaluate_expression(val, local_defs))
                case IdentifierProds():
                    types.add(self.evaluate_ident_prods(val, local_defs))
                case Iterable():
                    types.add(self.evaluate_iterable(val, local_defs))
                case _:
                    raise ValueError(f"Unknown array value type: {val.flat_string()}")
        if len(types) > 1:
            print(f"ERROR: expected homogenous types: {arr.flat_string()}\n\tgot {[t.token for t in types]}")
            return [], TokenType.SAN
        return flat_arr, types.pop()

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

    def is_similar_type(self, actual_type: str, expected_type: str) -> bool:
        'determines if two types are similar'
        if (actual_type == expected_type 
            # nuww is an ok val for any type
            or actual_type == "san"
            ): return True

        assert actual_type != expected_type
        match expected_type:
            # num types are convertible between each other
            case "chan" | "kun":
                match actual_type:
                    case "chan" | "kun" | "sama": return True
                    case _: return False
            # all types are convertible to bool
            case "sama": return True
            # every other type needs exact match
            case _: return False