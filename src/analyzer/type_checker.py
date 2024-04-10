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
        self.compile_global_types()
        self.check_program()

    def compile_global_types(self):
        '''
        populates the self.global_types dict with the unique global names
        any duplicates will be appended to error
        '''
        for global_dec in self.program.globals:
            self.global_defs[global_dec.id.string()] = (global_dec.id, GlobalType.IDENTIFIER)
        for func in self.program.functions:
            self.global_defs[func.id.string()] = (func.id, GlobalType.FUNCTION)
            self.function_param_types[func.id.string()] = [param.dtype for param in func.params]
        for cwass in self.program.classes:
            self.global_defs[cwass.id.string()] = (cwass.id, GlobalType.CLASS)
            for param in cwass.params:
                self.class_signatures[f"{cwass.id.string()}.{param.id.string()}"] = (param.id, GlobalType.CLASS_PROPERTY)
            for prop in cwass.properties:
                self.global_defs[f"{cwass.id.string()}.{prop.id.string()}"] = (prop.id, GlobalType.CLASS_PROPERTY)
            for method in cwass.methods:
                self.global_defs[f"{cwass.id.string()}.{method.id.string()}"] = (method.id, GlobalType.CLASS_METHOD)
                self.class_method_param_types[f"{cwass.id.string()}.{method.id.string()}"] = [param.dtype for param in method.params]

    def check_program(self) -> None:
        assert self.program.mainuwu
        self.check_function(self.program.mainuwu, self.global_defs)
        for func in self.program.functions: self.check_function(func, self.global_defs)
        # for cwass in self.program.classes: self.check_class(cwass)

    def check_function(self, func: Function, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.check_body(func.body, func.rtype, local_defs.copy())

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
                    self.check_if(statement, return_type, local_defs.copy())
                case WhileLoop():
                    self.check_while_loop(statement, return_type, local_defs.copy())
                case ForLoop():
                    self.check_for_loop(statement, return_type, local_defs.copy())
                case ReturnStatement():
                    self.check_return(statement, return_type, local_defs.copy())
                case FnCall():
                    self.check_fn_call(statement, local_defs)
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

    def check_fn_call(self, fn_call: FnCall, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        for arg in fn_call.args:
            self.evaluate_value(arg, local_defs)

    def check_for_loop(self, for_loop: ForLoop, return_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match for_loop.init:
            case Declaration() | ArrayDeclaration():
                self.check_declaration(for_loop.init, local_defs)
            case Assignment():
                self.check_assignment(for_loop.init, local_defs)
            case Token():
                self.evaluate_value(for_loop.init, local_defs)
            case IdentifierProds():
                raise NotImplementedError
        self.evaluate_value(for_loop.condition, local_defs)
        self.evaluate_value(for_loop.update, local_defs)
        self.check_body(for_loop.body, return_type, local_defs.copy())

    def check_return(self, ret: ReturnStatement, return_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        actual_type = self.evaluate_value(ret.expr, local_defs)
        if actual_type != return_type.token:
            print(f"ERROR: {return_type} != {actual_type}")

    def check_declaration(self, decl: Declaration | ArrayDeclaration, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        self.check_value(decl.value, decl.dtype, local_defs)
        local_defs[decl.id.string()] = (decl.dtype, GlobalType.IDENTIFIER)

    def check_assignment(self, assign: Assignment, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        expected_type = local_defs[assign.id.string()][0]
        self.check_value(assign.value, expected_type, local_defs)

    def check_value(self, value: Value, expected_type: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
        match expected_type.token:
            case TokenType.CHAN | TokenType.KUN | TokenType.SAMA:
                expected_types = [TokenType.CHAN, TokenType.KUN, TokenType.SAMA, TokenType.NUWW]
                actual_type = self.evaluate_value(value, local_defs)
                if actual_type not in expected_types:
                    print(f"ERROR: {expected_type} != {actual_type}")
            case TokenType.SENPAI:
                expected_types = [TokenType.SENPAI, TokenType.NUWW]
                actual_type = self.evaluate_value(value, local_defs)
                if actual_type not in expected_types:
                    print(f"ERROR: {expected_type} != {actual_type}")
            case TokenType.CHAN_ARR:
                expected_types = [TokenType.CHAN_ARR, TokenType.NUWW]
                actual_type = self.evaluate_value(value, local_defs)
                if actual_type not in expected_types:
                    print(f"ERROR: {expected_type} != {actual_type}")
            case UniqueTokenType():
                match value:
                    case ClassConstructor():
                        if value.id.string() != expected_type.string():
                            print(f"ERROR: {expected_type} != {value.id.string()}")
                        for arg in value.args:
                            self.evaluate_value(arg, local_defs)
                    case _:
                        print(f"ERROR: {expected_type} != {self.evaluate_value(value, local_defs)}")

    def evaluate_value(self, value: Value | Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        match value:
            case Token():
                return self.evaluate_token(value, local_defs)
            case Expression():
                return self.evaluate_expression(value, local_defs)
            case IdentifierProds():
                raise NotImplementedError
            case Iterable():
                raise NotImplementedError
            case _:
                if value.string() != None: raise ValueError(f"Unknown value: {value.string()}")
                return TokenType.NUWW

    def evaluate_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        match expr:
            case PrefixExpression():
                right = self.evaluate_value(expr.right, local_defs)
                if not right in self.math_operands():
                    print(f"ERROR: {right} cannot be negative")
                return right
            case InfixExpression():
                left = self.evaluate_value(expr.left, local_defs)
                right = self.evaluate_value(expr.right, local_defs)

                if expr.op.token in self.math_operators():
                    if not (left in self.math_operands() and right in self.math_operands()):
                        tab_newline = '\n\t' # cuz \ is now allowed in f-strings
                        print(f"ERROR: {left} {expr.op} {right}{tab_newline}"+
                            f"{f'{left} is not a math operand{tab_newline}' if left not in self.math_operands() else ''}"+
                            f"{f'{right} is not a math operand' if right not in self.math_operands() else ''}")
                    if left == TokenType.KUN or right == TokenType.KUN:
                        return TokenType.KUN
                    else:
                        return TokenType.CHAN
                elif expr.op.token in self.comparison_operators():
                    if not (left in self.math_operands() and right in self.math_operands()):
                        print(f"ERROR: {left} {expr.op} {right}\n\t"+
                              f"{left if left not in self.math_operands() else right} is not a comparison operand")
                    return TokenType.SAMA
                elif expr.op.token in self.equality_operators():
                    return TokenType.SAMA
                else:
                    raise ValueError(f"Unknown operator: {expr.op}")
            case PostfixExpression():
                left = self.evaluate_value(expr.left, local_defs)
                if not(left in self.math_operands()):
                    print(f"ERROR: {left} cannot be incremented or decremented")
                return left
            case _:
                raise ValueError(f"Unknown expression: {expr}")

    def evaluate_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> TokenType:
        match token.token:
            case TokenType.STRING_LITERAL: return TokenType.SENPAI
            case TokenType.INT_LITERAL: return TokenType.CHAN
            case TokenType.FLOAT_LITERAL: return TokenType.KUN
            case TokenType.FAX | TokenType.CAP: return TokenType.SAMA
            case TokenType.NUWW: return TokenType.SAN
            case UniqueTokenType(): return local_defs[token.string()][0].token
            case _: raise ValueError(f"Unknown token: {token}")

    def math_operands(self) -> list[TokenType]:
        return [TokenType.CHAN, TokenType.KUN, TokenType.SAMA, TokenType.NUWW]
    def math_operators(self) -> list[TokenType]:
        return [TokenType.ADDITION_SIGN, TokenType.DASH, TokenType.MULTIPLICATION_SIGN,
                TokenType.DIVISION_SIGN, TokenType.MODULO_SIGN]
    def comparison_operators(self) -> list[TokenType]:
        return [TokenType.LESS_THAN_SIGN, TokenType.GREATER_THAN_SIGN,
                TokenType.LESS_THAN_OR_EQUAL_SIGN, TokenType.GREATER_THAN_OR_EQUAL_SIGN]
    def equality_operators(self) -> list[TokenType]:
        return [TokenType.EQUALITY_OPERATOR, TokenType.INEQUALITY_OPERATOR,
                TokenType.AND_OPERATOR, TokenType.OR_OPERATOR]

    ### REFERENCE FROM ANALYZER
    # def analyze_class(self, cwass: Class) -> None:
    #     local_defs: dict[str, tuple[Token, GlobalType]] = self.global_names.copy()
    #     for p in cwass.params:
    #         self.analyze_param(p, local_defs)
    #     for prop in cwass.properties:
    #         self.analyze_declaration(prop, local_defs)
    #     for method in cwass.methods:
    #         self.analyze_function(method)
    #
    # def analyze_param(self, param: Parameter, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     assert isinstance(param.id, Token)
    #     if param.id.string() in local_defs:
    #         self.errors.append(DuplicateDefinitionError(
    #             *local_defs[param.id.string()],
    #             param.id,
    #             GlobalType.IDENTIFIER,
    #         ))
    #     else:
    #         local_defs[param.id.string()] = (param.id, GlobalType.IDENTIFIER)
    #
    # def analyze_args(self, args: list[Value], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     for arg in args:
    #         self.analyze_value(arg, local_defs)
    #
    # def analyze_body(self, body: BlockStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     when you're calling analyze_body(), make sure to pass in a copy of local_defs
    #     '''
    #     for stmt in body.statements:
    #         match stmt:
    #             case Print():
    #                 self.analyze_print(stmt, local_defs)
    #             case Input():
    #                 self.analyze_input(stmt, local_defs)
    #             case Declaration() | ArrayDeclaration():
    #                 self.analyze_declaration(stmt, local_defs)
    #             case Assignment():
    #                 self.analyze_assignment(stmt, local_defs)
    #             case IfStatement():
    #                 self.analyze_if(stmt, local_defs)
    #             case WhileLoop():
    #                 self.analyze_while_loop(stmt, local_defs)
    #             case ForLoop():
    #                 self.analyze_for_loop(stmt, local_defs.copy())
    #             case ReturnStatement():
    #                 self.analyze_return(stmt, local_defs)
    #             case FnCall():
    #                 self.analyze_ident_prods(stmt, local_defs)
    #             case _:
    #                 raise ValueError(f"Unknown statement: {stmt}")
    #
    # ## IN BODY ANALYZERS
    # def analyze_print(self, print_stmt: Print, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     for val in print_stmt.values:
    #         self.analyze_value(val, local_defs)
    #
    # def analyze_input(self, input_stmt: Input, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     self.analyze_value(input_stmt.expr, local_defs)
    #
    # def analyze_if(self, if_stmt: IfStatement | ElseIfStatement, local_defs: dict[str, tuple[Token, GlobalType]], else_if: bool = False) -> None:
    #     self.analyze_value(if_stmt.condition, local_defs)
    #     self.analyze_body(if_stmt.then, local_defs.copy())
    #     if else_if: return
    #     assert isinstance(if_stmt, IfStatement)
    #     for elif_stmt in if_stmt.else_if:
    #         self.analyze_if(elif_stmt, local_defs, else_if=True)
    #     if if_stmt.else_block:
    #         self.analyze_body(if_stmt.else_block, local_defs.copy())
    #
    # def analyze_declaration(self, decl: Declaration | ArrayDeclaration, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     self.expect_unique_token(decl.id, local_defs)
    #     self.analyze_value(decl.value, local_defs)
    #
    # def analyze_assignment(self, assign: Assignment, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     match assign.id:
    #         case Token():
    #             self.expect_defined_token(assign.id, local_defs)
    #         case IdentifierProds():
    #             self.analyze_ident_prods(assign.id, local_defs)
    #         case _:
    #             raise ValueError(f"Unknown assignment left hand side: {assign.id}")
    #     self.analyze_value(assign.value, local_defs)
    #
    # def analyze_while_loop(self, while_loop: WhileLoop, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     self.analyze_value(while_loop.condition, local_defs)
    #     self.analyze_body(while_loop.body, local_defs.copy())
    #
    # def analyze_for_loop(self, for_loop: ForLoop, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     when calling analyze_for_loop(), make sure to pass in a copy of local_defs
    #     '''
    #     match for_loop.init:
    #         case Assignment():
    #             self.analyze_assignment(for_loop.init, local_defs)
    #         case Declaration() | ArrayDeclaration():
    #             self.analyze_declaration(for_loop.init, local_defs)
    #         case Token():
    #             self.expect_defined_token(for_loop.init, local_defs)
    #         case IdentifierProds():
    #             self.analyze_ident_prods(for_loop.init, local_defs)
    #         case _:
    #             raise ValueError(f"Unknown for loop init: {for_loop.init}")
    #     self.analyze_value(for_loop.condition, local_defs)
    #     self.analyze_value(for_loop.update, local_defs)
    #     self.analyze_body(for_loop.body, local_defs.copy())
    #
    # def analyze_return(self, ret: ReturnStatement, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     self.analyze_value(ret.expr, local_defs)
    #
    # ## OTHER ANALYZERS
    # def analyze_value(self, value: Value | Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     match value:
    #         case Token():
    #             self.expect_defined_token(value, local_defs)
    #         case Expression():
    #             self.analyze_expression(value, local_defs)
    #         case IdentifierProds():
    #             self.analyze_ident_prods(value, local_defs)
    #         case Iterable():
    #             self.analyze_iterable(value, local_defs)
    #         case _:
    #             raise ValueError(f"Unknown value: {value}")
    # def analyze_ident_prods(self, ident_prod: IdentifierProds, local_defs: dict[str, tuple[Token, GlobalType]],
    #                         access_depth: int = 1) -> None:
    #     match ident_prod:
    #         case IndexedIdentifier():
    #             match ident_prod.id:
    #                 case Token():
    #                     self.expect_defined_token(ident_prod.id, local_defs)
    #                 case FnCall():
    #                     self.analyze_fn_call(ident_prod.id, local_defs)
    #             self.analyze_array_indices(ident_prod.index, local_defs)
    #         case FnCall():
    #             self.analyze_fn_call(ident_prod, local_defs)
    #         case ClassConstructor():
    #             self.analyze_args(ident_prod.args, local_defs)
    #         case ClassAccessor():
    #             if access_depth > 0:
    #                 match ident_prod.id:
    #                     case Token():
    #                         self.expect_defined_token(ident_prod.id, local_defs)
    #                     case FnCall():
    #                         self.analyze_fn_call(ident_prod.id, local_defs)
    #             match ident_prod.accessed:
    #                 case FnCall():
    #                     self.analyze_fn_call(ident_prod.accessed, local_defs)
    #                 case IndexedIdentifier():
    #                     self.analyze_array_indices(ident_prod.accessed.index, local_defs)
    #                 case ClassAccessor():
    #                     self.analyze_ident_prods(ident_prod.accessed, local_defs, access_depth=access_depth+1)
    #         case _:
    #             raise ValueError(f"Unknown identifier production: {ident_prod}")
    #
    # def analyze_fn_call(self, fn_call: FnCall, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     if fn_call.id.string() in local_defs and local_defs[fn_call.id.string()][1] == GlobalType.FUNCTION:
    #         pass
    #     else:
    #         self.errors.append(UndefinedError(
    #             fn_call.id,
    #             GlobalType.FUNCTION,
    #         ))
    #     self.analyze_args(fn_call.args, local_defs)
    #
    # def analyze_iterable(self, collection: Iterable, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     this is for array literals, string fmt, and string literals
    #     try not to use analyze_array_literal, analyze_string_fmt, or analyze_string_literal directly.
    #     use this method instead.
    #     '''
    #     match collection:
    #         case ArrayLiteral():
    #             self.analyze_array_literal(collection, local_defs)
    #         case StringFmt():
    #             self.analyze_string_fmt(collection, local_defs)
    #         case Input():
    #             self.analyze_input(collection, local_defs)
    #         case StringLiteral():
    #             self.analyze_string_literal(collection, local_defs)
    #         case _:
    #             raise ValueError(f"Unknown collection: {collection}")
    #
    # def analyze_string_literal(self, str_lit: StringLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     try not to use this method directly.
    #     use analyze_iterable instead
    #     '''
    #     for concat in str_lit.concats:
    #         match concat:
    #             case StringFmt():
    #                 self.analyze_string_fmt(concat, local_defs)
    #             case Input():
    #                 self.analyze_input(concat, local_defs)
    #             case StringLiteral():
    #                 self.analyze_string_literal(concat, local_defs)
    #
    # def analyze_array_literal(self, array_literal: ArrayLiteral, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     try not to use this method directly.
    #     use analyze_iterable instead
    #     '''
    #     for elem in array_literal.elements:
    #         self.analyze_value(elem, local_defs)
    # 
    # def analyze_array_indices(self, index_list: list[Value], local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     for idx in index_list:
    #         self.analyze_value(idx, local_defs)
    # 
    # def analyze_expression(self, expr: Expression, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     match expr:
    #         case PrefixExpression():
    #             self.analyze_value(expr.right, local_defs)
    #         case PostfixExpression():
    #             self.analyze_value(expr.left, local_defs)
    #         case InfixExpression():
    #             self.analyze_value(expr.left, local_defs)
    #             self.analyze_value(expr.right, local_defs)
    #         case _:
    #             raise ValueError(f"Unknown expression: {expr}")
    #
    # def analyze_string_fmt(self, string_fmt: StringFmt, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     try not to use this method directly.
    #     use analyze_iterable instead
    #     '''
    #     for expr in string_fmt.exprs:
    #         self.analyze_value(expr, local_defs)
    #
    #     for concat in string_fmt.concats:
    #         match concat:
    #             case StringFmt() | Input() | StringLiteral():
    #                 self.analyze_iterable(concat, local_defs)
    #             case _:
    #                 raise ValueError(f"Unknown concat: {concat}")
    #
    #
    # ## HELPER METHODS
    # def expect_defined_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     checks whether the token is defined in the scope
    #     if not, appends to errors
    #     '''
    #     match token.token:
    #         case TokenType.STRING_LITERAL | TokenType.INT_LITERAL | TokenType.FLOAT_LITERAL | TokenType.FAX | TokenType.CAP | TokenType.NUWW:
    #             pass
    #         case UniqueTokenType():
    #             if token.string() in local_defs:
    #                 pass
    #             else:
    #                 self.errors.append(UndefinedError(
    #                     token,
    #                     GlobalType.IDENTIFIER,
    #                 ))
    #         case _:
    #             raise ValueError(f"Unknown token: {token}")
    # def expect_unique_token(self, token: Token, local_defs: dict[str, tuple[Token, GlobalType]]) -> None:
    #     '''
    #     checks whether the token is not yet defined in the scope
    #     if already defined (duplicate), appends to errors
    #     '''
    #     match token.token:
    #         case UniqueTokenType():
    #             if token.string() in local_defs and local_defs[token.string()][1] == GlobalType.IDENTIFIER:
    #                 self.errors.append(DuplicateDefinitionError(
    #                     *local_defs[token.string()],
    #                     token,
    #                     GlobalType.IDENTIFIER,
    #                 ))
    #             else:
    #                 local_defs[token.string()] = (token, GlobalType.IDENTIFIER)
    #         case _:
    #             raise ValueError(f"Unknown token: {token}")
