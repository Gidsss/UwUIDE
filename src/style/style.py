from enum import Enum
class AnsiColor(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

    @staticmethod
    def colors_iter():
        '''
        Yields colors in order. This loops back to first color after last color.
        This is intended to be used with next(), not in a loop.
        '''
        colors = [AnsiColor.YELLOW, AnsiColor.BLUE, AnsiColor.MAGENTA, AnsiColor.CYAN]
        while True:
            for color in colors:
                yield color


class Styled:
    @staticmethod
    def print(*msgs, color: AnsiColor = AnsiColor.RESET, sep = ' ', end = '\n'):
        print(color.value, ' '.join(msgs), AnsiColor.RESET.value, sep=sep, end=end)

    @staticmethod
    def sprint(*msgs, color: AnsiColor = AnsiColor.RESET):
        return f"{color.value}{' '.join(msgs)}{AnsiColor.RESET.value}"

    @staticmethod
    def sprintln(*msgs, color: AnsiColor = AnsiColor.RESET):
        return Styled.sprint(*msgs, color=color) + '\n'
