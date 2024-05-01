from math import sqrt
class Float: ...
class Int: ...

class Float:
    def __init__(self, val):
        try:
            res = float(val)
            self.val: float = self.cap_val(res)
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
        return type(self)(self.cap_val(self.val + res))
    def __sub__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val - res))
    def __mul__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val * res))
    def __truediv__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val / res))
    def __mod__(self, other) -> "Float":
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val % res))
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
            return res
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to kuuuuuuuunnnnnnn!!")
    def __float__(self):
        try:
            res = float(self.val)
            return res
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to kuuuuuuuunnnnnnn!!")

    ## BUILTIN METHODS
    def _abs(self) -> "Float":
        return type(self)(self.cap_val(abs(self.val)))
    def _pow(self, other: int|float) -> "Float":
        return type(self)(self.cap_val(self.val ** other))
    def _sqrt(self) -> "Float":
        return type(self)(float((self.cap_val(sqrt(self.val))).__floor__()))
    def _isNegative(self) -> bool:
        return self.val < 0
    def _isPositive(self) -> bool:
        return self.val > 0
    def _ceil(self) -> "Float":
        return type(self)(float((self.cap_val(self.val)).__ceil__()))
    def _floor(self) -> "Float":
        return type(self)(float((self.cap_val(self.val)).__floor__()))
    def _chan(self) -> "Int":
        return Int(self.val)

    ## HELPER METHODS
    def cap_val(self, val) -> float:
        if val > 9999999999.0:
            val = 9999999999.0
        elif val < -9999999999.0:
            val = -9999999999.0
        return val

class Int:
    def __init__(self, val):
        try:
            res = int(float(val))
            self.val: int = self.cap_val(res)
        except:
            raise ValueError(f"Oh no!! '{val}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")

    ## META DUNDER METHODS
    # basic properties
    def __len__(self) -> int:
        return 1
    def __repr__(self):
        return repr(self.val)

    # operator overloading
    def __add__(self, other) -> "Int | Float":
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        if isinstance(other, float):
            return Float(float(self.cap_val(self.val + res)))
        return type(self)(self.cap_val(self.val + res))
    def __sub__(self, other) -> "Int | Float":
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        if isinstance(other, float):
            return Float(float(self.cap_val(self.val - res)))
        return type(self)(self.cap_val(self.val - res))
    def __mul__(self, other) -> "Int | Float":
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        if isinstance(other, float):
            return Float(float(self.cap_val(self.val * res)))
        return type(self)(self.cap_val(self.val * res))
    def __truediv__(self, other) -> Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Float(self.cap_val(self.val / res))
    def __mod__(self, other) -> "Int | Float":
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        if isinstance(other, float):
            return Float(float(self.cap_val(self.val % res)))
        return type(self)(self.cap_val(self.val % res))
    def __neg__(self) -> "Int":
        return type(self)(-self.val)
    def __lt__(self, other) -> bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val < res
    def __gt__(self, other) -> bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val > res
    def __le__(self, other) -> bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val <= res
    def __ge__(self, other) -> bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val >= res
    def __eq__(self, other):
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return res == self.val
    def __ne__(self, other):
        try:
            res = int(float(other))
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
    def __int__(self):
        try:
            res = int(self.val)
            return res
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to kuuuuuuuunnnnnnn!!")
    def __float__(self):
        try:
            res = float(self.val)
            return res
        except:
            raise ValueError(f"Oh no!! '{self.val}' cannot be converted to kuuuuuuuunnnnnnn!!")

    ## BUILTIN METHODS
    def _abs(self) -> "Int":
        return type(self)(self.cap_val(abs(self.val)))
    def _pow(self, other: int|float) -> "Int":
        return type(self)(self.cap_val(self.val ** other))
    def _sqrt(self) -> "Int":
        return type(self)(self.cap_val(int(sqrt(self.val))))
    def _isNegative(self) -> bool:
        return self.val < 0
    def _isPositive(self) -> bool:
        return self.val > 0
    def _kun(self) -> "Float":
        return Float(self.val)

    ## HELPER METHODS
    def cap_val(self, val) -> int:
        if val > 9999999999:
            val = 9999999999
        elif val < -9999999999:
            val = -9999999999
        return val
