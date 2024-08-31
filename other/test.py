import bz2
import random

def string_to_xor(byte_string):
    key = random.randint(1, 255)
    a = bytes([b ^ key for b in byte_string][::-1])
    return f"bytes([b ^ {key} for b in {list(a)}][::-1])"

def obfuscate(content):
    a = string_to_xor(bz2.compress(content))
    code = f"""
def eexec():
    exec(bz2.decompress({a}))

exec(eexec.__code__)

    """
    return code
