ATOMS = {
    # single characters only

    'num': {'1','2','3','4','5','6','7','8','9'},
    'number': {'0','1','2','3','4','5','6','7','8','9'},
    'alpha_small': {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',},
    'alpha_big': {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',},
    'alpha': {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    },
    'alphanum': {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0','1','2','3','4','5','6','7','8','9',
    },
    'arithmetic_operator': {'+', '-', '*', r'/', r'%'},
    'general_operator': {'+', '-', '*', '/', '%', '>', '<', '='},
}

DELIMS = {
    'end': {'~', ' '},
    'data_type': {'[', ',', '(', ')', ' ', '~', '=', '-'},
    'dono': {',', '(', ')', ' ', '='},
    'cwass': {',', '(', ')', ' ', '='},
    'bool': {',', ' ', '}', ')', '~'},
    'conditional': {'(', ' '},
    'io': {'(', ' '},
    'mainuwu': {'-', ' '},
    'int_float': {',', ' ', *ATOMS['general_operator'], ')', '}', ']', '~', '!', r'&', '|', '>', '<', '='},
    'string': {' ', ')', ',', '&', '}', '[', ']', '~', '!', '='},
    'assign_delim': {*ATOMS['alpha'], *ATOMS['number'], '{', ' ', '-', '('},
    'operator_delim': {*ATOMS['alpha'], *ATOMS['number'], ' ', '-', '('},
    'logical_delim': {'"', *ATOMS['alpha'], *ATOMS['number'], ' ', '-', '('},
    'string_parts': {'"', *ATOMS['alpha'], *ATOMS['number'], ' ', '-', '(', '|'},
    'open_brace': {'{', '}', '(', *ATOMS['number'], ' ', '"', *ATOMS['alpha'], '\n', '>'},
    'close_brace': {'}', '~', ' ', ',', ')', '\n', '>'},
    'open_parenthesis': {'{', *ATOMS['number'], *ATOMS['alpha'], ' ', '-', '\n', '>', '(', ')', '"'},
    'id': {' ', '~', ',', '(', ')', '[', ']', '}', *ATOMS['general_operator'], '!', r'&', '|', '.'},
    'close_parenthesis': {' ', *ATOMS['general_operator'], '!', '&', '|', '\n', '~', '>', '.', ',', ')', '(', '[', ']', '}'},
    'open_bracket': {']', *ATOMS['number'], '-', *ATOMS['alpha'], '(', ' '},
    'double_open_bracket': {' ', '\n', *ATOMS['alpha'], '>'},
    'close_bracket': {'(', ' ', '~', ',', ')', '[', ']', '}', *ATOMS['general_operator'], '!', r'&', '|', '.',},
    'double_close_bracket': {' ', '\n', *ATOMS['alpha'], '>'},
    'unary': {'|', '~', ')', *ATOMS['general_operator'], '!', ' '},
    'concat': {' ', '"', *ATOMS['alpha']},
    'line': {'\n', ' ', *ATOMS['alpha'], ']'},
    'comma': {*ATOMS['alpha'], ' ', *ATOMS['number'], '"', '-', '\n', '>'},
    'dot_op': {*ATOMS['alpha'], '[', '('},
    'start_done': {'\n', ' ', '>'},
    'nuww': {' ', '~', ')', '}', ','},
    'whitespace': {' '},
    'single_line_comment': {'\n'},
    'all': {None}
}
