from random import seed, randint

import time
from string import ascii_uppercase, digits


class UserExitException(Exception):
    pass


def get_random_string_without_repeats(n):
    res = ''
    seed(str(time.time()))
    alpha = list(ascii_uppercase + digits)
    for i in range(n):
        k = randint(0, len(alpha) - 1 - i)
        res += alpha[k]
        alpha[k], alpha[len(alpha) - i - 1] = alpha[len(alpha) - i - 1], alpha[k]
    return res
