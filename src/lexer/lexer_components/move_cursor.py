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
        