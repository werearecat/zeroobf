import argparse
import random
import bz2
import zlib
import gzip
import lzma
import marshal

def Generate_decode_string(string):
    num = random.randint(1000000, 9999999)
    encoded = ''.join(chr(ord(c) + num) for c in string)
    return f"''.join(chr(ord(c) - {num}) for c in {repr(encoded)})"

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
    return f"import random, bz2, zlib, gzip, lzma, marshal\nexec(__import__('marshal').loads(__import__('{name}').decompress({Generate_decode_string(compressed_code.decode('latin1'))})))"

def encryptcodegod(codee):
    for _ in range(5):
        codee = encryptcode(codee)
        print(f"Layer {_}")
    return codee

def main():
    parser = argparse.ArgumentParser(description="Encrypt Python code using various compression methods.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input file containing Python code.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file to save encrypted code.")
    
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as infile:
        codee = infile.read()

    encrypted_code = encryptcodegod(codee)

    with open(args.output, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_code)

if __name__ == "__main__":
    main()
