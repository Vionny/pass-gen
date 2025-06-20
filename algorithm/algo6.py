import math
import string

def check_password_entropy(pwd: str) -> int:
    char_set_size = 0

    if any(c.islower() for c in pwd):
        char_set_size += 26

    if any(c.isupper() for c in pwd):
        char_set_size += 26

    if any(c.isdigit() for c in pwd):
        char_set_size += 10

    if any(c in string.punctuation for c in pwd):
        char_set_size += 32  # estimated size of common symbol set

    if char_set_size == 0:
        return 0  # prevent log2(0)

    entropy = len(pwd) * math.log2(char_set_size)

    if entropy < 28:
        return 0
    elif entropy < 36:
        return 1
    elif entropy < 60:
        return 2
    elif entropy < 128:
        return 3
    else:
        return 4
