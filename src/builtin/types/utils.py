class TypeError(Exception):
    pass
def expect_type_is_in(actual, expecteds: list[type], msg: str):
    if type(actual) not in expecteds:
        raise TypeError(f"{msg}\nExpected any in {expecteds} !!\nGot {type(actual)} !!!")
    return True
