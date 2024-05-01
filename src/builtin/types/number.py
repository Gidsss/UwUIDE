class Int:
    def __init__(self, val):
        try:
            self.val: int = int(val)
            if self.val > 9999999999:
                self.val = 9999999999
            elif self.val < -9999999999:
                self.val = -9999999999
        except:
            raise ValueError(f"Oh no!! '{val}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")

    ## META DUNDER METHODS
    # basic properties
    def __len__(self) -> int:
        return 1
    def __repr__(self):
        return repr(self.val)

    # operator overloading
    def __add__(self, other) -> "Int":
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val + res)
    def __sub__(self, other) -> "Int":
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val - res)
    def __mul__(self, other) -> "Int":
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val * res)
    def __truediv__(self, other) -> "Int":
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val / res)
    def __neg__(self) -> "Int":
        return type(self)(-self.val)
    def __lt__(self, other) -> bool:
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val < res
    def __gt__(self, other) -> bool:
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val > res
    def __le__(self, other) -> bool:
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val <= res
    def __ge__(self, other) -> bool:
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val >= res
    def __eq__(self, other):
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return res == self.val
    def __ne__(self, other):
        try:
            res = int(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return res != self.val

    # converting to other types
    def __str__(self):
        return str(self.val)
    def __nonzero__(self):
        return bool(self.val)
    def __bool__(self):
        return bool(self.val)
    def __float__(self):
        try:
            res = float(self.val)
            return Float(res)
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to kuuuuuuuunnnnnnn!!")

    ## BUILTIN METHODS
    def _abs(self) -> "Int":
        return type(self)(abs(self.val))

class Float:
    def __init__(self, val):
        try:
            self.val: float = float(val)
            if self.val > 9999999999.0:
                self.val = 9999999999.0
            elif self.val < -9999999999.0:
                self.val = -9999999999.0
        except:
            raise ValueError(f"Oh no!! '{val}' cannot be converted to kuuuuuuuunnnnnnn!!")

    ## META DUNDER METHODS
    # basic properties
    def __len__(self) -> int:
        return 1
    def __repr__(self):
        return repr(self.val)

    # operator overloading
    def __add__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.val + res)
    def __sub__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.val - res)
    def __mul__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.val * res)
    def __truediv__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.val / res)
    def __neg__(self) -> "Float":
        return type(self)(-self.val)
    def __lt__(self, other) -> bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return self.val < res
    def __gt__(self, other) -> bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return self.val > res
    def __le__(self, other) -> bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return self.val <= res
    def __ge__(self, other) -> bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return self.val >= res
    def __eq__(self, other):
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return res == self.val
    def __ne__(self, other):
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return res != self.val

    # converting to other types
    def __str__(self):
        return str(self.val)
    def __nonzero__(self):
        return bool(self.val)
    def __bool__(self):
        return bool(self.val)
    def __int__(self):
        try:
            res = int(self.val)
            return Int(res)
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to kuuuuuuuunnnnnnn!!")

    ## BUILTIN METHODS
    def _abs(self) -> "Float":
        return type(self)(abs(self.val))
