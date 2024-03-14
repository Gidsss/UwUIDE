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
    'end': {'~', ' ', '\n'},
    'data_type': {'[', ',', '(', ')', ' ', '~', '=', '-', '\n'},
    'dono': {',', '(', ')', ' ', '=', '\n'},
    'cwass': {'.', ',', '(', ')', ' ', '=', '\n'},
    'bool': {',', ' ', '}', ')', '~', '\n'},
    'conditional': {'[', '(', ' ', '\n'},
    'io': {'(', ' ', '\n'},
    'mainuwu': {'-', ' ', '\n'},
    'int_float': {',', ' ', *ATOMS['general_operator'], ')', '}', ']', '~', '!', r'&', '|', '>', '<', '=', '\n'},
    'string': {' ', ')', ',', '&', '}', '[', ']', '~', '!', '=', '\n'},
    'assign_delim': {*ATOMS['alpha'], *ATOMS['number'], '{', ' ', '-', '(', '"', '\n'},
    'operator_delim': {*ATOMS['alpha'], *ATOMS['number'], ' ', '-', '(', '{', '\n'},
    'logical_delim': {'"', *ATOMS['alpha'], *ATOMS['number'], ' ', '-', '(', '{', '\n'},
    'string_parts': {'"', *ATOMS['alpha'], *ATOMS['number'], ' ', '-', '(', '|', '\n', '&'},
    'open_brace': {'{', '}', '(', *ATOMS['number'], ' ', '"', *ATOMS['alpha'], '\n', '>', '-'},
    'close_brace': {'}', '~', ' ', ',', ')', '\n', '>', '&', *ATOMS['general_operator']},
    'open_parenthesis': {'{', *ATOMS['number'], *ATOMS['alpha'], ' ', '-', '\n', '>', '(', ')', '"'},
    'id': {'\n', ' ', '~', ',', '(', ')', '[', ']', '}', *ATOMS['general_operator'], '!', r'&', '|', '.'},
    'close_parenthesis': {' ', *ATOMS['general_operator'], '!', '&', '|', '\n', '~', '>', '.', ',', ')', '(', '[', ']', '}'},
    'open_bracket': {']', *ATOMS['number'], '-', *ATOMS['alpha'], '(', ' ', '\n'},
    'double_open_bracket': {' ', '\n', *ATOMS['alpha'], '>'},
    'close_bracket': {'\n', '(', ' ', '~', ',', ')', '[', ']', '}', *ATOMS['general_operator'], '!', r'&', '|', '.', '\n'},
    'double_close_bracket': {' ', '\n', *ATOMS['alpha'], '>'},
    'unary': {'|', '~', ')', *ATOMS['general_operator'], '!', ' ', '\n'},
    'concat': {' ', '"', *ATOMS['alpha'], *ATOMS['number'], '(', '{', '\n'},
    'line': {'\n', ' ', *ATOMS['alpha'], ']'},
    'comma': {*ATOMS['alpha'], ' ', *ATOMS['number'], '"', '-', '\n', '>', '{'},
    'dot_op': {*ATOMS['alpha'], '[', '(', '\n'},
    'nuww': {' ', '~', ')', '}', ',', '\n'},
    'whitespace': {' ', '\n'},
    'single_line_comment': {'\n'},
    'all': {None}
}
