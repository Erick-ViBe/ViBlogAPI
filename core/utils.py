import random
import string


ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits
STRING_LENGTH = 6


def generate_random_string(chars=ALPHANUMERIC_CHARS, length=STRING_LENGTH):
    """Generates a random string of chars in lowercase and numbers"""
    return "".join(random.choice(chars) for _ in range(length))
