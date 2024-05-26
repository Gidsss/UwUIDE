from __future__ import annotations
from .namespace import Int, Bool

class String:
    def __init__(self, val: str = ""):
        self.val: str = str(val)

    ## META DUNDER METHODS
    # basic properties
    def __len__(self):
        return len(self.val)
    def __str__(self):
        return str(self.val)
    def __repr__(self):
        return repr(self.val)

    # operator overloading
    def __add__(self, other) -> String:
        'concatenates two strings'
        expect_type_is_in(other, self.valid_operands(),
                               msg=f"OwO... you can't add that!")
        return String(self.val + str(other))
    def __radd__(self, other) -> String:
        'concatenates two strings'
        expect_type_is_in(other, self.valid_operands(),
                               msg=f"OwO... you can't add that!")
        return String(str(other) + self.val)
    def __eq__(self, other) -> Bool:
        return Bool(other == self.val)
    def __ne__(self, other) -> Bool:
        return Bool(other != self.val)

    # converting to other types
    def __nonzero__(self):
        'determines the truth value of String (same as str)'
        return bool(self.val)
    def __bool__(self):
        'determines the truth value of String (same as str)'
        return bool(self.val)
    def __int__(self):
        'converts String to int'
        try:
            res = int(self.val)
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return int(res)
    def __float__(self):
        'converts String to float'
        try:
            res = float(self.val)
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to kuuuuuuuunnnnnnnnnnn!!")
        return float(res)

    # subscripting
    def __getitem__(self, index):
        return String(self.val[index])
    def __contains__(self, item):
        return item in self.val
    def __iter__(self):
        return iter(self.val)

    ## BUILTIN METHODS
    def _len(self) -> Int:
        return Int(self.__len__())
    def _reversed(self) -> String:
        return type(self)(self.val[::-1])
    def _has(self, item: str) -> Bool:
        return Bool(str(item) in self.val)
    def _upper(self) -> String:
        return type(self)(self.val.upper())
    def _lower(self) -> String:
        return type(self)(self.val.lower())
    def _concat(self, item: str) -> String:
        tmp = str(self.val) + str(item)
        return type(self)(tmp)
    def _prepend(self, item: str) -> String:
        tmp = str(item) + str(self.val)
        return type(self)(tmp)
    def _count(self, item: str) -> Int:
        return Int(self.val.count(str(item)))
    def _endswith(self, item: str) -> Bool:
        return Bool(self.val.endswith(str(item)))
    def _startswith(self, item: str) -> Bool:
        return Bool(self.val.startswith(str(item)))
    def _index(self, item: str) -> Int:
        return Int(self.val.find(str(item)))
    def _replace(self, old: str, new: str) -> String:
        return type(self)(self.val.replace(str(old), str(new)))
    def _strip(self) -> String:
        return type(self)(self.val.strip())
    def _split(self) -> Array:
        return Array([type(self)(x) for x in self.val.split(" ")])
    def _swapcase(self) -> String:
        return type(self)(self.val.swapcase())
    def _title(self) -> String:
        return type(self)(self.val.title())
    def _first(self, n: Int) -> String:
        idx: int = max(int(n), 0)
        return type(self)(self.val[:idx])
    def _last(self, n: Int) -> String:
        idx: int = max(int(n), 0)
        return type(self)(self.val[-idx:])
    def _substr(self, start: Int, end: Int) -> String:
        start_idx: int = max(int(start), 0)
        end_idx: int = max(int(end), 0)
        return type(self)(self.val[start_idx:end_idx+1])
    def _from(self, item: str) -> String:
        if self.val.find(str(item)) == -1:
            return type(self)("")
        return type(self)(str(item) + str(self.val[self.val.find(str(item))+len(item):]))
    def _upTo(self, item: str) -> String:
        if self.val.find(str(item)) == -1:
            return type(self)("")
        return type(self)(str(self.val[:self.val.find(str(item))]) + str(item))

    ## UTILS
    def valid_operands(self) -> list[type]:
        return [str, String]

