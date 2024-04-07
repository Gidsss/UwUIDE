
class TypeError(Exception):
    pass
def expect_type_is_in(actual, expecteds: list[type], msg: str):
    for expected in expecteds:
        if not isinstance(actual, expected):
            raise TypeError(f"{msg}\nExpected any in {expecteds} !!\nGot {type(actual)} !!!")
    return True
