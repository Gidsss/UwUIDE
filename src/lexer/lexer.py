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
                cursor_advanced, is_end_of_file = self._peek("bweak", TokenType.BWEAK)
                if cursor_advanced:
                    continue

            if self._current_char == 'c':
                cursor_advanced, is_end_of_file = self._peek('chan', TokenType.CHAN)
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek('cap', TokenType.BOOL_LITERAL)
                if cursor_advanced:
                    continue

            if self._current_char == 'f':
                cursor_advanced, is_end_of_file = self._peek("fwunc", TokenType.FWUNC)
                if cursor_advanced:
                    continue
            
            if self._current_char == '-':
                # check if unary first
                cursor_advanced, is_end_of_file = self._peek('--', TokenType.UNARY)
                if cursor_advanced:
                    continue
                
                # check if minus
                # check if negative

                # if ID_DELIM
                starting_position = ending_position = tuple(self._position)
                self._tokens.append(Token('-', 'ID_DELIM', starting_position, ending_position))                
                is_end_of_file = self._advance()
                continue

            if self._current_char == '~':
                # always append '~' but check delims anyway
                cursor_advanced, is_end_of_file = self._peek('~', TokenType.TERMINATOR)
                if cursor_advanced:
                    continue

            # can be identifiers or function names
            if self._current_char.isalpha():
                cursor_advanced = self._is_func_name()
                if cursor_advanced:
                    if is_end_of_file:
                        break
                    is_end_of_file = self._advance()
                    continue

                else:
                    # make temp_id to hold read chars
                    temp_id = ""
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
                            break

                        elif self._current_char in DELIMS['id']:
                            self._reverse()
                            starting_position = (self._position[0], self._position[1]-len(temp_id)+1)
                            ending_position = (self._position[0], self._position[1])
                            self._tokens.append(Token(temp_id, TokenType.IDENTIFIER, starting_position, ending_position))
                            break

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
                line, col = ending_position
                self._errors.append(DelimError(token_type, (line, col+1), lexeme, delim))
            
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
        if before:
            multi_line = line - multi_line_count
        else:
            multi_line = line + multi_line_count

        if multi_line_count == "EOF":
            multi_line = len(self._lines) - line - 1
        elif multi_line_count == "BOF":
            multi_line = 0

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
                        if beginning_of_file:
                            break

                        cursor_advance_reverse_count += 1
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
                                cursor_advance_reverse_count -= 1
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
                            cursor_advance_reverse_count -= 1
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
                                cursor_advance_reverse_count -= 1
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
                            cursor_advance_reverse_count -= 1
                            break
                        # limit number of times advancing can go to newlines with multi_line_count
                        elif multi_line < self._position[0]:
                            break

        if before:
            self._advance(cursor_advance_reverse_count)
        else:
            self._reverse(cursor_advance_reverse_count)

        return all(found)


    def print_error_logs(self):
        for error in self.errors:
            print(error)

    def _is_func_name(self) -> bool:
        """
        check if not a valid function name by looking for fwunc before the current character but parenthesis don't exist after don't
            throw error if so
            eg. fwunc aqua-chan~
        check if function again by looking if there is '(' after
            if '(', is a function name
            eg. calling: aqua(args)~
        check if function by looking for fwunc before the current characer
            if 'fwunc', is a function name
            eg. declaring: fwunc aqua-chan(params)~
        else is literal
        """
        parentheses_exist = self._seek('(', ignore_space=False)
        dash_datatype_exist = self._seek('-', ignore_space=False)
        fwunc_exists = self._seek('fwunc', before=True)
        
        cursor_advanced = False
        if fwunc_exists:
            if parentheses_exist and dash_datatype_exist:
                # correct function name declaration, append to tokens
                temp_id = ""
                current_line = self._position[0]

                while True:
                    if self._current_char == '-':
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._tokens.append(Token(temp_id, TokenType.FUNC_NAME, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._reverse()
                        line, col = self._position
                        self._errors.append(DelimError(TokenType.FUNC_NAME, (line, col + 1), temp_id, '\n'))
                        break
                cursor_advanced = True

            else:
                if not parentheses_exist:
                    # function declaration has no opening parenthesis as delimiter
                    self._errors.append(CustomError(Error.OPEN_PAREN_FUNC, tuple(self._position)))
                if not dash_datatype_exist:
                    # function declaration has no datatype indicated
                    self._errors.append(CustomError(Error.DATA_TYPE_FUNC, tuple(self._position)))
                
                # treat it as identifier, move cursor till an identifier delim and append to errors
                temp_id = ""
                current_line = self._position[0]

                while True:
                    if self._current_char in DELIMS['id']:
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._errors.append(CustomError(Error.INVALID_FUNC_DECLARE, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._errors.append(CustomError(Error.INVALID_FUNC_DECLARE, starting_position, ending_position))
                        break
                cursor_advanced = True
        
        elif parentheses_exist:
            if dash_datatype_exist:
                # correct function name declaration, append to tokens
                temp_id = ""
                current_line = self._position[0]

                while True:
                    if self._current_char == '-':
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._errors.append(CustomError(Error.MISSING_FWUNC, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()

                    if is_end_of_file:
                        self._reverse()
                        line, col = self._position
                        self._errors.append(DelimError(TokenType.FUNC_NAME, (line, col + 1), temp_id, '\n'))
                        break
            else:
                # correct funciton name call, append to token
                temp_id = ""
                current_line = self._position[0]

                while True:
                    if self._current_char == '(':
                        self._reverse()
                        starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                        ending_position = tuple([self._position[0], self._position[1]])
                        self._tokens.append(Token(temp_id, TokenType.FUNC_NAME, starting_position, ending_position))
                        break

                    temp_id += self._current_char
                    is_end_of_file = self._advance()
                    in_next_line = self._position[0] != current_line

                    if is_end_of_file or in_next_line:
                        if in_next_line:
                            self._reverse()
                        line, col = self._position
                        self._errors.append(DelimError(TokenType.FUNC_NAME, (line, col + 1), temp_id, '\n'))
                        break

            cursor_advanced = True
        
        return cursor_advanced
    
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
                self._errors.append(CustomError(Error.UNCLOSED_STRING, starting_position, ending_position,
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
        original_starting_char = temp_num =  self._current_char
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
                    self._errors.append(CustomError(Error.OUT_OF_BOUNDS_INT_FLOAT, starting_position, ending_position,
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
                            self._errors.append(CustomError(Error.MULTIPLE_DECIMAL_POINT, starting_position, ending_position,
                                                            context = f"'{corrected_value}' has {decimal_point_count} decimal points"))
                            break_outside_loop = True
                            break

                        before_decimal_digit_count = len(corrected_value[:corrected_value.index('.')])
                        if before_decimal_digit_count > 10:
                            self._errors.append(CustomError(Error.OUT_OF_BOUNDS_INT_FLOAT, starting_position, ending_position,
                                                            context = f"'{corrected_value}' is {len(corrected_value)} digits long"))
                            break_outside_loop = True
                            break
                        
                        after_decimal_digit_count = len(corrected_value[corrected_value.index('.')+1:])
                        if after_decimal_digit_count > 10:
                            self._errors.append(IntFloatWarning(Error.OUT_OF_BOUNDS_INT_FLOAT, corrected_value, temp_num, starting_position, ending_position,
                                                                context = f"'{corrected_value}' is {len(corrected_value)} digits long after the decimal point"))

                        self._tokens.append(Token(corrected_value, TokenType.FLOAT_LITERAL, starting_position, ending_position))
                        break_outside_loop = True
                        break

                    temp_num += self._current_char

                if break_outside_loop:
                    break

            temp_num += self._current_char

        return self._advance()
        

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
    print("\n\n","#"*30,"\nlexeme\ttoken\t\trange")
    for token in x.tokens:
        print(f"{token.lexeme}", end="\t")
        print(f"{token.token}", end="\t")
        print(f"{token.position} - {token.end_position}", end="\t")
        print()

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
    