class Array:
    def __init__(self, vals: "list|Array"):
        tmp: "list|Array" = vals
        while isinstance(tmp, Array): tmp = tmp.val
        self.val: list = tmp

    ## META DUNDER METHODS
    # basic properties
    def __len__(self):
        return len(self.val)
    def __str__(self):
        res = "{"
        for val in self.val: res += str(val) + ", "
        res = (res[:-2] if res[-2:] == ", " else res) + "}"
        return res
    def __repr__(self):
        return repr(self.val)

    # operator overloading
    def __eq__(self, other) -> Bool:
        expect_type_is_in(other, self.valid_operands(),
                               msg=f"OwO... you can't compare with that!")
        return Bool(self.val == other)
    def __ne__(self, other) -> Bool:
        expect_type_is_in(other, self.valid_operands(),
                               msg=f"OwO... you can't compare with that!")
        return Bool(self.val != other)

    # converting to other types
    def __nonzero__(self):
        'determines the truth value of Array (same as list)'
        return bool(self.val)
    def __bool__(self):
        'determines the truth value of Array (same as list)'
        return bool(self.val)

    # subscripting
    def __getitem__(self, index):
        return self.val[index]
    def __setitem__(self, index, item):
        self.val[index] = item
    def __contains__(self, item):
        return item in self.val
    def __iter__(self):
        return iter(self.val)

    ## BUILTIN METHODS
    def _len(self) -> Int:
        return Int(self.__len__())
    def _reverse(self) -> None:
        self.val = self.val[::-1]
    def _append(self, item) -> None:
        self.val.append(item)
    def _has(self, item) -> Bool:
        return Bool(item in self.val)
    def _clear(self) -> None:
        self.val.clear()
    def _count(self, item) -> Int:
        return Int(self.val.count(item))
    def _extend(self, item) -> None:
        self.val.extend(item)
    def _index(self, item) -> Int:
        if item not in self.val: return Int(-1)
        return Int(self.val.index(item))
    def _pop(self):
        if len(self.val) == 0: raise PopError("OwO...Tried to pop from an empty array!!!!!")
        return self.val.pop()
    def _prepend(self, item) -> None:
        self.val.insert(0, item)
    def _prextend(self, item) -> None:
        self.val = item + self.val
    def _dimension(self) -> Int:
        dimension = 0
        tmp = self.val
        while isinstance(tmp, list):
            dimension += 1
            if len(tmp) == 0: break
            tmp = tmp[0]
            if not isinstance(tmp, Array): break
            tmp = tmp.val
        return Int(dimension)
    def _first(self, n) -> Array:
        idx = max(int(n), 0)
        return Array(self.val[:idx])
    def _flatten(self) -> Array:
        def flatten(arr: list|Array) -> list:
            flattened = []
            for item in arr:
                match item:
                    case list() | Array(): flattened.extend(flatten(item))
                    case _: flattened.append(item)
            return flattened
        return Array(flatten(self.val))
    def _join(self, separator: String) -> String:
        return String(str(separator).join([str(val) for val in self._flatten()]))
    def _last(self, n) -> Array:
        idx = max(int(n), 0)
        return Array(self.val[-idx:])
    def _replace(self, old, new) -> None:
        self.val = [new if x == old else x for x in self.val]
    def _shift(self):
        if len(self.val) == 0: raise ShiftError("OwO...Tried to shift from an empty array!!!!!")
        return self.val.pop(0)

    ## UTILS
    def valid_operands(self) -> list[type]:
        return [list, Array]

class TypeError(Exception):...
class PopError(Exception):...
class ShiftError(Exception):...
def expect_type_is_in(actual, expecteds: list[type], msg: str):
    if type(actual) not in expecteds:
        raise TypeError(f"{msg}\nExpected any in {expecteds} !!\nGot {type(actual)} !!!")
    return True
