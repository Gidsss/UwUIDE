from __future__ import annotations
from math import sqrt

class Bool:
    def __init__(self, val):
        try:
            self.val = bool(val)
        except:
            raise ValueError(f"oh no!! {self.val} cannot be converted to saaaamaaaaaaaaaaaa!!")

    ## META DUNDER METHODS
    # basic properties
    def __len__(self) -> int:
        return 1
    def __repr__(self):
        return self.__str__()

    # operator overloading
    def __add__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val + res)
    def __radd__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res + self.val)
    def __sub__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val - res)
    def __rsub__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res - self.val)
    def __mul__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val * res)
    def __rmul__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res * self.val)
    def __truediv__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val / res)
    def __rtruediv__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res / self.val)
    def __mod__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val % res)
    def __rmod__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res % self.val)
    def __pow__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val ** res)
    def __rpow__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res ** self.val)
    def __neg__(self) -> Bool:
        return type(self)(-self.val)
    def __lt__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val < res)
    def __gt__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val > res)
    def __le__(self, other) -> bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return self.val <= res
    def __ge__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(self.val >= res)
    def __eq__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res == self.val)
    def __ne__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return type(self)(res != self.val)

    # converting to other types
    def __str__(self):
        match self.val:
            case True: return "fax"
            case False: return "cap"
            case _: raise ValueError(f"oh no!! {self.val} cannot be converted to saaaamaaaaaaaaaaaa!!")
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
    def __add__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val + res))
    def __radd__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(res + self.val))
    def __sub__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val - res))
    def __rsub__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(res - self.val))
    def __mul__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val * res))
    def __rmul__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(res * self.val))
    def __truediv__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val / res))
    def __rtruediv__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(res / self.val))
    def __mod__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val % res))
    def __rmod__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(res % self.val))
    def __pow__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(self.val ** res))
    def __rpow__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return type(self)(self.cap_val(res ** self.val))
    def __neg__(self) -> Float:
        return type(self)(-self.val)
    def __lt__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return Bool(self.val < res)
    def __gt__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return Bool(self.val > res)
    def __le__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return Bool(self.val <= res)
    def __ge__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return Bool(self.val >= res)
    def __eq__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return Bool(res == self.val)
    def __ne__(self, other) -> Bool:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to kuuuuuuuunnnnnnn!!")
        return Bool(res != self.val)

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
    def _abs(self) -> Float:
        return type(self)(self.cap_val(abs(self.val)))
    def _pow(self, other: int|float) -> Float:
        return type(self)(self.cap_val(self.val ** other))
    def _sqrt(self) -> Float:
        return type(self)(float((self.cap_val(sqrt(self.val))).__floor__()))
    def _isNegative(self) -> Bool:
        return Bool(self.val < 0)
    def _isPositive(self) -> Bool:
        return Bool(self.val > 0)
    def _ceil(self) -> Float:
        return type(self)(float((self.cap_val(self.val)).__ceil__()))
    def _floor(self) -> Float:
        return type(self)(float((self.cap_val(self.val)).__floor__()))
    def _int(self) -> Int:
        return Int(self.val)

    ## HELPER METHODS
    def cap_val(self, val: float|int) -> float:
        if val > 9999999999.0:
            val = 9999999999.0
        elif val < -9999999999.0:
            val = -9999999999.0
        return float(val)

class Int:
    def __init__(self, val):
        try:
            self.val = 0
            res = float(val)
            self.val: int = int(self.cap_val(res))
        except:
            raise ValueError(f"Oh no!! '{val}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")

    ## META DUNDER METHODS
    # basic properties
    def __len__(self) -> int:
        return 1
    def __repr__(self):
        return repr(self.val)

    # operator overloading
    def __add__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(self.val + other)))
            case Float(): return Float(float(self.cap_val(self.val + other.val)))
            case _: return type(self)(self.cap_val(self.val + res))
    def __radd__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(other + self.val)))
            case Float(): return Float(float(self.cap_val(other.val + self.val)))
            case _: return type(self)(self.cap_val(res + self.val))
    def __sub__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(self.val - other)))
            case Float(): return Float(float(self.cap_val(self.val - other.val)))
            case _: return type(self)(self.cap_val(self.val - res))
    def __rsub__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(other - self.val)))
            case Float(): return Float(float(self.cap_val(other.val - self.val)))
            case _: return type(self)(self.cap_val(res - self.val))
    def __mul__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(self.val * other)))
            case Float(): return Float(float(self.cap_val(self.val * other.val)))
            case _: return type(self)(self.cap_val(self.val * res))
    def __rmul__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(other * self.val)))
            case Float(): return Float(float(self.cap_val(other.val * self.val)))
            case _: return type(self)(self.cap_val(res * self.val))
    def __truediv__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Float(self.cap_val(self.val / res))
    def __rtruediv__(self, other) -> Float:
        try:
            res = float(other)
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Float(self.cap_val(res / self.val))
    def __mod__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(self.val % other)))
            case Float(): return Float(float(self.cap_val(self.val % other.val)))
            case _: return type(self)(self.cap_val(self.val % res))
    def __rmod__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(other % self.val)))
            case Float(): return Float(float(self.cap_val(other.val % self.val)))
            case _: return type(self)(self.cap_val(res % self.val))
    def __pow__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(self.val ** other)))
            case Float(): return Float(float(self.cap_val(self.val ** other.val)))
            case _: return type(self)(self.cap_val(self.val ** res))
    def __rpow__(self, other) -> Int | Float:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        match other:
            case float(): return Float(float(self.cap_val(other ** self.val)))
            case Float(): return Float(float(self.cap_val(other.val ** self.val)))
            case _: return type(self)(self.cap_val(res ** self.val))
    def __neg__(self) -> Int:
        return type(self)(-self.val)
    def __lt__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Bool(self.val < res)
    def __gt__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Bool(self.val > res)
    def __le__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Bool(self.val <= res)
    def __ge__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Bool(self.val >= res)
    def __eq__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Bool(res == self.val)
    def __ne__(self, other) -> Bool:
        try:
            res = int(float(other))
        except:
            raise ValueError(f"Oh no!! '{other}' cannot be converted to chaaaaaaaaannnnnnnnnn!!")
        return Bool(res != self.val)

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
    def _abs(self) -> Int:
        return type(self)(self.cap_val(abs(self.val)))
    def _pow(self, other: int|float) -> Int:
        return type(self)(self.cap_val(self.val ** other))
    def _sqrt(self) -> Int:
        return type(self)(self.cap_val(int(sqrt(self.val))))
    def _isNegative(self) -> Bool:
        return Bool(self.val < 0)
    def _isPositive(self) -> Bool:
        return Bool(self.val > 0)
    def _float(self) -> Float:
        return Float(self.val)

    ## HELPER METHODS
    def cap_val(self, val: float|int) -> int|float:
        if val > 9999999999:
            val = 9999999999
        elif val < -9999999999:
            val = -9999999999
        return val
