def _verify_delim(context: tuple[list[str], list[int], str], expected_delims, current = False) -> tuple[bool, str]:
    lines, position, _ = context
    line, column = position

    if current:
        next_char = lines[line][column]
    elif column+1 >= len(lines[line]):
        next_char = '\n'
    else:
        next_char = lines[line][column+1]

    is_delim = True if next_char in expected_delims else False
        
    return is_delim, next_char