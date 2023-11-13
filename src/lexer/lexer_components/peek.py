from .verify_delim import verify_delim
from .move_cursor import advance_cursor, reverse_cursor

from constants.constants import *
from ..token import *
from ..error_handler import *

def reserved(to_check: str, token_type: TokenType, 
             context: tuple[list[str], list[int], str, list[Token], list[DelimError]],
             before: bool = False, ignore_space: bool = False) -> tuple[bool,bool,str]:
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
    lines, position, current_char, tokens, logs = context

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

            is_end_of_file, current_char = advance_cursor(context, end[1]-column-1)
            context = lines, position, current_char, tokens, logs
            
        lexeme = to_check
        next_char_is_correct_delim, delim = verify_delim(context, token_type.expected_delims)
        if next_char_is_correct_delim:
            tokens.append(Token(lexeme, token_type, starting_position, ending_position))
        else:
            is_end_of_file, current_char = advance_cursor(context)
            context = lines, position, current_char, tokens, logs

            # preemptively check if the lexeme or current character is not valid to be in a fwunc/cwass/identifier name
            in_new_line = position[0] != line
            if not any(char in ATOMS['alphanum'] for char in lexeme) or not current_char in ATOMS['alphanum'] or in_new_line:
                _, current_char = reverse_cursor(context)
                context = lines, position, current_char, tokens, logs

                line, col = ending_position
                logs.append(DelimError(token_type, (line, col + 1), lexeme, delim))
            else:
                # check if identifier
                is_end_of_file, current_char = identifier(context, from_keyword=to_check)
                context = lines, position, current_char, tokens, logs

        is_end_of_file, current_char = advance_cursor(context)
        cursor_advanced = True

    else:
        cursor_advanced = False

    return cursor_advanced, is_end_of_file, current_char


def identifier(context: tuple[list[str], list[int], str, list[Token], list[DelimError]],
               from_keyword: str = None, cwass: bool = False) -> tuple[bool, str]:
    lines, position, current_char, tokens, logs = context

    temp_id = from_keyword if from_keyword else ''
    current_line = position[0]

    if cwass:
        expected_delims = DELIMS['cwass']
        unique_token = UniqueTokenType.CWASS
        delim_error_token = TokenType.GEN_CWASS_NAME
    else:
        expected_delims = DELIMS['id'] 
        unique_token = UniqueTokenType.ID 
        delim_error_token = TokenType.GEN_IDENTIFIER

    while True:
        temp_id += current_char
        is_end_of_file, current_char = advance_cursor(context)
        context = lines, position, current_char, tokens, logs

        in_next_line = position[0] != current_line

        if is_end_of_file or in_next_line:
            if in_next_line:
                _, current_char = reverse_cursor(context)
                context = lines, position, current_char, tokens, logs

            line, col = position
            logs.append(DelimError(TokenType.GEN_IDENTIFIER, (line, col + 1), temp_id, '\n'))
            cursor_advanced = True
            break

        elif current_char in expected_delims:
            _, current_char = reverse_cursor(context)
            context = lines, position, current_char, tokens, logs

            starting_position = (position[0], position[1]-len(temp_id)+1)
            ending_position = (position[0], position[1])
            tokens.append(Token(temp_id, UniqueTokenType(temp_id, unique_token),
                                            starting_position, ending_position))
            break

        elif not current_char.isalnum():
            special_char = current_char

            _, current_char = reverse_cursor(context)
            context = lines, position, current_char, tokens, logs

            line, col = position
            logs.append(DelimError(delim_error_token, (line, col + 1), temp_id, special_char))
            break
    
    context = lines, position, current_char
    is_end_of_file, current_char = advance_cursor(context)
    return is_end_of_file, current_char


def comments(context: tuple[list[str], list[int], str, list[Token], list[DelimError]],
             multiline: bool = False) -> bool:
    'returns true if found comments/error about comments, false otherwise'
    lines, position, current_char, tokens, logs = context
    to_seek = r'>//<' if multiline else '>.<'
    comment_indicator_exists = seek(to_seek, include_current=True)

    current_line = position[0]
    cursor_advanced = False
    is_end_of_file = True

    if comment_indicator_exists:
        if multiline:
            starting_position = tuple(position)
            is_end_of_file, current_char = advance_cursor(context, len(to_seek)-1)
            context = lines, position, current_char, tokens, logs
            temp_comment = to_seek

            closing_comment_indicator_exists = seek(to_seek, multi_line_count='EOF')
            if closing_comment_indicator_exists:
                # keep appending until found >//< in order
                while True:
                    current_line = position[0]
                    is_end_of_file, current_char = advance_cursor(context)
                    context = lines, position, current_char, tokens, logs

                    if position[0] > current_line:
                        temp_comment += '\n'
                    temp_comment += current_char

                    if current_char == '/' and lines[position[0]][position[1]+1] == '/' and lines[position[0]][position[1]+2] == '<':
                        is_end_of_file, current_char = advance_cursor(context, 3)
                        context = lines, position, current_char, tokens, logs
                        temp_comment += '/<'

                        ending_position = tuple(position)
                        tokens.append(Token(temp_comment, TokenType.MULTI_LINE_COMMENT, starting_position, ending_position))
                        break

            else:
                # comment out the rest of the code if there is no closing indicator is 
                while not is_end_of_file:
                    current_line = position[0]
                    is_end_of_file, current_char = advance_cursor(context)
                    context = lines, position, current_char, tokens, logs

                    if position[0] > current_line:
                        temp_comment += '\n'
                    if not is_end_of_file:
                        temp_comment += current_char

                    if is_end_of_file:
                        ending_position = tuple(position)
                        logs.append(GenericWarning(Warn.UNCLOSED_MULTI_LINE_COMMENT, starting_position))
                        tokens.append(Token(temp_comment, TokenType.MULTI_LINE_COMMENT, starting_position, ending_position))

        else:
            temp_comment = to_seek
            starting_position = tuple(position)
            is_end_of_file, current_char = advance_cursor(context, len(to_seek)-1)
            context = lines, position, current_char, tokens, logs

            while True:
                is_end_of_file, current_char = advance_cursor(context)
                context = lines, position, current_char, tokens, logs

                in_next_line = position[0] > current_line
                if not is_end_of_file and not in_next_line:
                    temp_comment += current_char

                if is_end_of_file or in_next_line:
                    ending_position = tuple(position)
                    tokens.append(Token(temp_comment, TokenType.SINGLE_LINE_COMMENT, starting_position, ending_position))
                    break


        cursor_advanced = True
    else:
        cursor_advanced = False

    return cursor_advanced, is_end_of_file, current_char