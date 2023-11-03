from sys import argv
from pathlib import Path

from constants.constants import DELIMS
from .token import Token, TokenType
from .error_handler import Error


class Lexer():
    'description'

    def __init__(self, source_code: list[str]):
        self._lines = source_code

        self._position = [0,0]
        self._current_char = self._lines[self._position[0]][self._position[1]]

        self._nest_level = 0

        self._tokens: list[Token] = []
        self._errors: list[Error] = []

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
                # cursor_advanced, is_end_of_file = self._peek('fwunc', TokenType.FWUNC)
                # if cursor_advanced:
                #     continue

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
            if self._current_char.isalpha():
                cursor_advanced = self._is_func_name()
                if cursor_advanced:
                    continue

                else:
                    # make temp_id to hold read chars
                    temp_id = ""
                    current_line = self._position[0]

                    while True:
                        if self._current_char in DELIMS['id']:
                            self._reverse()

                            starting_position = tuple([self._position[0], self._position[1]-len(temp_id)+1])
                            ending_position = tuple([self._position[0], self._position[1]])
                            self._tokens.append(Token(temp_id, TokenType.IDENTIFIER, starting_position, ending_position))
                            break

                        temp_id += self._current_char
                        is_end_of_file = self._advance()

                        if is_end_of_file or self._position[0] != current_line:
                            self._reverse()
                            line, col = self._position
                            self._errors.append(Error(TokenType.IDENTIFIER, (line, col + 1), temp_id, r'\n'))
                            break
            
            if is_end_of_file:
                break
            is_end_of_file = self._advance()
    
    def _advance(self, increment: int = 1) -> bool:        
        # initial check if EOF already
        end_of_file = self._position[0] >= len(self._lines)
        if end_of_file:
            self._current_char = None
            return True
        
        # increment cursor
        # go to next line first char if out of bounds in current line (index 'length+1')
        self._position[1] += increment
        current_line_length = len(self._lines[self._position[0]])
        while self._position[1] >= current_line_length:
            self._position[1] -= current_line_length
            self._position[0] += 1

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
        beginning_of_file = self._position == [0,0]
        if beginning_of_file:
            self._current_char = self._lines[self._position[0]][self._position[1]]
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
            
    def _verify_delim(self, delim_list: list[str], current = False) -> tuple[bool, str]:
        if delim_list == [None]:
            return True, None

        line, column = self._position

        if current:
            next_char = self._lines[line][column]
        elif column+1 >= len(self._lines[line]):
            next_char = r'\n'
        else:
            next_char = self._lines[line][column+1]

        for delim in delim_list:
            start = (0, column)
            end = (len(delim), column + len(delim))

            is_delim = True
            for i in range(len(delim)):
                if i >= len(next_char):
                    is_delim = False
                    break

                if delim[i] != next_char[i]:
                    is_delim = False
                    break

            if is_delim:
                break
            
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
                self._errors.append(Error(token_type, (line, col+1), lexeme, delim))
            
            is_end_of_file = self._advance()
            cursor_advanced = True

        else:
            cursor_advanced = False

        return cursor_advanced, is_end_of_file
    
    def _seek(self, to_seek: str|list[str], before: bool = False, multi_line_count: int|str = 0) -> bool:
        '''
        seeks multiple characters ('ab') or multiple sets of characters (['a', 'b']) in order;

        can seek through multi lines but line count should be indicated

        can go until end of file if "EOF" is passed as multi_line_count
        '''
        pass

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
        cursor_advanced = False

        parentheses_exist = self._seek(['(', ')'])
        fwunc_exists = self._seek('fwunc', before=True)

        if fwunc_exists and not parentheses_exist:
            # throw error
            # unterminated function name or whatever
            cursor_advanced = True

        elif parentheses_exist:
            # treat as function name
            # check delimiter
            # append
            cursor_advanced = True

        if fwunc_exists:
            # treat as function name
            # check delimiter
            # append
            cursor_advanced = True
        
        return cursor_advanced

    def _is_literal(self) -> bool:
        # !NOTE! might be redundant with method above

        # check if id delim is present after
        # if id delim: is literal
        # else false
        pass

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
        "bweak",
        ' aqua-chan',
        'aqua',
        'aqua-chan = cap~',
        'bweak~ bweak',
        'shion-chan~ojou~'
    ]
    print_lex(source_code)
    