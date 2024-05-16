from src.builtin.types.namespace import Int, Float, Bool, String

from random import randint, uniform, choice
from string import ascii_letters, digits, punctuation

def _randomInt(bound1: Int, bound2: Int) -> Int:
    lower = min(float(bound1), float(bound2))
    upper = bound2 if lower == bound1 else bound1
    return Int(randint(int(lower), int(upper)))

def _randomFloat(bound1: Int, bound2: Int) -> Float:
    lower = min(float(bound1), float(bound2))
    upper = bound2 if lower == bound1 else bound1
    return Float(uniform(int(lower), int(upper)))

def _randomBool() -> Bool: return Bool(randint(0, 1))

def _randomString(length: Int) -> String:
    return String(''.join(choice(ascii_letters + digits + punctuation) for _ in range(max(int(length), 0))))
