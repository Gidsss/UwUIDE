class ErrorSrc:
    src = [""]


class Error:
    def __init__(self, error_type: str, message: str, position: tuple[int, int], end_position: tuple[int, int] = None):
        self.error_type = error_type
        self.message = message
        self.position = position
        self.end_position = end_position

    def __str__(self):
        log = f"[{self.error_type}] Error on line {self.position[0] + 1}"
        if self.end_position and self.position[1] != self.end_position[1]:
            log += f" from column {self.position[1]} to {self.end_position[1]}"
        else:
            log += f" column {self.position[1]}"

        log += ':\n'
        log += f"\t{self.message}\n"

        # Error preview
        error_range = 1 if self.end_position is None else self.end_position[1] - self.position[1] + 1
        index_str = str(self.position[0] + 1)
        border = f"\t{'_' * (len(ErrorSrc.src[self.position[0]]) + len(index_str) + 3)}\n"
        log += border
        log += f"\t{index_str} | {ErrorSrc.src[self.position[0]]}\n"
        log += f"\t{' ' * len(index_str)} | {' ' * self.position[1]}{'^' * error_range}\n"
        log += border

        return log


class BasicError:
    """
    Error class with no position. Used for errors like "missing mainuwu function"
    """

    def __init__(self, error_type: str, message: str):
        self.error_type = error_type
        self.message = message

    def __str__(self):
        log = f"[{self.error_type}] {self.message}"
        return log
