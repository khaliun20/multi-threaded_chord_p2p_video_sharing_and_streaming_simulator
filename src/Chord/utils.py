import random
import string

random_str_len = 8


def random_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random_str_len))


def consistent_hash(key: str, m: int):
    return hash(key) % (2 ** m)
