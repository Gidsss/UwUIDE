from verify_delim import verify_delim
from move_cursor import advance_cursor, reverse_cursor

from constants.constants import *
from ..token import *
from ..error_handler import *

def reserved(context: tuple[list[str], list[int], str], tokens: list[Token], logs: list[DelimError],
          to_check: str, token_type: TokenType, before: bool = False, ignore_space: bool = False) -> tuple[bool,bool,str]:
    '''
    returns
    1. if cursor moved (token was appended to either tokens or logs)
    2. if end of file 
    3. current character

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
    lines, position, current_char = context

    length = len(to_check)
    line, column = position

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
                if lines[line][j] == " ":
                    continue
                if to_check[i] != lines[line][j]:
                    is_equal = False
                    break
                i -= 1
                j -= 1
        else:
            while (i < end[0]) and (j < end[1]):
                if lines[line][j] == " ":
                    continue
                if to_check[i] != lines[line][j]:
                    is_equal = False
                    break
                i += 1
                j += 1
    else:
        for i,j in zip(range(start[0], end[0], increment), range(start[1], end[1], increment)):
            if j >= len(lines[line]) or to_check[i] != lines[line][j]:
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
            current_char = advance_cursor(context, end[1]-column-1)
            
        lexeme = to_check
        next_char_is_correct_delim, delim = verify_delim(context, token_type.expected_delims)
        if next_char_is_correct_delim:
            tokens.append(Token(lexeme, token_type, starting_position, ending_position))
        else:
            is_end_of_file, current_char = advance_cursor(context)
            # preemptively check if the lexeme or current character is not valid to be in a fwunc/cwass/identifier name
            in_new_line = position[0] != line
            if not any(char in ATOMS['alphanum'] for char in lexeme) or not current_char in ATOMS['alphanum'] or in_new_line:
                current_char = reverse_cursor(context)
                line, col = ending_position
                logs.append(DelimError(token_type, (line, col + 1), lexeme, delim))
            else:
                # check if identifier
                is_end_of_file, current_char = identifier(from_keyword=to_check)
        
        is_end_of_file, current_char = advance_cursor(context)
        cursor_advanced = True

    else:
        cursor_advanced = False

    return cursor_advanced, is_end_of_file, current_char