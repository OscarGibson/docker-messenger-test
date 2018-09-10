import string
from random import choice

allchar = string.ascii_letters + string.digits

def generate_random_string(length= 32):
    return "".join(choice(allchar) for x in range(length))