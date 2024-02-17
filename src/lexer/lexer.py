from constants.constants import DELIMS, ATOMS
from .token import Token, TokenType, UniqueTokenType
from .error_handler import Error, DelimError, GenericError, ErrorSrc

from .lexer_components.move_cursor import advance_cursor
from .lexer_components import peek

class Lexer():
    'description'

    def __init__(self, source_code: list[str]):
        self._lines = source_code
        ErrorSrc.src = source_code
        UniqueTokenType.clear()

        self._position = [0,0]
        self._current_char = self._lines[self._position[0]][self._position[1]]

        self._nest_level = 0

        self._tokens: list[Token] = []
        self._logs: list[GenericError | DelimError] = []

        self._get_tokens()

    @property
    def tokens(self) -> list[Token]:
        return self._tokens

    @property
    def errors(self):
        return self._logs
    
    @property
    def context(self):
        'to be passed to outside modules'
        return self._lines, self._position, self._current_char, self._tokens, self._logs

    def _get_tokens(self):
        is_end_of_file = False
        cursor_advanced = False
        valid_starting_chars = {*ATOMS['alphanum'], *ATOMS['general_operator'],
                                '|', '!', '&', '{', '}', '[', ']', '(', ')', ',', '.', '~', '"'}
        
        while not is_end_of_file:
            if self._current_char in ['\n', ' ', '\t']:
                self._tokens.append(Token(self._current_char, TokenType.WHITESPACE, tuple(self._position), tuple(self._position)))
                is_end_of_file, self._current_char = advance_cursor(self.context)
                if is_end_of_file:
                    break
                continue

            if self._current_char not in valid_starting_chars:
                self._logs.append(GenericError(Error.UNEXPECTED_SYMBOL, tuple(self._position)))
                is_end_of_file, self._current_char = advance_cursor(self.context)
                if is_end_of_file:
                    break
                continue

            if self._current_char == 'b':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('bweak', TokenType.BWEAK, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == 'c':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('chan', TokenType.CHAN, self.context)
                if cursor_advanced:
                    continue
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('cap', TokenType.CAP, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('cwass', TokenType.CWASS, self.context)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'd':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('dono', TokenType.DONO, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('do whiwe', TokenType.DO_WHIWE, self.context)
                if cursor_advanced:
                    continue
                
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('donee~', TokenType.DONE, self.context)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'e':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('ewse iwf', TokenType.EWSE_IWF, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('ewse', TokenType.EWSE, self.context)
                if cursor_advanced:
                    continue
                
            if self._current_char == 'f':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved("fwunc", TokenType.FWUNC, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('fax', TokenType.FAX, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('fow', TokenType.FOW, self.context)
                if cursor_advanced:
                    continue
        
            if self._current_char == 'g':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('gwobaw', TokenType.GWOBAW, self.context)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'i':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('iwf', TokenType.IWF, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('inpwt', TokenType.INPWT, self.context)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'k':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('kun', TokenType.KUN, self.context)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'm':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('mainuwu', TokenType.MAINUWU, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == 'n':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('nuww', TokenType.NUWW, self.context)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'p':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('pwint', TokenType.PWINT, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == 's':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('san', TokenType.SAN, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('sama', TokenType.SAMA, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('senpai', TokenType.SENPAI, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('staart!', TokenType.START, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == 'w':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('whiwe', TokenType.WHIWE, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('wetuwn', TokenType.WETUWN, self.context)
                if cursor_advanced:
                    continue
            
            # Literals check
            # can be identifiers or function names
            if self._current_char in ATOMS['alpha_small']:
                is_end_of_file, self._current_char = peek.identifier(self.context)
                if is_end_of_file:
                    break
                continue

            # class names
            if self._current_char in ATOMS['alpha_big']:
                is_end_of_file, self._current_char  = peek.identifier(self.context, cwass=True)
                if is_end_of_file:
                    break
                continue
            
            if self._current_char in ATOMS['number']:
                is_end_of_file, self._current_char = peek.int_float(self.context)
                if is_end_of_file:
                    break
                continue
            
            # string literals
            if self._current_char in ['|', '"']:
                is_end_of_file, self._current_char = peek.string(self.context)
                if is_end_of_file:
                    break
                continue

            # Symbol Checks
            if self._current_char == '=':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('==', TokenType.EQUALITY_OPERATOR, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('=', TokenType.ASSIGNMENT_OPERATOR, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == '+':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('++', TokenType.INCREMENT_OPERATOR, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('+', TokenType.ADDITION_SIGN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == '-':
                line, column = tuple(self._position)
                after_slice = self._lines[line][column+1:]
                before_slice = self._lines[line][:column]

                if len(after_slice) < 1:
                    line, col = self._position
                    self._logs.append(DelimError(TokenType.DASH, (line, col + 1), '-', '\n'))
                    is_end_of_file, self._current_char = advance_cursor(self.context)
                    continue

                # Check if - is negative
                valid_ops = [TokenType.ASSIGNMENT_OPERATOR, 
                             TokenType.ADDITION_SIGN, TokenType.DASH, TokenType.MULTIPLICATION_SIGN, TokenType.DIVISION_SIGN, TokenType.MODULO_SIGN,
                             TokenType.GREATER_THAN_SIGN, TokenType.LESS_THAN_SIGN ,TokenType.GREATER_THAN_OR_EQUAL_SIGN ,TokenType.LESS_THAN_OR_EQUAL_SIGN,
                             TokenType.EQUALITY_OPERATOR, TokenType.INEQUALITY_OPERATOR, 
                             TokenType.AND_OPERATOR, TokenType.OR_OPERATOR,]
                operator_before = self._check_prev_token(valid_ops)
                line_copy = self._lines[line]
                if line_copy.lstrip()[0] == '-' or operator_before:
                    if after_slice[0] in ATOMS["number"]:
                        is_end_of_file, self._current_char = advance_cursor(self.context)
                        is_end_of_file, self._current_char = peek.int_float(self.context, negative=True)
                        if is_end_of_file:
                            break
                        continue

                # Differentiate between arithmetic and unary
                if len(after_slice) > 0:
                    # If next char is a dash, check if it is delimited by unary expected delims
                    if self._lines[line][column+1] == '-':
                        if len(after_slice) > 1:
                            if self._lines[line][column+2] in DELIMS['unary']:
                                starting_position = tuple(self._position)
                                ending_position = tuple([self._position[0], self._position[1]+1])
                                self._tokens.append(Token('--', TokenType.DECREMENT_OPERATOR, starting_position, ending_position))
                                is_end_of_file, self._current_char = advance_cursor(self.context, 2)
                                continue
                    starting_position = ending_position = tuple(self._position)
                    self._tokens.append(Token('-', TokenType.DASH, starting_position, ending_position))
                    is_end_of_file, self._current_char = advance_cursor(self.context)
                    continue

            if self._current_char == '!':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('!=', TokenType.INEQUALITY_OPERATOR, self.context)
                if cursor_advanced:
                    continue

                self._logs.append(GenericError(Error.UNEXPECTED_SYMBOL, tuple(self._position),
                                               context=f"Symbol {self._current_char} is invalid. Did you mean '!='?"))
                is_end_of_file, self._current_char = advance_cursor(self.context)
                continue

            if self._current_char == '>':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('>=', TokenType.GREATER_THAN_OR_EQUAL_SIGN, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.comments(self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.comments(self.context, multiline=True)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('>', TokenType.GREATER_THAN_SIGN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == '<':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('<=', TokenType.LESS_THAN_OR_EQUAL_SIGN, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('<', TokenType.LESS_THAN_SIGN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == '*':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('*', TokenType.MULTIPLICATION_SIGN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == '/':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('/', TokenType.DIVISION_SIGN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == '%':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('%', TokenType.MODULO_SIGN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == "|":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('||', TokenType.OR_OPERATOR, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == "&":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('&&', TokenType.AND_OPERATOR, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('&', TokenType.CONCATENATION_OPERATOR, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == "{":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('{', TokenType.OPEN_BRACE, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == "}":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('}', TokenType.CLOSE_BRACE, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == "(":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('(', TokenType.OPEN_PAREN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == ")":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved(')', TokenType.CLOSE_PAREN, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == "[":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('[[', TokenType.DOUBLE_OPEN_BRACKET, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('[', TokenType.OPEN_BRACKET, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == "]":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved(']]', TokenType.DOUBLE_CLOSE_BRACKET, self.context)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file, self._current_char = peek.reserved(']', TokenType.CLOSE_BRACKET, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == ",":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved(',', TokenType.COMMA, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == ".":
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('.', TokenType.DOT_OP, self.context)
                if cursor_advanced:
                    continue

            if self._current_char == '~':
                cursor_advanced, is_end_of_file, self._current_char = peek.reserved('~', TokenType.TERMINATOR, self.context)
                if cursor_advanced:
                    continue

    def _check_prev_token(self, to_check: TokenType | list[TokenType], prev_count: int = 1, in_order=False):
        """
        Checks prev token if it has the token type/s passed. Must be on the same line

        can check for token a specific token behind from the current character
            eg. `fwunc aqua-chan`, `fwunc` is 3 tokens behind from c in chan

        can check for multiple token types if any is directly behind (default) or if all are behind in order
            eg. `fwunc aqua-chan`, `-`, `aqua`, and `fwunc` are 1, 2, 3 tokens behind from c in chan respectivly
        """

        # Convert input to list
        if isinstance(to_check, TokenType):
            to_check = [to_check]
        if in_order and prev_count > 1:
            raise ValueError("You are checking for tokens in order. Please keep the prev_count as default '1'")

        present_flag = False
        if in_order:
            start = 1
            prev_count = len(to_check)+1
        else:
            start = prev_count
            prev_count += 1

        to_check_index = 0
        for i in range(start, prev_count):
            if len(self.tokens) >= i:
                prev_token = self.tokens[-i]
                in_same_line = prev_token.position[0] == self._position[0]
                if in_same_line:
                    if to_check[to_check_index] == TokenType.GEN_CWASS_NAME and prev_token.token.token.startswith('CWASS'):
                        present_flag = True
                    elif to_check[to_check_index] == TokenType.GEN_IDENTIFIER and prev_token.token.token.startswith('IDENTIFIER'):
                        present_flag = True
                    else:
                        if prev_token.token in to_check and prev_token.position[0] == self._position[0]:
                            present_flag = True
                        else:
                            present_flag = False
                            break
            to_check_index += 1

        return present_flag

    def print_error_logs(self):
        for error in self.errors:
            print(error)

def print_lex(source_code: list[str]) -> Lexer:
    print('\nsample text file')
    print("_"*20)
    for i, line in enumerate(source_code):
        print(f"{i+1} | {line}")
    print("_"*20)
    print('end of file\n')
    x = Lexer(source_code)
    x.print_error_logs()
    print("\n\n","#"*64)
    print(f"{'lexeme':^20}{'token':^20}{'range':^20}")
    print("","_"*63)
    border = "|"
    for token in x.tokens:
        print(border, end='')
        print(f"{token.lexeme:^18}", end=border)
        print(f"{token.token:^20}", end=border)
        print(f"{f'{token.position} - {token.end_position}':^23}", end=border)
        print()
    print("","_"*63)
    return x
