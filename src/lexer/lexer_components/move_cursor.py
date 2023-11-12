def advance(context: tuple[list[str], list[int], str], increment: int = 1) -> bool:
    lines, position, current_char = context

    # initial check if EOF already
    temp_position = position[1]
    temp_position += increment
    end_of_file = temp_position > len(lines[len(lines)-1])-1 and position[0] == len(lines)-1
    if end_of_file:
        position[1] += increment
        current_char = None
        return True, current_char
    
    # increment cursor
    # go to next line first char if out of bounds in current line (index 'length+1')
    position[1] += increment
    current_line_length = len(lines[position[0]])
    while position[1] >= current_line_length:
        position[1] -= current_line_length
        position[0] += 1
        current_line_length = len(lines[position[0]])
    
    # check if EOF after incrementing
    # if not EOF, read current character since we're sure we are not out of bounds otherwise due to previous check
    end_of_file = position[0] >= len(lines)

    current_char = lines[position[0]][position[1]] if not end_of_file else None
    return end_of_file, current_char

def reverse(context: tuple[list[str], list[int], str], increment: int = 1) -> bool:
    lines, position, current_char = context

    # initial check if BOF already
    temp_position = position[1]
    temp_position -= increment
    beginning_of_file = temp_position < 0 and position[0] == 0
    if beginning_of_file:
        position[1] -= increment
        current_char = None
        return True, current_char
    
    # decrement cursor
    # go to previous line last char if out of bounds in current line (index '-1')
    position[1] -= increment
    while position[1] < 0:
        position[0] -= 1
        current_line_length = len(lines[position[0]])
        position[1] += current_line_length

    # assign current char since we're sure we are not out of bounds
    current_char = lines[position[0]][position[1]]

    # check if BOF after decrementing, return true if so
    beginning_of_file = position == [0,0]

    current_char = lines[position[0]][position[1]] if not beginning_of_file else None
    return beginning_of_file, current_char