from sys import argv
from pathlib import Path

from constants.constants import *
from .token import *
from .error_handler import *

from .lexer_components.move_cursor import advance, reverse

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
    def move_cursor_context(self):
        'to be passed to outside modules'
        return self._lines, self._position, self._current_char

    def _get_tokens(self):
        is_end_of_file = False
        cursor_advanced = False
        valid_starting_chars = {*ATOMS['alphanum'], *ATOMS['general_operator'],
                                '|', '&', '{', '}', '[', ']', '(', ')', ',', '.', '~', '"'}
        
        while not is_end_of_file:
            if self._current_char in ['\n', ' ']:
                is_end_of_file, self._current_char = advance(self.move_cursor_context)
                if is_end_of_file:
                    break
                continue

            if self._current_char not in valid_starting_chars:
                self._logs.append(GenericError(Error.UNEXPECTED_SYMBOL, tuple(self._position)))
                is_end_of_file, self._current_char = advance(self.move_cursor_context)
                if is_end_of_file:
                    break
                continue

            if self._current_char == 'b':
                cursor_advanced, is_end_of_file = self._peek('bweak', TokenType.BWEAK)
                if cursor_advanced:
                    continue

            if self._current_char == 'c':
                cursor_advanced, is_end_of_file = self._peek('chan', TokenType.CHAN)
                if cursor_advanced:
                    continue
                cursor_advanced, is_end_of_file = self._peek('cap', TokenType.CAP)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('cwass', TokenType.CWASS)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'd':
                cursor_advanced, is_end_of_file = self._peek('dono', TokenType.DONO)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('do whiwe', TokenType.DO_WHIWE)
                if cursor_advanced:
                    continue
                
                cursor_advanced, is_end_of_file = self._peek('donee~', TokenType.DONE)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'e':
                cursor_advanced, is_end_of_file = self._peek('ewse iwf', TokenType.EWSE_IWF)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('ewse', TokenType.EWSE)
                if cursor_advanced:
                    continue
                
            if self._current_char == 'f':
                cursor_advanced, is_end_of_file = self._peek("fwunc", TokenType.FWUNC)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('fax', TokenType.FAX)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('fow', TokenType.FOW)
                if cursor_advanced:
                    continue
        
            if self._current_char == 'g':
                cursor_advanced, is_end_of_file = self._peek('gwobaw', TokenType.GWOBAW)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'i':
                cursor_advanced, is_end_of_file = self._peek('iwf', TokenType.IWF)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('inpwt', TokenType.INPWT)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'k':
                cursor_advanced, is_end_of_file = self._peek('kun', TokenType.KUN)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'm':
                cursor_advanced, is_end_of_file = self._peek('mainuwu', TokenType.MAINUWU)
                if cursor_advanced:
                    continue

            if self._current_char == 'n':
                cursor_advanced, is_end_of_file = self._peek('nuww', TokenType.NUWW)
                if cursor_advanced:
                    continue
            
            if self._current_char == 'p':
                cursor_advanced, is_end_of_file = self._peek('pwint', TokenType.PWINT)
                if cursor_advanced:
                    continue

            if self._current_char == 's':
                cursor_advanced, is_end_of_file = self._peek('san', TokenType.SAN)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('sama', TokenType.SAMA)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('senpai', TokenType.SENPAI)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('staart!', TokenType.START)
                if cursor_advanced:
                    continue

            if self._current_char == 'w':
                cursor_advanced, is_end_of_file = self._peek('whiwe', TokenType.WHIWE)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('wetuwn', TokenType.WETUWN)
                if cursor_advanced:
                    continue
            
            # Literals check
            # can be identifiers or function names
            if self._current_char in ATOMS['alpha_small']:
                cursor_advanced, is_end_of_file = self._is_identifier()
                if cursor_advanced:
                    if is_end_of_file:
                        break
                    is_end_of_file, self._current_char = advance(self.move_cursor_context)
                    continue

            # class names
            if self._current_char in ATOMS['alpha_big']:
                cursor_advanced, is_end_of_file = self._is_identifier(cwass=True)
                if cursor_advanced:
                    if is_end_of_file:
                        break
                    is_end_of_file, self._current_char = advance(self.move_cursor_context)
                    continue
            
            if self._current_char in ATOMS['number']:
                is_end_of_file = self._peek_int_float_literal()
                if is_end_of_file:
                    break
                continue
            
            # string literals
            if self._current_char in ['|', '"']:
                is_end_of_file = self._peek_string_literal()
                if is_end_of_file:
                    break
                continue

            # Symbol Checks
            if self._current_char == '=':
                cursor_advanced, is_end_of_file = self._peek('==', TokenType.EQUALITY_OPERATOR)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('=', TokenType.ASSIGNMENT_OPERATOR)
                if cursor_advanced:
                    continue

            if self._current_char == '+':
                cursor_advanced, is_end_of_file = self._peek('++', TokenType.INCREMENT_OPERATOR)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('+', TokenType.ADDITION_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '-':
                line, column = tuple(self._position)
                after_slice = self._lines[line][column+1:]
                before_slice = self._lines[line][:column]

                if len(after_slice) < 1:
                    line, col = self._position
                    self._logs.append(DelimError(TokenType.DASH, (line, col + 1), '-', '\n'))

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
                        is_end_of_file, self._current_char = advance(self.move_cursor_context)
                        is_end_of_file = self._peek_int_float_literal(negative=True)
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
                                self._current_char = advance(self.move_cursor_context)
                                is_end_of_file, self._current_char = advance(self.move_cursor_context, 2)
                                continue
                    starting_position = ending_position = tuple(self._position)
                    self._tokens.append(Token('-', TokenType.DASH, starting_position, ending_position))
                    is_end_of_file, self._current_char = advance(self.move_cursor_context)
                    continue

            if self._current_char == '!':
                cursor_advanced, is_end_of_file = self._peek('!=', TokenType.INEQUALITY_OPERATOR)
                if cursor_advanced:
                    continue

                self._logs.append(GenericError(Error.UNEXPECTED_SYMBOL, tuple(self._position),
                                               context=f"Symbol {self._current_char} is invalid. Did you mean '!='?"))

            if self._current_char == '>':
                cursor_advanced, is_end_of_file = self._peek('>=', TokenType.GREATER_THAN_OR_EQUAL_SIGN)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek_comments()
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek_comments(multiline=True)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('>', TokenType.GREATER_THAN_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '<':
                cursor_advanced, is_end_of_file = self._peek('<=', TokenType.LESS_THAN_OR_EQUAL_SIGN)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('<', TokenType.LESS_THAN_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '*':
                cursor_advanced, is_end_of_file = self._peek('*', TokenType.MULTIPLICATION_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '/':
                cursor_advanced, is_end_of_file = self._peek('/', TokenType.DIVISION_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '%':
                cursor_advanced, is_end_of_file = self._peek('%', TokenType.MODULO_SIGN)
                if cursor_advanced:
                    continue

            if self._current_char == "|":
                cursor_advanced, is_end_of_file = self._peek('||', TokenType.OR_OPERATOR)
                if cursor_advanced:
                    continue

            if self._current_char == "&":
                cursor_advanced, is_end_of_file = self._peek('&&', TokenType.AND_OPERATOR)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('&', TokenType.CONCATENATION_OPERATOR)
                if cursor_advanced:
                    continue

            if self._current_char == "{":
                cursor_advanced, is_end_of_file = self._peek('{', TokenType.OPEN_BRACE)
                if cursor_advanced:
                    continue

            if self._current_char == "}":
                cursor_advanced, is_end_of_file = self._peek('}', TokenType.CLOSE_BRACE)
                if cursor_advanced:
                    continue

            if self._current_char == "(":
                cursor_advanced, is_end_of_file = self._peek('(', TokenType.OPEN_PAREN)
                if cursor_advanced:
                    continue

            if self._current_char == ")":
                cursor_advanced, is_end_of_file = self._peek(')', TokenType.CLOSE_PAREN)
                if cursor_advanced:
                    continue

            if self._current_char == "[":
                cursor_advanced, is_end_of_file = self._peek('[[', TokenType.DOUBLE_OPEN_BRACKET)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('[', TokenType.OPEN_BRACKET)
                if cursor_advanced:
                    continue

            if self._current_char == "]":
                cursor_advanced, is_end_of_file = self._peek(']]', TokenType.DOUBLE_CLOSE_BRACKET)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek(']', TokenType.CLOSE_BRACKET)
                if cursor_advanced:
                    continue

            if self._current_char == ",":
                cursor_advanced, is_end_of_file = self._peek(',', TokenType.COMMA)
                if cursor_advanced:
                    continue

            if self._current_char == ".":
                cursor_advanced, is_end_of_file = self._peek('.', TokenType.DOT_OP)
                if cursor_advanced:
                    continue

            if self._current_char == '~':
                cursor_advanced, is_end_of_file = self._peek('~', TokenType.TERMINATOR)
                if cursor_advanced:
                    continue

            if is_end_of_file:
                break
            is_end_of_file, self._current_char = advance(self.move_cursor_context)

    def _verify_delim(self, delim_set: set[str], current = False) -> tuple[bool, str]:
        line, column = self._position

        if current:
            next_char = self._lines[line][column]
        elif column+1 >= len(self._lines[line]):
            next_char = '\n'
        else:
            next_char = self._lines[line][column+1]

        is_delim = True if next_char in delim_set else False
            
        return is_delim, next_char

    def _peek(self, to_check: str, token_type: TokenType,
              before: bool = False, ignore_space: bool = False) -> tuple[bool,bool]:
        '''
        Main process

        1. checks whether the given to_check string is equal to characters directly before/after the current character (current character included in check)
        2. if equal, call _verify_delim to verify the delimiter
        3. if delimiter is correct, this will append the to_check string as a lexeme to the list of tokens

        _____________________

        Optional processes

        4. if before is true, the function will check the characters before the current character instead (current character included in check)
        5. if ignore_space is true, the function will skip checking whitespaces present in the source code
                - so "a q u a" will be equal to to_check="aqua"
                - this is useful for checking if a keyword is present directly before/after the current character which may be separated by whitespace/s

        '''
        length = len(to_check)
        line, column = self._position

        if before:
            # if length = 5; [0,1,2,3,4] start at index 4 and end in -1 to include 0
            start = (length-1, column)
            end = (-1, column-length)
            increment = -1
        else:
            start = (0, column)
            end = (length, column+length)
            increment = 1

        is_equal = True
        if ignore_space:
            i = start[0]
            j = start[1]
            if before:
                while (i > end[0]) and (j > end[1]):
                    if self._lines[line][j] == " ":
                        continue
                    if to_check[i] != self._lines[line][j]:
                        is_equal = False
                        break
                    i -= 1
                    j -= 1
            else:
                while (i < end[0]) and (j < end[1]):
                    if self._lines[line][j] == " ":
                        continue
                    if to_check[i] != self._lines[line][j]:
                        is_equal = False
                        break
                    i += 1
                    j += 1
        else:
            for i,j in zip(range(start[0], end[0], increment), range(start[1], end[1], increment)):
                if j >= len(self._lines[line]) or to_check[i] != self._lines[line][j]:
                    is_equal = False
                    break
        
        is_end_of_file = False
        cursor_advanced = False
        if is_equal:
            if before:
                starting_position = (line, end[1]+1)
                ending_position = (line, column)
            
            else:
                starting_position = (line, column)
                ending_position = (line, end[1]-1)
                self._current_char = advance(self.move_cursor_context, end[1]-column-1)
                
            lexeme = to_check
            next_char_is_correct_delim, delim = self._verify_delim(token_type.expected_delims)
            if next_char_is_correct_delim:
                self._tokens.append(Token(lexeme, token_type, starting_position, ending_position))
            else:
                is_end_of_file, self._current_char = advance(self.move_cursor_context)
                # preemptively check if the lexeme or current character is not valid to be in a fwunc/cwass/identifier name
                in_new_line = self._position[0] != line
                if not any(char in ATOMS['alphanum'] for char in lexeme) or not self._current_char in ATOMS['alphanum'] or in_new_line:
                    self._current_char = reverse(self.move_cursor_context)
                    line, col = ending_position
                    self._logs.append(DelimError(token_type, (line, col + 1), lexeme, delim))
                else:
                    # check if identifier
                    cursor_advanced, _ = self._is_identifier(from_keyword=to_check)
            
            is_end_of_file, self._current_char = advance(self.move_cursor_context)
            cursor_advanced = True

        else:
            cursor_advanced = False

        return cursor_advanced, is_end_of_file
    
    def _seek(self, to_seek: str|list[str], before: bool = False, multi_line_count: int|str = 0,
              ignore_space = True, max_space_count: int = None, alphanum_only: bool = False,
              include_current: bool = False) -> bool:
        '''
        seeks concatenated characters ('ab') or multiple separate characters (['a', 'b']) in order;

        can search through multi lines but line count should be indicated

        can go until end|beginning of file if "EOF|BOF" is passed as multi_line_count
        '''
        if isinstance(to_seek, str):
            to_seek = [to_seek]
            
        line = self._position[0]
        if before and isinstance(multi_line_count, int):
            multi_line = line - multi_line_count
        elif not before and isinstance(multi_line_count, int):
            multi_line = line + multi_line_count

        if multi_line_count == "EOF":
            multi_line = len(self._lines) - 1
        elif multi_line_count == "BOF":
            multi_line = 0
        is_max_multi_line = None

        space_count = 0

        cursor_advance_reverse_count = 0
        found = [False]*len(to_seek)
        file_out_of_bounds = False
        
        for i in range(len(found)):
            if not include_current:
                if before:
                    file_out_of_bounds, self._current_char = reverse(self.move_cursor_context)
                else:
                    file_out_of_bounds, self._current_char = advance(self.move_cursor_context)
                cursor_advance_reverse_count += 1

            while not found[i]:
                preempt_start_char_index = len(to_seek[i])-1 if before else 0
                # intial check if you already got to the beginning or end of file form previous searches
                if file_out_of_bounds:
                    break
                
                # limit number of times reversing can go to newlines with multi_line_count
                if is_max_multi_line is None:
                    is_max_multi_line = multi_line > self._position[0] if before else multi_line < self._position[0]

                if is_max_multi_line:
                    cursor_advance_reverse_count -= 1
                    if before:
                        self._current_char = advance(self.move_cursor_context)
                    else:
                        self._current_char = reverse(self.move_cursor_context)
                    break
                
                if self._current_char == to_seek[i][preempt_start_char_index]:
                    if len(to_seek[i]) == 1:
                        found[i] = True
                        break

                    preempt_success = True
                    if before:
                        preempt_iter = range(len(to_seek[i])-2, -1, -1)
                        last_iter = 0 
                    else:
                        preempt_iter = range(1, len(to_seek[i]), 1)
                        last_iter = len(to_seek[i])-1

                    for preempt in preempt_iter:
                        if before:
                            file_out_of_bounds, self._current_char = reverse(self.move_cursor_context)
                        else:
                            file_out_of_bounds, self._current_char = advance(self.move_cursor_context)
                        cursor_advance_reverse_count += 1

                        is_max_multi_line = multi_line > self._position[0] if before else multi_line < self._position[0]
                        # limit number of times reversing can go to newlines with multi_line_count
                        if is_max_multi_line or file_out_of_bounds:
                            preempt_success = False
                            cursor_advance_reverse_count -= 1
                            if before:
                                self._current_char = advance(self.move_cursor_context)
                            else:
                                self._current_char = reverse(self.move_cursor_context)
                            break

                        # don't check for last character (not included in to_seek)
                        elif preempt == last_iter and not preempt_success:
                            preempt_success = False
                            break
                        elif to_seek[i][preempt] != self._current_char:
                            preempt_success = False
                            break

                    if preempt_success:
                        found[i] = True
                        break

                elif self._current_char == ' ':
                    if ignore_space:
                        space_count += 1
                        if max_space_count and space_count > max_space_count:
                            break

                        cursor_advance_reverse_count += 1
                        if before:
                            file_out_of_bounds, self._current_char = reverse(self.move_cursor_context)
                        else:
                            file_out_of_bounds, self._current_char = advance(self.move_cursor_context)
                        if file_out_of_bounds:
                            break

                        is_max_multi_line = multi_line > self._position[0] if before else multi_line < self._position[0]
                        if is_max_multi_line:
                            cursor_advance_reverse_count -= 1
                            if before:
                                self._current_char = advance(self.move_cursor_context)
                            else:
                                self._current_char = reverse(self.move_cursor_context)
                            break
                    else:
                        break
    
                elif alphanum_only and self._current_char not in ATOMS['alphanum']:
                    break
    
                else:
                    if before:
                        file_out_of_bounds, self._current_char = reverse(self.move_cursor_context)
                    else:
                        file_out_of_bounds, self._current_char = advance(self.move_cursor_context)
                    cursor_advance_reverse_count += 1
                    # check again after reversing
                    if file_out_of_bounds:
                        break
                    
                    is_max_multi_line = multi_line > self._position[0] if before else multi_line < self._position[0]
                    if is_max_multi_line:
                        cursor_advance_reverse_count -= 1
                        if before:
                            self._current_char = advance(self.move_cursor_context)
                        else:
                            self._current_char = reverse(self.move_cursor_context)
                        break
        if before:
            self._current_char = advance(self.move_cursor_context, cursor_advance_reverse_count)
        else:
            self._current_char = reverse(self.move_cursor_context, cursor_advance_reverse_count)
        return all(found)


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
    
    def _is_identifier(self, from_keyword: str = None, cwass: bool = False) -> bool:
        cursor_advanced = False
        temp_id = from_keyword if from_keyword else ''
        current_line = self._position[0]

        if cwass:
            expected_delims = DELIMS['cwass']
            unique_token = UniqueTokenType.CWASS
            delim_error_token = TokenType.GEN_CWASS_NAME
        else:
            expected_delims = DELIMS['id'] 
            unique_token = UniqueTokenType.ID 
            delim_error_token = TokenType.GEN_IDENTIFIER

        while True:
            temp_id += self._current_char
            is_end_of_file, self._current_char = advance(self.move_cursor_context)
            in_next_line = self._position[0] != current_line

            if is_end_of_file or in_next_line:
                if in_next_line:
                    self._current_char = reverse(self.move_cursor_context)

                line, col = self._position
                self._logs.append(DelimError(TokenType.GEN_IDENTIFIER, (line, col + 1), temp_id, '\n'))
                cursor_advanced = True
                break

            elif self._current_char in expected_delims:
                self._current_char = reverse(self.move_cursor_context)
                starting_position = (self._position[0], self._position[1]-len(temp_id)+1)
                ending_position = (self._position[0], self._position[1])
                self._tokens.append(Token(temp_id, UniqueTokenType(temp_id, unique_token),
                                              starting_position, ending_position))
                cursor_advanced = True
                break

            elif not self._current_char.isalnum():
                special_char = self._current_char
                self._current_char = reverse(self.move_cursor_context)

                line, col = self._position
                self._logs.append(DelimError(delim_error_token, (line, col + 1), temp_id, special_char))
                cursor_advanced = True
                break

        return cursor_advanced, is_end_of_file
    
    def _peek_string_literal(self):
        if self._current_char == '"':
            token_types = (TokenType.STRING_PART_START, TokenType.STRING_LITERAL)
        elif self._current_char == "|":
            token_types = (TokenType.STRING_PART_MID, TokenType.STRING_PART_END)
        
        temp_string = ''
        escape_count = 0
        current_line = self._position[0]

        while True:
            temp_string += self._current_char
            is_end_of_file, self._current_char = advance(self.move_cursor_context)
            in_next_line = self._position[0] != current_line

            if is_end_of_file or in_next_line:
                if in_next_line:
                    self._current_char = reverse(self.move_cursor_context)
                starting_position = (self._position[0], self._position[1]-len(temp_string)+1)
                ending_position = (self._position[0], self._position[1])
                self._logs.append(GenericError(Error.UNCLOSED_STRING, starting_position, ending_position,
                                               context = f"'{temp_string}' is unclosed"))
                break

            elif self._current_char == '\\':
                is_end_of_file, self._current_char = advance(self.move_cursor_context)
                if is_end_of_file:
                    break

                # NOTE put escapable characters here
                if self._current_char not in ["|", '"']:
                    self._current_char = reverse(self.move_cursor_context)
                    temp_string += '\\'
                else:
                    escape_count += 1
            
            elif self._current_char in ['|', '"']:
                if self._current_char == '|':
                    token_type = token_types[0]
                    delims = DELIMS['string_parts'] 
                else:
                    token_type = token_types[1]
                    delims = DELIMS['string'] 

                temp_string += self._current_char
                temp_string = '"' + temp_string[1:-1] + '"'
                temp_string_length = len(temp_string) + escape_count

                starting_position = (self._position[0], self._position[1]-temp_string_length+1)
                ending_position = (self._position[0], self._position[1])

                next_char_is_correct_delim, delim = self._verify_delim(delims)
                if next_char_is_correct_delim:
                    self._tokens.append(Token(temp_string, token_type, starting_position, ending_position))
                else:
                    self._logs.append(DelimError(token_type, (ending_position[0], ending_position[1] + 1), temp_string, delim))
                break
        
        is_end_of_file, self._current_char = advance(self.move_cursor_context)
        return is_end_of_file

    def _peek_int_float_literal(self, negative=False):
        temp_num = "-"+self._current_char if negative else self._current_char
        current_line = self._position[0]
        break_outside_loop = False

        while True:
            is_end_of_file, self._current_char = advance(self.move_cursor_context)
            in_next_line = self._position[0] != current_line
            if is_end_of_file or in_next_line:
                if in_next_line:
                    self._current_char = reverse(self.move_cursor_context)
                line, col = self._position
                self._logs.append(DelimError(TokenType.INT_LITERAL, (line, col + 1), temp_num, '\n'))
                break

            # preemptively break when a delimiter is found for integers
            if self._current_char in DELIMS['int_float']:
                self._current_char = reverse(self.move_cursor_context)
                corrected_value = temp_num
                starting_position = (self._position[0], self._position[1] - len(temp_num) + 1)
                ending_position = (self._position[0], self._position[1])

                self._tokens.append(Token(corrected_value, TokenType.INT_LITERAL, starting_position, ending_position))
                break

            # floats that can have one leading zero
            elif self._current_char == '.':
                temp_num += self._current_char
                while True:
                    is_end_of_file, self._current_char = advance(self.move_cursor_context)
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._current_char = reverse(self.move_cursor_context)
                        line, col = self._position
                        self._logs.append(DelimError(TokenType.FLOAT_LITERAL, (line, col + 1), temp_num, '\n'))
                        break

                    # preemptively break when a delimiter is found for floats
                    elif self._current_char in DELIMS['int_float']:
                        self._current_char = reverse(self.move_cursor_context)
                        corrected_value = temp_num
                        starting_position = tuple([self._position[0], self._position[1] - len(temp_num) + 1])
                        ending_position = tuple(self._position)

                        # has no numbers after decimal point
                        if temp_num[-1:] == '.':
                            corrected_value = temp_num + '0'
                            starting_position = tuple([self._position[0], self._position[1] - len(temp_num) + 1])
                            ending_position = tuple(self._position)
                            self._logs.append(
                                GenericError(Error.MISSING_TRAILING_ZERO_FLOAT, starting_position, ending_position,
                                             context=f"consider replacing '{temp_num}' with '{corrected_value}'"))
                            break_outside_loop = True
                            break

                        self._tokens.append(
                            Token(corrected_value, TokenType.FLOAT_LITERAL, starting_position, ending_position))
                        break

                    elif not self._current_char.isdigit():
                        invalid_delim = self._current_char
                        self._current_char = reverse(self.move_cursor_context)
                        self._logs.append(
                            DelimError(TokenType.INT_LITERAL, tuple(self._position), temp_num, invalid_delim))
                        break

                    temp_num += self._current_char
                break

            elif not self._current_char.isdigit():
                invalid_delim = self._current_char
                self._current_char = reverse(self.move_cursor_context)
                self._logs.append(DelimError(TokenType.INT_LITERAL, tuple(self._position), temp_num, invalid_delim))
                break

            temp_num += self._current_char

        is_end_of_file, self._current_char = advance(self.move_cursor_context)
        return is_end_of_file

    def _peek_comments(self, multiline: bool = False) -> bool:
        'returns true if found comments/error about comments, false otherwise'
        to_seek = r'>//<' if multiline else '>.<'
        comment_indicator_exists = self._seek(to_seek, include_current=True)

        current_line = self._position[0]
        cursor_advanced = False
        is_end_of_file = True

        if comment_indicator_exists:
            if multiline:
                starting_position = tuple(self._position)
                is_end_of_file, self._current_char = advance(self.move_cursor_context, len(to_seek)-1)
                temp_comment = to_seek

                closing_comment_indicator_exists = self._seek(to_seek, multi_line_count='EOF')
                if closing_comment_indicator_exists:
                    # keep appending until found >//< in order
                    while True:
                        current_line = self._position[0]
                        is_end_of_file, self._current_char = advance(self.move_cursor_context)

                        if self._position[0] > current_line:
                            temp_comment += '\n'
                        temp_comment += self._current_char

                        if self._current_char == '/' and self._lines[self._position[0]][self._position[1]+1] == '/' and self._lines[self._position[0]][self._position[1]+2] == '<':
                            is_end_of_file, self._current_char = advance(self.move_cursor_context, 3)
                            temp_comment += '/<'

                            ending_position = tuple(self._position)
                            self._tokens.append(Token(temp_comment, TokenType.MULTI_LINE_COMMENT, starting_position, ending_position))
                            break

                else:
                    # comment out the rest of the code if there is no closing indicator is 
                    while not is_end_of_file:
                        current_line = self._position[0]
                        is_end_of_file, self._current_char = advance(self.move_cursor_context)

                        if self._position[0] > current_line:
                            temp_comment += '\n'
                        if not is_end_of_file:
                            temp_comment += self._current_char

                        if is_end_of_file:
                            ending_position = self._position.copy()
                            self._logs.append(GenericWarning(Warn.UNCLOSED_MULTI_LINE_COMMENT, starting_position))
                            self._tokens.append(Token(temp_comment, TokenType.MULTI_LINE_COMMENT, starting_position, ending_position))

            else:
                temp_comment = to_seek
                starting_position = tuple(self._position)
                is_end_of_file, self._current_char = advance(self.move_cursor_context, len(to_seek)-1)
                while True:
                    is_end_of_file, self._current_char = advance(self.move_cursor_context)
                    in_next_line = self._position[0] > current_line
                    if not is_end_of_file and not in_next_line:
                        temp_comment += self._current_char

                    if is_end_of_file or in_next_line:
                        ending_position = tuple(self._position)
                        self._tokens.append(Token(temp_comment, TokenType.SINGLE_LINE_COMMENT, starting_position, ending_position))
                        break


            cursor_advanced = True
        else:
            cursor_advanced = False

        return cursor_advanced, is_end_of_file

def print_lex(source_code: list[str]):
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