import random

def string_to_xor(string):
    key = random.randint(1, 255)
    a = ''.join(chr(ord(c) ^ key) for c in string) 
    return f"""''.join(chr(ord(c) ^ {key}) for c in "{repr(a)}")"""
