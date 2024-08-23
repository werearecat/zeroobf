import random, bz2, zlib, gzip, lzma, marshal

def string_to_xor(string):
    key = random.randint(1, 255)
    a = ''.join(chr(ord(c) ^ key) for c in string) 
    return f"""''.join(chr(ord(c) ^ {key}) for c in {repr(a)})"""

def encryptcode(codee):
    compiled_code = compile(codee, '<string>', 'exec')
    methods = [
        ('bz2', bz2.compress, bz2.decompress),
        ('zlib', zlib.compress, zlib.decompress),
        ('gzip', gzip.compress, gzip.decompress),
        ('lzma', lzma.compress, lzma.decompress)
    ]
    name, compress_func, _ = random.choice(methods)
    compressed_code = compress_func(marshal.dumps(compiled_code))
    return f"import random, bz2, zlib, gzip, lzma, marshal\nexec(__import__('marshal').loads(__import__('{name}').decompress({string_to_xor(compressed_code)})))"

def encryptcodegod(codee):
    for _ in range(25):
        codee = encryptcode(codee)
    return codee

print(encryptcodegod('print("hi")'))
