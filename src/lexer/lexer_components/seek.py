from .move_cursor import advance_cursor, reverse_cursor

from constants.constants import *
from ..token import *
from ..error_handler import *

def seek(context: tuple[list[str], list[int], str, list[Token], list[DelimError]],
          to_seek: str|list[str], before: bool = False, multi_line_count: int|str = 0,
          ignore_space = True, max_space_count: int = None, alphanum_only: bool = False,
          include_current: bool = False) -> bool:
    '''
    seeks concatenated characters ('ab') or multiple separate characters (['a', 'b']) in order;

    can search through multi lines but line count should be indicated

    can go until end|beginning of file if "EOF|BOF" is passed as multi_line_count
    '''
    lines, position, current_char, tokens, logs = context

    if isinstance(to_seek, str):
        to_seek = [to_seek]
        
    line = position[0]
    if before and isinstance(multi_line_count, int):
        multi_line = line - multi_line_count
    elif not before and isinstance(multi_line_count, int):
        multi_line = line + multi_line_count

    if multi_line_count == "EOF":
        multi_line = len(lines) - 1
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
                file_out_of_bounds, current_char = reverse_cursor(context)
                context = lines, position, current_char, tokens, logs
            else:
                file_out_of_bounds, current_char = advance_cursor(context)
                context = lines, position, current_char, tokens, logs
            cursor_advance_reverse_count += 1

        while not found[i]:
            preempt_start_char_index = len(to_seek[i])-1 if before else 0
            # intial check if you already got to the beginning or end of file form previous searches
            if file_out_of_bounds:
                break
            
            # limit number of times reversing can go to newlines with multi_line_count
            if is_max_multi_line is None:
                is_max_multi_line = multi_line > position[0] if before else multi_line < position[0]

            if is_max_multi_line:
                cursor_advance_reverse_count -= 1
                if before:
                    _, current_char = advance_cursor(context)
                    context = lines, position, current_char, tokens, logs
                else:
                    _, current_char = reverse_cursor(context)
                break
            
            if current_char == to_seek[i][preempt_start_char_index]:
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
                        file_out_of_bounds, current_char = reverse_cursor(context)
                        context = lines, position, current_char, tokens, logs
                    else:
                        file_out_of_bounds, current_char = advance_cursor(context)
                        context = lines, position, current_char, tokens, logs
                    cursor_advance_reverse_count += 1

                    is_max_multi_line = multi_line > position[0] if before else multi_line < position[0]
                    # limit number of times reversing can go to newlines with multi_line_count
                    if is_max_multi_line or file_out_of_bounds:
                        preempt_success = False
                        cursor_advance_reverse_count -= 1
                        if before:
                            _, current_char = advance_cursor(context)
                            context = lines, position, current_char, tokens, logs
                        else:
                            _, current_char = reverse_cursor(context)
                            context = lines, position, current_char, tokens, logs
                        break

                    # don't check for last character (not included in to_seek)
                    elif preempt == last_iter and not preempt_success:
                        preempt_success = False
                        break
                    elif to_seek[i][preempt] != current_char:
                        preempt_success = False
                        break

                if preempt_success:
                    found[i] = True
                    break

            elif current_char == ' ':
                if ignore_space:
                    space_count += 1
                    if max_space_count and space_count > max_space_count:
                        break

                    cursor_advance_reverse_count += 1
                    if before:
                        file_out_of_bounds, current_char = reverse_cursor(context)
                        context = lines, position, current_char, tokens, logs
                    else:
                        file_out_of_bounds, current_char = advance_cursor(context)
                        context = lines, position, current_char, tokens, logs
                    if file_out_of_bounds:
                        break

                    is_max_multi_line = multi_line > position[0] if before else multi_line < position[0]
                    if is_max_multi_line:
                        cursor_advance_reverse_count -= 1
                        if before:
                            _, current_char = advance_cursor(context)
                            context = lines, position, current_char, tokens, logs
                        else:
                            _, current_char = reverse_cursor(context)
                            context = lines, position, current_char, tokens, logs
                        break
                else:
                    break

            elif alphanum_only and current_char not in ATOMS['alphanum']:
                break

            else:
                if before:
                    file_out_of_bounds, current_char = reverse_cursor(context)
                    context = lines, position, current_char, tokens, logs
                else:
                    file_out_of_bounds, current_char = advance_cursor(context)
                    context = lines, position, current_char, tokens, logs
                cursor_advance_reverse_count += 1
                # check again after reversing
                if file_out_of_bounds:
                    break
                
                is_max_multi_line = multi_line > position[0] if before else multi_line < position[0]
                if is_max_multi_line:
                    cursor_advance_reverse_count -= 1
                    if before:
                        _, current_char = advance_cursor(context)
                        context = lines, position, current_char, tokens, logs
                    else:
                        _, current_char = reverse_cursor(context)
                        context = lines, position, current_char, tokens, logs
                    break
    if before:
        current_char = advance_cursor(context, cursor_advance_reverse_count)
    else:
        current_char = reverse_cursor(context, cursor_advance_reverse_count)
    return all(found)