from typing import Self

class String:
    def __init__(self, val: str):
        expect_type_is_in(val, self.stringable_types(),
                               msg=f"OwO... that ain't stringable!")
        self.val: str = str(val)

    ## META DUNDER METHODS
    # basic properties
    def __len__(self):
        return len(self.val)
    def __str__(self):
        return str(self.val)

    # operator overloading
    def __add__(self, other):
        'concatenates two strings'
        expect_type_is_in(other, self.valid_operands(),
                               msg=f"OwO... you can't add that!")
        return String(self.val + str(other))
    def __eq__(self, other):
        expect_type_is_in(other, self.stringable_types(),
                               msg=f"OwO... you can't compare with that!")
        return other == self.val
    def __ne__(self, other):
        expect_type_is_in(other, self.stringable_types(),
                               msg=f"OwO... you can't compare with that!")
        return other != self.val

    # converting to other types
    def __nonzero__(self):
        'determines the truth value of String (same as str)'
        expect_type_is_in(self.val, self.valid_operands(),
                               msg=f"OwO... that ain't a String!")
        return bool(self.val)
    def __bool__(self):
        'determines the truth value of String (same as str)'
        expect_type_is_in(self.val, self.valid_operands(),
                               msg=f"OwO... that ain't a String!")
        return bool(self.val)
    def __int__(self):
        'converts String to int'
        expect_type_is_in(self.val, self.valid_operands(),
                               msg=f"OwO... that ain't a String!")
        return int(self.val)
    def __float__(self):
        'converts String to float'
        expect_type_is_in(self.val, self.valid_operands(),
                               msg=f"OwO... that ain't a String!")
        return float(self.val)

    # subscripting
    def __getitem__(self, index):
        return self.val[index]
    def __contains__(self, item):
        return item in self.val
    def __iter__(self):
        return iter(self.val)

    ## BUILTIN METHODS
    def _len(self) -> int:
        return self.__len__()
    def _reversed(self) -> Self:
        return type(self)(self.val[::-1])
    def _has(self, item: str) -> bool:
        return item in self.val
    def _upper(self) -> Self:
        return type(self)(self.val.upper())
    def _lower(self) -> Self:
        return type(self)(self.val.lower())

    ## UTILS
    def stringable_types(self) -> list[type]:
        return [str, String, int, float, bool, Array]
    def valid_operands(self) -> list[type]:
        return [str, String]

class Array:
    def __init__(self, vals: list):
        self.val: list = vals

    ## META DUNDER METHODS
    # basic properties
    def __len__(self):
        return len(self.val)
    def __str__(self):
        return str(self.val)
    def __repr__(self):
        return repr(self.val)

    # operator overloading
    def __eq__(self, other):
        expect_type_is_in(other, self.valid_operands(),
                               msg=f"OwO... you can't compare with that!")
        return self.val == other
    def __ne__(self, other):
        expect_type_is_in(other, self.valid_operands(),
                               msg=f"OwO... you can't compare with that!")
        return self.val != other

    # converting to other types
    def __nonzero__(self):
        'determines the truth value of Array (same as list)'
        expect_type_is_in(self.val, self.valid_operands(),
                               msg=f"OwO... that ain't an Array!")
        return bool(self.val)
    def __bool__(self):
        'determines the truth value of Array (same as list)'
        expect_type_is_in(self.val, self.valid_operands(),
                               msg=f"OwO... that ain't an Array!")
        return bool(self.val)

    # subscripting
    def __getitem__(self, index):
        return self.val[index]
    def __contains__(self, item):
        return item in self.val
    def __iter__(self):
        return iter(self.val)

    ## BUILTIN METHODS
    def _len(self) -> int:
        return self.__len__()
    def _reverse(self) -> None:
        self.val = self.val[::-1]
    def _append(self, item) -> None:
        self.val.append(item)

    ## UTILS
    def valid_array_elems(self) -> list[type]:
        return [str, String, int, float, bool, list, Array]
    def valid_operands(self) -> list[type]:
        return [list, Array]

class TypeError(Exception):
    pass
def expect_type_is_in(actual, expecteds: list[type], msg: str):
    if type(actual) not in expecteds:
        raise TypeError(f"{msg}\nExpected any in {expecteds} !!\nGot {type(actual)} !!!")
    return True
