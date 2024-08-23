import random, bz2, zlib, gzip, lzma, marshal

def string_to_xor(byte_string):
    key = random.randint(1, 255)
    a = bytes([b ^ key for b in byte_string])
    return f"bytes([b ^ {key} for b in {list(a)}])"

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
    return f"import random, bz2, zlib, gzip, lzma, marshal\nexec(marshal.loads(__import__('{name}').decompress({string_to_xor(compressed_code)})))"

def encryptcodegod(codee):
    for _ in range(25):
        codee = encryptcode(codee)
    return codee

print(encryptcodegod('print("hi")'))
