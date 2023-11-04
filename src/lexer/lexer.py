from sys import argv
from pathlib import Path

from constants.constants import *
from .token import *
from .error_handler import *

class Lexer():
    'description'

    def __init__(self, source_code: list[str]):
        self._lines = source_code

        self._position = [0,0]
        self._current_char = self._lines[self._position[0]][self._position[1]]

        self._nest_level = 0

        self._tokens: list[Token] = []
        self._errors: list[DelimError] = []

        self._get_tokens()

    @property
    def tokens(self) -> list[Token]:
        return self._tokens

    @property
    def errors(self):
        return self._errors

    def _get_tokens(self):
        is_end_of_file = False
        cursor_advanced = False
        
        while not is_end_of_file:
            if self._current_char == 'b':
                cursor_advanced, is_end_of_file = self._peek('bweak', TokenType.BWEAK)
                if cursor_advanced:
                    continue

            if self._current_char == 'c':
                cursor_advanced, is_end_of_file = self._peek('chan', TokenType.CHAN)
                if cursor_advanced:
                    continue
                cursor_advanced, is_end_of_file = self._peek('cap', TokenType.BOOL_LITERAL)
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

                cursor_advanced, is_end_of_file = self._peek('fax', TokenType.BOOL_LITERAL)
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

            # Symbol Checks
            if self._current_char == '=':
                cursor_advanced, is_end_of_file = self._peek('==', TokenType.EQUALITY)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('=', TokenType.ASSIGN)
                if cursor_advanced:
                    continue

            if self._current_char == '+':
                cursor_advanced, is_end_of_file = self._peek('++', TokenType.UNARY)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('+', TokenType.ARITHMETIC)
                if cursor_advanced:
                    continue

            if self._current_char == '-':
                # Check if - is dash data type
                line, column = tuple(self._position)
                after_slice = self._lines[line][column+1:]
                data_types = ["chan", "kun", "sama", "senpai", "san", "dono"]
                valid_data_type = None
                # Check if the valid data types exist after the -
                for data_type in data_types:
                    if len(data_type) <= len(after_slice):
                        equal = True
                        for expected_char, actual_char in zip(data_type, after_slice):
                            if expected_char != actual_char:
                                equal = False
                                break
                        if equal:
                            valid_data_type = data_type
                            break

                # If there is a valid data type after the -
                if valid_data_type is not None:
                    if len(valid_data_type) < len(after_slice):
                        delim = after_slice[len(valid_data_type)]
                        if delim in TokenType.DATA_TYPE.expected_delims:
                            starting_position = ending_position = tuple(self._position)
                            self._tokens.append(Token('-', 'ID_DELIM', starting_position, ending_position))
                            is_end_of_file = self._advance()
                            continue
                    elif len(valid_data_type) == len(after_slice):
                        starting_position = ending_position = tuple(self._position)
                        self._tokens.append(Token('-', 'ID_DELIM', starting_position, ending_position))
                        is_end_of_file = self._advance()
                        continue

                # Check if - is negative
                valid_ops = [TokenType.ASSIGN, TokenType.ARITHMETIC, TokenType.RELATIONAL,
                             TokenType.EQUALITY, TokenType.LOGIC]
                operator_before = self._check_prev_token(valid_ops)
                if column == 0 or operator_before:
                    cursor_advanced, is_end_of_file = self._peek('-', TokenType.NEGATIVE)
                    if cursor_advanced:
                        continue

                # Differentiate between arithmetic and unary
                if len(after_slice) > 0:
                    # If next char is a dash, check if it is delimited by unary expected delims
                    if self._lines[line][column+1] == '-':
                        if len(after_slice) > 1:
                            if self._lines[line][column+2] in TokenType.UNARY.expected_delims:
                                # Check if prev token is identifier
                                identifier_before = self._check_prev_token(TokenType.IDENTIFIER)
                                if identifier_before:
                                    starting_position = tuple(self._position)
                                    ending_position = tuple([self._position[0], self._position[1]+1])
                                    self._tokens.append(Token('--', TokenType.UNARY, starting_position, ending_position))
                                else:
                                    pass
                                    # Throw custom error - Missing identifier
                                is_end_of_file = self._advance(2)
                                continue
                    starting_position = ending_position = tuple(self._position)
                    self._tokens.append(Token('-', TokenType.ARITHMETIC, starting_position, ending_position))
                    is_end_of_file = self._advance()
                    continue

                # negative

            if self._current_char == '!':
                cursor_advanced, is_end_of_file = self._peek('!=', TokenType.EQUALITY)
                if cursor_advanced:
                    continue

                # throw custom error - unexpected symbol

            if self._current_char == '>':
                cursor_advanced, is_end_of_file = self._peek('>=', TokenType.RELATIONAL)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek_comments()
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek_comments(multiline=True)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('>', TokenType.RELATIONAL)
                if cursor_advanced:
                    continue

            if self._current_char == '<':
                cursor_advanced, is_end_of_file = self._peek('<=', TokenType.RELATIONAL)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('<', TokenType.RELATIONAL)
                if cursor_advanced:
                    continue

            if self._current_char == '*':
                cursor_advanced, is_end_of_file = self._peek('*', TokenType.ARITHMETIC)
                if cursor_advanced:
                    continue

            if self._current_char == '/':
                cursor_advanced, is_end_of_file = self._peek('/', TokenType.ARITHMETIC)
                if cursor_advanced:
                    continue

            if self._current_char == '%':
                cursor_advanced, is_end_of_file = self._peek('%', TokenType.ARITHMETIC)
                if cursor_advanced:
                    continue

            if self._current_char == "|":
                cursor_advanced, is_end_of_file = self._peek('||', TokenType.LOGIC)
                if cursor_advanced:
                    continue

                # throw custom error - unexpected symbol

            if self._current_char == "&":
                cursor_advanced, is_end_of_file = self._peek('&&', TokenType.LOGIC)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('&', TokenType.CONCAT)
                if cursor_advanced:
                    continue

            if self._current_char == "{":
                cursor_advanced, is_end_of_file = self._peek('{', TokenType.OPEN_BRACE)
                if cursor_advanced:
                    continue

            if self._current_char == "}":
                cursor_advanced, is_end_of_file = self._peek('{', TokenType.CLOSE_BRACE)
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
                cursor_advanced, is_end_of_file = self._peek(',', TokenType.DOT_OP)
                if cursor_advanced:
                    continue

            if self._current_char == '~':
                cursor_advanced, is_end_of_file = self._peek('~', TokenType.TERMINATOR)
                if cursor_advanced:
                    continue

            # can be identifiers or function names
            if self._current_char in ATOMS['alpha']:
                cwass = False if self._current_char == self._current_char.lower() else True
                cursor_advanced, is_end_of_file = self._is_func_or_cwass_name(cwass)
                if cursor_advanced:
                    if is_end_of_file:
                        break
                    is_end_of_file = self._advance()
                    continue

                else:
                    # make temp_id to hold read chars
                    cursor_advanced, is_end_of_file = self._is_identifier()
                    if cursor_advanced:
                        if is_end_of_file:
                            break
                        is_end_of_file = self._advance()
                        continue


            if self._current_char in ['|', '"']:
                is_end_of_file = self._peek_string_literal()
                if is_end_of_file:
                    break
                continue

            if self._current_char in ATOMS['number']:
                is_end_of_file = self._peek_int_float_literal()
                if is_end_of_file:
                    break
                continue

            if is_end_of_file:
                break
            is_end_of_file = self._advance()
    
    def _advance(self, increment: int = 1) -> bool:        
        # initial check if EOF already
        temp_position = self._position[1]
        temp_position += increment
        end_of_file = temp_position > len(self._lines[len(self._lines)-1])-1 and self._position[0] == len(self._lines)-1
        if end_of_file:
            self._position[1] += increment
            self._current_char = None
            return True
        
        # increment cursor
        # go to next line first char if out of bounds in current line (index 'length+1')
        self._position[1] += increment
        current_line_length = len(self._lines[self._position[0]])
        while self._position[1] >= current_line_length:
            self._position[1] -= current_line_length
            self._position[0] += 1
            current_line_length = len(self._lines[self._position[0]])
        
        # check if EOF after incrementing
        # if not EOF, read current character since we're sure we are not out of bounds otherwise due to previous check
        end_of_file = self._position[0] >= len(self._lines)
        if end_of_file:
            self._current_char = None
            return True
        else:
            self._current_char = self._lines[self._position[0]][self._position[1]]
            return False
    
    def _reverse(self, increment: int = 1) -> bool:
        # initial check if BOF already
        temp_position = self._position[1]
        temp_position -= increment
        beginning_of_file = temp_position < 0 and self._position[0] == 0
        if beginning_of_file:
            self._position[1] -= increment
            self._current_char = None
            return True
        
        # decrement cursor
        # go to previous line last char if out of bounds in current line (index '-1')
        self._position[1] -= increment
        while self._position[1] < 0:
            self._position[0] -= 1
            current_line_length = len(self._lines[self._position[0]])
            self._position[1] += current_line_length

        # assign current char since we're sure we are not out of bounds
        self._current_char = self._lines[self._position[0]][self._position[1]]

        # check if BOF after decrementing, return true if so
        beginning_of_file = self._position == [0,0]
        return True if beginning_of_file else False
            
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
                self._advance(end[1]-column-1)
                
            lexeme = to_check
            next_char_is_correct_delim, delim = self._verify_delim(token_type.expected_delims)
            if next_char_is_correct_delim:
                self._tokens.append(Token(lexeme, token_type, starting_position, ending_position))
            else:
                is_end_of_file = self._advance()
                # preemptively check if the lexeme or current character is not valid to be in a fwunc/cwass/identifier name
                in_new_line = self._position[0] != line
                if not any(char in ATOMS['alphanum'] for char in lexeme) or not self._current_char in ATOMS['alphanum'] or in_new_line:
                    _ = self._reverse()
                    line, col = ending_position
                    self._errors.append(DelimError(token_type, (line, col+1), lexeme, delim))
                else:
                    # check if function name before identifier
                    cursor_advanced, _ = self._is_func_or_cwass_name(from_keyword=to_check)
                    if not cursor_advanced:
                        # check if identifier
                        cursor_advanced, _ = self._is_identifier(from_keyword=to_check)
            
            is_end_of_file = self._advance()
            cursor_advanced = True

        else:
            cursor_advanced = False

        return cursor_advanced, is_end_of_file
    
    def _seek(self, to_seek: str|list[str], before: bool = False, multi_line_count: int|str = 0, ignore_space = True) -> bool:
        '''
        seeks concatenated characters ('ab') or multiple separate characters (['a', 'b']) in order;

        can search through multi lines but line count should be indicated

        can go until end|beginning of file if "EOF|BOF" is passed as multi_line_count
        '''
        if isinstance(to_seek, str):
            lengths = [len(to_seek)]
            to_seek = [to_seek]
        elif isinstance(to_seek, list) and all(isinstance(item, str) for item in to_seek):
            lengths = [len(item) for item in to_seek]
        else:
            raise ValueError(f"{to_seek} is not a valid parameter. Please pass a list of strings")
        
        line = self._position[0]
        if before and isinstance(multi_line_count, int):
            multi_line = line - multi_line_count
        elif not before and isinstance(multi_line_count, int):
            multi_line = line + multi_line_count

        if multi_line_count == "EOF":
            multi_line = len(self._lines) - self._position[0]
        elif multi_line_count == "BOF":
            multi_line = self._position[0]

        cursor_advance_reverse_count = 0
        found = [False]*len(to_seek)
        beginning_of_file = False
        end_of_file = False
        for i in range(len(found)):
            if before:
                while not found[i]:
                    # intial check if you already got to the beginning of file form previous searches
                    if beginning_of_file:
                        break

                    if self._current_char == to_seek[i][lengths[i]-1]:
                        beginning_of_file = self._reverse()
                        cursor_advance_reverse_count += 1
                        if beginning_of_file:
                            break

                        preempt_success = True
                        for preempt in range(lengths[i]-2 ,-1, -1):
                            cursor_advance_reverse_count += 1
                            if to_seek[i][preempt] != self._current_char:
                                preempt_success = False
                                break
                            elif preempt == 0:
                                break
                            self._reverse()
                        
                        cursor_advance_reverse_count -= 1
                        if preempt_success:
                            found[i] = True
                            break

                    elif self._current_char == ' ':
                        if ignore_space:
                            beginning_of_file = self._reverse()
                            cursor_advance_reverse_count += 1
                            if beginning_of_file:
                                break
                            elif multi_line > self._position[0]:
                                break
                        else:
                            break
                    else:
                        beginning_of_file = self._reverse()
                        cursor_advance_reverse_count += 1
                        # check again after reversing
                        if beginning_of_file:
                            break
                        # limit number of times reversing can go to newlines with multi_line_count
                        elif multi_line > self._position[0]:
                            break
            else:
                while not found[i]:
                    # intial check if you already got to the end of file form previous searches
                    if end_of_file:
                        break

                    if self._current_char == to_seek[i][0]:
                        preempt_success = True
                        for preempt in range(0, lengths[i]):
                            cursor_advance_reverse_count += 1
                            if to_seek[i][preempt] != self._current_char:
                                preempt_success = False
                                break
                            elif preempt == lengths[i]-1:
                                break
                            self._advance()
                        
                        cursor_advance_reverse_count -= 1
                        if preempt_success:
                            found[i] = True
                            break
                    elif self._current_char == ' ':
                        if ignore_space:
                            end_of_file = self._advance()
                            cursor_advance_reverse_count += 1
                            # check again after advancing
                            if end_of_file:
                                break
                            # limit number of times advancing can go to newlines with multi_line_count
                            elif multi_line < self._position[0]:
                                break
                        else:
                            break
                    else:
                        end_of_file = self._advance()
                        cursor_advance_reverse_count += 1
                        # check again after advancing
                        if end_of_file:
                            break
                        # limit number of times advancing can go to newlines with multi_line_count
                        elif multi_line < self._position[0]:
                            break
        if before:
            self._advance(cursor_advance_reverse_count)
        else:
            self._reverse(cursor_advance_reverse_count)
        return all(found)


    def _check_prev_token(self, to_check: TokenType | list[TokenType]):
        """
        Checks prev token if it has the token type/s passed. Must be on the same line
        """

        # Convert input to list
        if isinstance(to_check, TokenType):
            to_check = [to_check]
        present_flag = False
        if len(self.tokens) > 0:
            prev_token = self.tokens[-1]
            if prev_token.token in to_check and prev_token.position[0] == self._position[0]:
                present_flag = True

        return present_flag

    def print_error_logs(self):
        for error in self.errors:
            print(error)

    def _is_func_or_cwass_name(self, cwass = False, from_keyword: str = '') -> bool:
        """
        checks if the current character up to a fwunc/cwass delimiter is a proper fwunc/cwass name

        Args:
            - args: bool = determines whether to treat the current character as the beginning of a cwass name or a func name

        Returns:
            - cursor_advanced: bool = cursor will advance (`True`) if:
                - the current character up to a delimiter is a proper cwass/fwunc name and is appended to self.tokens
                - the current character up to a delimiter is an incomplete cwass/fwunc name and is appended to self.errors
                - NOTE: will return `False` if it doesn't meet these requirements (probably is an identifier name)
        """
        temp_id = from_keyword

        if cwass:
            token_type =  TokenType.CWASS
            open_paren_error = Error.CWASS_OPEN_PAREN
            invalid_name_error = Error.INVALID_CWASS_DECLARE
            missing_keyword_error = Error.MISSING_CWASS

        else:
            token_type = TokenType.FUNC_NAME
            open_paren_error = Error.FWUNC_OPEN_PAREN
            data_type_error = Error.FWUNC_DATA_TYPE            
            invalid_name_error = Error.INVALID_FUNC_DECLARE
            missing_keyword_error = Error.MISSING_FWUNC

        parentheses_exist = self._seek('(', ignore_space=False)
        dash_datatype_exist = self._seek('-', ignore_space=False)
        identifier_exists = self._seek('fwunc', before=True), self._seek('cwass', before=True)

        cursor_advanced = False
        is_end_of_file = False
        if any(identifier_exists):
            if parentheses_exist and dash_datatype_exist:
                # correct function name declaration, append to tokens
                current_line = self._position[0]

                while True:
                    if self._current_char == '-':
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        
                        if identifier_exists[0] and temp_id[0].isupper():
                            self._errors.append(GenericError(Error.FWUNC_UPPERCASE, starting_position, ending_position,
                                                            context = f"invalid function name: {temp_id}"))
                        elif identifier_exists[1] and temp_id[0].islower():
                            self._errors.append(GenericError(Error.CWASS_LOWERCASE, starting_position, ending_position,
                                                            context = f'invalid class name: {temp_id}'))
                        else:
                            self._tokens.append(Token(temp_id, token_type, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._reverse()
                        line, col = self._position
                        self._errors.append(DelimError(token_type, (line, col + 1), temp_id, '\n'))
                        break
                cursor_advanced = True

            else:
                # treat it as identifier, move cursor till an identifier delim and append to errors
                current_line = self._position[0]
                while True:
                    if self._current_char == '(' or self._current_char in DELIMS['id']:
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])

                        if not parentheses_exist:
                            # function declaration has no opening parenthesis as delimiter
                            self._errors.append(GenericError(open_paren_error, starting_position, ending_position))
                        if not dash_datatype_exist:
                            # function declaration has no datatype indicated
                            if cwass:
                                self._tokens.append(Token(temp_id, token_type, starting_position, ending_position))
                            else:
                                self._errors.append(GenericError(data_type_error, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._errors.append(GenericError(invalid_name_error, starting_position, ending_position))
                        break
                cursor_advanced = True
        
        elif parentheses_exist:
            if dash_datatype_exist:
                # correct function name declaration, append to tokens
                current_line = self._position[0]

                while True:
                    if self._current_char == '-':
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._errors.append(GenericError(missing_keyword_error, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()

                    if is_end_of_file:
                        self._reverse()
                        line, col = self._position
                        self._errors.append(DelimError(token_type, (line, col + 1), temp_id, '\n'))
                        break
            else:
                # correct funciton name call, append to token
                current_line = self._position[0]

                while True:
                    if self._current_char == '(':
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._tokens.append(Token(temp_id, token_type, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._reverse()
                        line, col = self._position
                        self._errors.append(DelimError(token_type, (line, col + 1), temp_id, '\n'))
                        break

            cursor_advanced = True
        return cursor_advanced, is_end_of_file
    
    def _is_identifier(self, from_keyword: str = '') -> bool:
        cursor_advanced = False
        temp_id = from_keyword
        current_line = self._position[0]

        while True:
            temp_id += self._current_char
            is_end_of_file = self._advance()
            in_next_line = self._position[0] != current_line

            if is_end_of_file or in_next_line:
                if in_next_line:
                    self._reverse()
                line, col = self._position
                self._errors.append(DelimError(TokenType.IDENTIFIER, (line, col + 1), temp_id, '\n'))
                cursor_advanced = True
                break

            elif self._current_char in DELIMS['id']:
                self._reverse()
                starting_position = (self._position[0], self._position[1]-len(temp_id)+1)
                ending_position = (self._position[0], self._position[1])
                
                if not any(temp_id.startswith(alpha) for alpha in ATOMS['alpha_small']):
                    self._errors.append(GenericError(Error.IDEN_INVALID_START, starting_position, ending_position,
                                                    f"'{temp_id}' is invalid"))

                # check if all characters are either alpha or numbers
                elif not temp_id.isalnum():
                    self._errors.append(GenericError(Error.IDEN_INVALID_NAME, starting_position, ending_position,
                                                    f"'{temp_id}' is invalid"))
                else:
                    self._tokens.append(Token(temp_id, TokenType.IDENTIFIER, starting_position, ending_position))

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
            is_end_of_file = self._advance()
            in_next_line = self._position[0] != current_line

            if is_end_of_file or in_next_line:
                if in_next_line:
                    self._reverse()
                starting_position = (self._position[0], self._position[1]-len(temp_string)+1)
                ending_position = (self._position[0], self._position[1])
                self._errors.append(GenericError(Error.UNCLOSED_STRING, starting_position, ending_position,
                                                context = f"'{temp_string}' is unclosed"))
                break

            elif self._current_char == '\\':
                is_end_of_file = self._advance()
                if is_end_of_file:
                    break

                if self._current_char != "|":
                    self._reverse()
                    temp_string += '\\'
                else:
                    escape_count += 1
            
            elif self._current_char in ['|', '"']:
                if self._current_char == '|':
                    token_type = token_types[0]
                    delims = DELIMS['logical_delim'] 
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
                    self._errors.append(DelimError(token_type, (ending_position[0], ending_position[1]+1), temp_string, delim))
                break

        return self._advance()
    
    def _peek_int_float_literal(self):
        original_starting_char = temp_num = self._current_char
        current_line = self._position[0]
        break_outside_loop = False

        while True:
            is_end_of_file = self._advance()
            in_next_line = self._position[0] != current_line
            if is_end_of_file or in_next_line:
                if in_next_line:
                    self._reverse()
                line, col = self._position
                self._errors.append(DelimError(TokenType.INT_LITERAL, (line, col + 1), temp_num, '\n'))
                break

            # preemptively break when a delimiter is found for integers 
            if self._current_char in DELIMS['int_float']:
                self._reverse()
                corrected_value = temp_num
                starting_position = (self._position[0], self._position[1]-len(temp_num)+1)
                ending_position = (self._position[0], self._position[1])

                if original_starting_char == '0':
                    # only floats or literal '0' can start with 0
                    if len(temp_num) > 1:
                        corrected_value = str(int(temp_num))
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_num)+1])
                        ending_position = tuple(self._position)
                        self._errors.append(IntFloatWarning(Warn.LEADING_ZEROES_INT, corrected_value, temp_num, starting_position, ending_position))

                if len(corrected_value) > 10:
                    self._errors.append(GenericError(Error.OUT_OF_BOUNDS_INT_FLOAT, starting_position, ending_position,
                                                    context = f"'{corrected_value}' is {len(corrected_value)} digits long"))
                    break

                self._tokens.append(Token(corrected_value, TokenType.INT_LITERAL, starting_position, ending_position))
                break

            # floats with one leading zero
            elif self._current_char == '.':
                temp_num += self._current_char
                while True:
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._reverse()
                        line, col = self._position
                        self._errors.append(DelimError(TokenType.FLOAT_LITERAL, (line, col + 1), temp_num, '\n'))
                        break_outside_loop = True
                        break

                    # preemptively break when a delimiter is found for floats
                    if self._current_char in DELIMS['int_float']:
                        self._reverse()
                        corrected_value = temp_num
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_num)+1])
                        ending_position = tuple(self._position)

                        # has trailing zero but not the only trailing zero
                        if temp_num[-1:] == '0' and not temp_num[-2:-1] == '.':
                            corrected_value = str(float(temp_num))
                            starting_position = tuple([self._position[0], self._position[1]-len(temp_num)+1])
                            ending_position = tuple(self._position)
                            self._errors.append(IntFloatWarning(Warn.TRAILING_ZEROES_FLOAT, corrected_value, temp_num, starting_position, ending_position))

                        # has no numbers after decimal point
                        if temp_num[-1:] == '.':
                            corrected_value = temp_num + '0'
                            starting_position = tuple([self._position[0], self._position[1]-len(temp_num)+1])
                            ending_position = tuple(self._position)
                            self._errors.append(IntFloatWarning(Warn.MISSING_TRAILING_ZERO_FLOAT, corrected_value, temp_num, starting_position, ending_position))

                        # has multiple decimal points
                        decimal_point_count = corrected_value.count('.')
                        if decimal_point_count > 1:
                            self._errors.append(GenericError(Error.MULTIPLE_DECIMAL_POINT, starting_position, ending_position,
                                                            context = f"'{corrected_value}' has {decimal_point_count} decimal points"))
                            break_outside_loop = True
                            break

                        before_decimal_digit_count = len(corrected_value[:corrected_value.index('.')])
                        if before_decimal_digit_count > 10:
                            self._errors.append(GenericError(Error.OUT_OF_BOUNDS_INT_FLOAT, starting_position, ending_position,
                                                            context = f"'{corrected_value}' is {len(corrected_value)} digits long"))
                            break_outside_loop = True
                            break
                        
                        after_decimal_digit_count = len(corrected_value[corrected_value.index('.')+1:])
                        if after_decimal_digit_count > 10:
                            temp_num = corrected_value
                            corrected_value = corrected_value[:corrected_value.index('.')] + corrected_value[corrected_value.index('.'):][:11]
                            self._errors.append(IntFloatWarning(Error.OUT_OF_BOUNDS_INT_FLOAT, corrected_value, temp_num, starting_position, ending_position,
                                                                context = f"'{temp_num}' is {len(temp_num)} digits long after the decimal point\n\tvalue = '{temp_num}' --> corrected valule = '{corrected_value}'"))

                        self._tokens.append(Token(corrected_value, TokenType.FLOAT_LITERAL, starting_position, ending_position))
                        break_outside_loop = True
                        break

                    temp_num += self._current_char

                if break_outside_loop:
                    break

            # treat as invalid identifier if followed by non-number
            if self._current_char not in ATOMS['number']:
                cursor_advanced, _ = self._is_func_or_cwass_name(temp_num)
                if cursor_advanced:
                    break
                else:
                    # make temp_id to hold read chars
                    cursor_advanced, _ = self._is_identifier(temp_num)
                    if cursor_advanced:
                        break

            temp_num += self._current_char

        return self._advance()
    
    def _peek_comments(self, multiline: bool = False) -> bool:
        'returns true if found comments/error about comments, false otherwise'
        to_seek = r'>//<' if multiline else '>.<'
        comment_indicator_exists = self._seek(to_seek)

        current_line = self._position[0]
        cursor_advanced = False
        is_end_of_file = True

        if comment_indicator_exists:
            if multiline:
                starting_position = self._position.copy()
                is_end_of_file = self._advance(len(to_seek) - 1)
                temp_comment = to_seek

                closing_comment_indicator_exists = self._seek(to_seek, multi_line_count='EOF')
                if closing_comment_indicator_exists:
                    # keep appending until found >//< in order
                    while True:
                        current_line = self._position[0]
                        is_end_of_file = self._advance()

                        # !TODO! CHANGE AFTER ADDING \n TO EVERY LINE (just remove it lul)
                        if self._position[0] > current_line:
                            temp_comment += '\n'
                        temp_comment += self._current_char

                        if self._current_char == '/' and self._lines[self._position[0]][self._position[1]+1] == '/' and self._lines[self._position[0]][self._position[1]+2] == '<':
                            self._advance(3)
                            temp_comment += '/<'

                            ending_position = self._position.copy()
                            self._tokens.append(Token(temp_comment, TokenType.MULTI_LINE_COMMENT, starting_position, ending_position))
                            break

                else:
                    # comment out the rest of the code if there is no closing indicator is 
                    while not is_end_of_file:
                        current_line = self._position[0]
                        is_end_of_file = self._advance()

                        # !TODO! CHANGE AFTER ADDING \n TO EVERY LINE (just remove it lul)
                        if self._position[0] > current_line:
                            temp_comment += '\n'
                        if not is_end_of_file:
                            temp_comment += self._current_char

                        if is_end_of_file:
                            ending_position = self._position.copy()
                            self._errors.append(GenericWarning(Warn.UNCLOSED_MULTI_LINE_COMMENT, starting_position))
                            self._tokens.append(Token(temp_comment, TokenType.MULTI_LINE_COMMENT, starting_position, ending_position))

            else:
                temp_comment = to_seek
                starting_position = self._position.copy()
                is_end_of_file = self._advance(len(to_seek) - 1)
                while True:
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] > current_line
                    if not is_end_of_file and not in_next_line:
                        temp_comment += self._current_char

                    # !TODO! CHANGE AFTER ADDING \n TO EVERY LINE
                    # new implementation could be looking at line length-2 and if character there is \n, that's newline 
                    # every other \n will be treated as a comment
                    if is_end_of_file or in_next_line:
                        ending_position = self._position.copy()
                        self._tokens.append(Token(temp_comment, TokenType.SINGLE_LINE_COMMENT, starting_position, ending_position))
                        break


            cursor_advanced = True
        else:
            cursor_advanced = False

        return cursor_advanced, is_end_of_file


"""
def read_file(file_path: Path) -> list[str]:
    with open(file_path, 'r') as file:
        lines = [line for line in file]

    return lines
"""
def print_lex(source_code: list[str]):
    print('\nsample text file')
    print("_"*20)
    for i, line in enumerate(source_code):
        print(f"{i} | {line}")
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

if __name__ == "__main__":
    # file_path = argv[1]
    # source_code = read_file(file_path)
    source_code = [
        "a  fwunc aquachan(~",
        # 'aqua-chan(args)~',
        ' aqua-chan',
        'aqua',
        'aqua-chan = cap~',
        'bweak~ bweak',
        'shion-chan~ojou~'
    ]
    print_lex(source_code)
    
