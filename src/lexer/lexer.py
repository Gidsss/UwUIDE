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
        self._at_EOF = False
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

    def advance(self, increment: int = 1):
       self._at_EOF, self._current_char = advance_cursor(self.context, increment = increment)

    # methods that interact with outside modules
    @property
    def context(self):
        'to be passed to outside modules'
        return self._lines, self._position, self._current_char, self._tokens, self._logs
    def peek_reserved(self, reserved: str, token_type: TokenType) -> bool:
        cursor_advanced, self._at_EOF, self._current_char = peek.reserved(reserved, token_type, self.context)
        return cursor_advanced
    def peek_comments(self, multiline: bool = False) -> bool:
        cursor_advanced, self._at_EOF, self._current_char = peek.comments(self.context, multiline=multiline)
        return cursor_advanced
    def peek_ident(self, cwass: bool = False) -> bool:
        self._at_EOF, self._current_char  = peek.identifier(self.context, cwass=cwass)
    def peek_int_float(self, negative: bool = False, start_pos: tuple[int, int] = None):
        self._at_EOF, self._current_char = peek.int_float(self.context, negative=negative, start_pos=start_pos)
    def peek_string(self):
        self._at_EOF, self._current_char = peek.string(self.context)

    def _get_tokens(self):
        cursor_advanced = False
        valid_starting_chars = {*ATOMS['alphanum'], *ATOMS['general_operator'],
                                '|', '!', '&', '{', '}', '[', ']', '(', ')', ',', '.', '~', '"'}
        
        while not self._at_EOF:
            if self._current_char in ['\n', ' ', '\t']:
                self._tokens.append(Token(self._current_char, TokenType.WHITESPACE, tuple(self._position), tuple(self._position)))
                self.advance()
                if self._at_EOF:
                    break
                continue

            if self._current_char not in valid_starting_chars:
                self._logs.append(GenericError(Error.UNEXPECTED_SYMBOL, tuple(self._position)))
                self.advance()
                if self._at_EOF:
                    break
                continue

            if self._current_char == 'b':
                cursor_advanced = self.peek_reserved('bweak', TokenType.BWEAK)
                if cursor_advanced:
                    continue

            if self._current_char == 'c':
                cursor_advanced = self.peek_reserved('chan', TokenType.CHAN)
                if cursor_advanced:
                    continue
                cursor_advanced = self.peek_reserved('cap', TokenType.CAP)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('cwass', TokenType.CWASS)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'd':
                cursor_advanced = self.peek_reserved('dono', TokenType.DONO)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('do whiwe', TokenType.DO_WHIWE)
                if cursor_advanced:
                    continue
                
                cursor_advanced = self.peek_reserved('donee~', TokenType.DONE)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'e':
                cursor_advanced = self.peek_reserved('ewse iwf', TokenType.EWSE_IWF)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('ewse', TokenType.EWSE)
                if cursor_advanced:
                    continue
                
            if self._current_char == 'f':
                cursor_advanced = self.peek_reserved("fwunc", TokenType.FWUNC)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('fax', TokenType.FAX)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('fow', TokenType.FOW)
                if cursor_advanced:
                    continue
        
            if self._current_char == 'g':
                cursor_advanced = self.peek_reserved('gwobaw', TokenType.GWOBAW)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'i':
                cursor_advanced = self.peek_reserved('iwf', TokenType.IWF)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('inpwt', TokenType.INPWT)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'k':
                cursor_advanced = self.peek_reserved('kun', TokenType.KUN)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'm':
                cursor_advanced = self.peek_reserved('mainuwu', TokenType.MAINUWU)
                if cursor_advanced:
                    continue

            if self._current_char == 'n':
                cursor_advanced = self.peek_reserved('nuww', TokenType.NUWW)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'p':
                cursor_advanced = self.peek_reserved('pwint', TokenType.PWINT)
                if cursor_advanced:
                    continue

            if self._current_char == 's':
                cursor_advanced = self.peek_reserved('san', TokenType.SAN)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('sama', TokenType.SAMA)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('senpai', TokenType.SENPAI)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('staart!', TokenType.START)
                if cursor_advanced:
                    continue

            if self._current_char == 'w':
                cursor_advanced = self.peek_reserved('whiwe', TokenType.WHIWE)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('wetuwn', TokenType.WETUWN)
                if cursor_advanced:
                    continue
            
            # Literals check
            # can be identifiers or function names
            if self._current_char in ATOMS['alpha_small']:
                self.peek_ident()
                if self._at_EOF:
                    break
                continue

            # class names
            if self._current_char in ATOMS['alpha_big']:
                self.peek_ident(cwass=True)
                if self._at_EOF:
                    break
                continue
            
            if self._current_char in ATOMS['number']:
                self.peek_int_float()
                if self._at_EOF:
                    break
                continue
            
            # string literals
            if self._current_char in ['|', '"']:
                self.peek_string()
                if self._at_EOF:
                    break
                continue

            # Symbol Checks
            if self._current_char == '=':
                cursor_advanced = self.peek_reserved('==', TokenType.EQUALITY_OPERATOR)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('=', TokenType.ASSIGNMENT_OPERATOR)
                if cursor_advanced:
                    continue

            if self._current_char == '+':
                cursor_advanced = self.peek_reserved('++', TokenType.INCREMENT_OPERATOR)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('+', TokenType.ADDITION_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '-':
                line, column = tuple(self._position)
                after_slice = self._lines[line][column+1:]
                before_slice = self._lines[line][:column]

                if len(after_slice) < 1:
                    line, col = self._position
                    self._logs.append(DelimError(TokenType.DASH, (line, col + 1), '-', '\n'))
                    self.advance()
                    continue

                # Check if - is negative
                valid_ops = [TokenType.ASSIGNMENT_OPERATOR, 
                             TokenType.ADDITION_SIGN, TokenType.DASH, TokenType.MULTIPLICATION_SIGN, TokenType.DIVISION_SIGN, TokenType.MODULO_SIGN,
                             TokenType.GREATER_THAN_SIGN, TokenType.LESS_THAN_SIGN ,TokenType.GREATER_THAN_OR_EQUAL_SIGN ,TokenType.LESS_THAN_OR_EQUAL_SIGN,
                             TokenType.EQUALITY_OPERATOR, TokenType.INEQUALITY_OPERATOR, 
                             TokenType.AND_OPERATOR, TokenType.OR_OPERATOR,
                             TokenType.STRING_PART_START, TokenType.STRING_PART_MID]
                operator_before = self._check_prev_token(valid_ops)
                line_copy = self._lines[line]
                if line_copy.lstrip()[0] == '-' or operator_before:
                    inc = 0
                    break_outer = False
                    continue_outer = False
                    for char in after_slice:
                        inc += 1
                        if char in [' ', '\t', '\n']:
                            continue
                        elif char not in ATOMS['number']:
                            # to prevent reading numbers in a string, identifier or function name
                            break
                        if char in ATOMS['number']:
                            self.advance(inc)
                            self.peek_int_float(negative=True, start_pos=(self._position[0], self._position[1]-inc))
                            if self._at_EOF:
                                break_outer = True
                            continue_outer = True
                            break
                    if break_outer:
                        break
                    if continue_outer:
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
                                self.advance(2)
                                continue
                    starting_position = ending_position = tuple(self._position)
                    self._tokens.append(Token('-', TokenType.DASH, starting_position, ending_position))
                    self.advance()
                    continue

            if self._current_char == '!':
                cursor_advanced = self.peek_reserved('!=', TokenType.INEQUALITY_OPERATOR)
                if cursor_advanced:
                    continue

                self._logs.append(GenericError(Error.UNEXPECTED_SYMBOL, tuple(self._position),
                                               context=f"Symbol {self._current_char} is invalid. Did you mean '!='?"))
                self.advance()
                continue

            if self._current_char == '>':
                cursor_advanced = self.peek_reserved('>=', TokenType.GREATER_THAN_OR_EQUAL_SIGN)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_comments()
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_comments(multiline=True)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('>', TokenType.GREATER_THAN_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '<':
                cursor_advanced = self.peek_reserved('<=', TokenType.LESS_THAN_OR_EQUAL_SIGN)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('<', TokenType.LESS_THAN_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '*':
                cursor_advanced = self.peek_reserved('*', TokenType.MULTIPLICATION_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '/':
                cursor_advanced = self.peek_reserved('/', TokenType.DIVISION_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '%':
                cursor_advanced = self.peek_reserved('%', TokenType.MODULO_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == "|":
                cursor_advanced = self.peek_reserved('||', TokenType.OR_OPERATOR)
                if cursor_advanced:
                    continue

            if self._current_char == "&":
                cursor_advanced = self.peek_reserved('&&', TokenType.AND_OPERATOR)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('&', TokenType.CONCATENATION_OPERATOR)
                if cursor_advanced:
                    continue

            if self._current_char == "{":
                cursor_advanced = self.peek_reserved('{', TokenType.OPEN_BRACE)
                if cursor_advanced:
                    continue

            if self._current_char == "}":
                cursor_advanced = self.peek_reserved('}', TokenType.CLOSE_BRACE)
                if cursor_advanced:
                    continue

            if self._current_char == "(":
                cursor_advanced = self.peek_reserved('(', TokenType.OPEN_PAREN)
                if cursor_advanced:
                    continue

            if self._current_char == ")":
                cursor_advanced = self.peek_reserved(')', TokenType.CLOSE_PAREN)
                if cursor_advanced:
                    continue

            if self._current_char == "[":
                cursor_advanced = self.peek_reserved('[[', TokenType.DOUBLE_OPEN_BRACKET)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved('[', TokenType.OPEN_BRACKET)
                if cursor_advanced:
                    continue

            if self._current_char == "]":
                cursor_advanced = self.peek_reserved(']]', TokenType.DOUBLE_CLOSE_BRACKET)
                if cursor_advanced:
                    continue

                cursor_advanced = self.peek_reserved(']', TokenType.CLOSE_BRACKET)
                if cursor_advanced:
                    continue

            if self._current_char == ",":
                cursor_advanced = self.peek_reserved(',', TokenType.COMMA)
                if cursor_advanced:
                    continue

            if self._current_char == ".":
                cursor_advanced = self.peek_reserved('.', TokenType.DOT_OP)
                if cursor_advanced:
                    continue

            if self._current_char == '~':
                cursor_advanced = self.peek_reserved('~', TokenType.TERMINATOR)
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
        i = start
        while i < prev_count:
            if len(self.tokens) >= i:
                prev_token = self.tokens[-i]
                if prev_token.token == TokenType.WHITESPACE:
                    prev_count += 1
                    i += 1
                    continue

                in_same_line = prev_token.position[0] == self._position[0]
                if in_same_line:
                    if to_check[to_check_index] == TokenType.GEN_CWASS_NAME and prev_token.token.token.startswith('CWASS'):
                        present_flag = True
                        i += 1
                    elif to_check[to_check_index] == TokenType.GEN_IDENTIFIER and prev_token.token.token.startswith('IDENTIFIER'):
                        present_flag = True
                        i += 1
                    else:
                        if prev_token.token in to_check and prev_token.position[0] == self._position[0]:
                            present_flag = True
                            i += 1
                        else:
                            present_flag = False
                            i += 1
                            break
            to_check_index += 1
            i += 1

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
