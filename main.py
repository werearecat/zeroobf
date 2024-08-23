import marshal
import bz2

def string_to_xor(string):
    key = random.randint(1, 255)
    a = ''.join(chr(ord(c) ^ key) for c in string) 
    return f"""''.join(chr(ord(c) ^ {key}) for c in {repr(a)})"""

def encryptcode(codee):
    compiled_code = compile(codee, '<string>', 'exec')
    compressed_code = bz2.compress(marshal.dumps(compiled_code))
    compressed_code_str = string_to_xor(compressed_code)
    return f"exec(__import__('marshal').loads(__import__('bz2').decompress({compressed_code_str})))"
