ATOMS = {
    # single characters only

    'num': ['1','2','3','4','5','6','7','8','9'],
    'number': ['0','1','2','3','4','5','6','7','8','9'],
    'alpha_small': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',],
    'alpha_big': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',],
    'alpha': [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ],
    'arithmetic_operator': ['+', '-', '*', r'/', r'%',]
}

DELIMS = {
    'end': ['~'],
    'data_type': [',', '(', ')', ' ', '~', '='],
    'bool': [',', ' ', '}', ')', '~'],
    'conditional': ['('],
    'function': ['('],
    'mainuwu': ['-'],
    'int_float': [' ', *ATOMS['arithmetic_operator'], ')', '}', ']', '~', '!', r'&', '|', '>', '<', '='],
    'string': [' ', ')', ',', '&', '}', '[', ']', '~', '!', '='],
    'id': [' ', '~', ',', ')', '[', ']', '}', *ATOMS['arithmetic_operator'], '!', r'&', '|', '>', '<', '=', '.',],
    'assign_delim': [*ATOMS['alpha'], *ATOMS['number'], '{', ' ', '-' '('],
    'arithmetic_operator': [*ATOMS['alpha_small'], *ATOMS['number'], ' ', '-', '('],
    'logical_delim': ['"', *ATOMS['alpha_small'], *ATOMS['number'], ' ', '-', '('],
    'open_brace': [*ATOMS['number'], ' ', '"', *ATOMS['alpha_small'], r'\n', '>'],
    'close_brace': ['~', ' ', ',', ')', '>'],
    'open_parenthesis': [*ATOMS['number'], *ATOMS['alpha_small'], ' ', '-', r'\n', '>'],
    'close_parenthesis': [' ', *ATOMS['arithmetic_operator'], r'\n', '~', '>', '.'],
    'open_bracket': [*ATOMS['number'], '-'],
    'double_open_bracket': [' ', r'\n', *ATOMS['alpha_small'], '>'],
    'close_bracket': [' ', '~', ',', ')', '[', ']', '}', *ATOMS['arithmetic_operator'], '!', r'&', '|', '>', '<', '=', '.',],
    'double_close_bracket': [' ', r'\n', *ATOMS['alpha_small'], '>'],
    'unary': ['~', ')', '', *ATOMS['arithmetic_operator']],
    'concat': [' ', '"', *ATOMS['alpha_small']],
    'line': [None],
    'comma': [*ATOMS['alpha_small'], ' ', *ATOMS['number'], '"', '-', r'\n', '>'],
    'dot_op': [*ATOMS['alpha_small']],
    'start_done': [r'\n', ' ', '>'],
    'nuww': [' ', '~', ')', '}', ','],
}