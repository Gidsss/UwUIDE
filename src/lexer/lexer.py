from sys import argv
from pathlib import Path
from typing import NamedTuple
from .error_handler import *

ATOMS = {
    'num': ['1','2','3','4','5','6','7','8','9'],
    'number': ['0','1','2','3','4','5','6','7','8','9'],
    'alpha': [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ],
}

DELIMS = {
    'end': ['~'],
    'data_type': [',', '(', ')', ' ', '~', '='],
    'bool': [',', ' ', '}', ')', '~'],
    'line': [None],
    'assign_delim': [*ATOMS['number'], *ATOMS['alpha'], '{', ' ', '-' '('],
    'logical_delim': ['"', *ATOMS['number'], *ATOMS['alpha'], ' ', '-', '('],
    'id': [' ', '~', ',', '(', ')', '[', ']', '{', '}', '+', '-', '*', r'/', r'%', '.', '!' ,'&', '|' , '>', '<', '='],
    'operator': [*ATOMS['alpha'], *ATOMS['number'], ' ', '-', '('],
    'unary': ['~', '(']

}

class Token(NamedTuple):
    lexeme: str
    token: str
    position: tuple[int,int]
    end_position: tuple[int,int]

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
                cursor_advanced, is_end_of_file = self._peek(
                    "bweak", "RESERVED_WORD",
                    'end',
                    ErrorType.BWEAK
                )
                if cursor_advanced:
                    continue

            if self._current_char == 'c':
                cursor_advanced, is_end_of_file = self._peek(
                    'chan', 'INT_DATA_TYPE',
                    'data_type',
                    ErrorType.DATA_TYPE
                )
                if cursor_advanced:
                    continue

                cursor_advanced, is_end_of_file = self._peek(
                    'cap', 'BOOLEAN_VALUE',
                    'bool',
                    ErrorType.BOOL
                )

                if cursor_advanced:
                    continue
            
            if self._current_char == '-':
                # check if unary first
                cursor_advanced, is_end_of_file = self._peek(
                    '--', 'UNARY_OPERATOR',
                    'unary',
                    ErrorType.UNARY
                )
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
                # always append '~'
                starting_position = ending_position = tuple(self._position)
                self._tokens.append(Token('~', 'LINE_BREAK', starting_position, ending_position))                
                is_end_of_file = self._advance()
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

                            starting_position = tuple([self._position[0], self._position[1]-len(temp_id)-1])
                            ending_position = tuple([self._position[0], self._position[1]])
                            self._tokens.append(Token(temp_id, "IDENTIFIER", starting_position, ending_position))
                            break

                        temp_id += self._current_char
                        is_end_of_file = self._advance()

                        if is_end_of_file or self._position[0] != current_line:
                            self._reverse()
                            line, col = self._position
                            self._errors.append(Error(ErrorType.ID, (line, col + 1), temp_id, DELIMS['id'], r'\n'))
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

    def _peek(self, to_check: str, token: str,
              delim_id: str, error_type: str,
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
                if to_check[i] != self._lines[line][j]:
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
            next_char_is_correct_delim, delim = self._verify_delim(DELIMS[delim_id])
            if next_char_is_correct_delim:
                self._tokens.append(Token(lexeme, token, starting_position, ending_position))
            else:
                line, col = ending_position
                self._errors.append(Error(error_type, (line, col+1), lexeme, DELIMS[delim_id], delim))
            
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
    