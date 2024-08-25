import argparse
import random
import bz2
import zlib
import gzip
import lzma
import marshal
import base64

def string_to_lzma(byte_string):
    a = lzma.compress(byte_string)
    return f"lzma.decompress({repr(a)})"

def junk(codee):
    c = 'a' + str(random.randint(999999999999, 99999999999999))
    key = random.randint(1, 255)
    code_ = ''.join(chr(ord(c) ^ key) for c in codee)
    data = f"""
def {c}():
    {c} = {repr(code_)}
    if {random.randint(99999, 9999999)} == {random.randint(99999, 9999999)}:
        print({random.randint(99999, 9999999)})
        aaa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        print({random.randint(99999, 9999999)})
        bbb{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        z{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        zz{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        c{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        cc{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

    elif '{c}' == '{c}':
        exec(''.join(chr(ord(c) ^ {key}) for c in {c}))
        {c} = {random.randint(99999, 9999999)}{random.randint(99999, 9999999)}{random.randint(99999, 9999999)}

        aaa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        bbb{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        x{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        xx{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}

        a{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}
        aa{random.randint(99999, 9999999)} = {random.randint(99999, 9999999)}


{c}()
    """
    return data



def encryptcode(codee):
    compiled_code = compile(codee, 'zeroobf lmao', 'exec')
    methods = [
        ('bz2', bz2.compress, bz2.decompress),
        ('zlib', zlib.compress, zlib.decompress),
        ('gzip', gzip.compress, gzip.decompress),
        ('lzma', lzma.compress, lzma.decompress)
    ]
    name, compress_func, _ = random.choice(methods)
    compressed_code = compress_func(marshal.dumps(compiled_code))
    return f"import random, bz2, zlib, gzip, lzma, marshal\nexec(__import__('marshal').loads(__import__('{name}').decompress({string_to_lzma(compressed_code)})))"

def encryptcodegod(codee):
    for _ in range(2):
        codee = junk(codee)
        codee = encryptcode(codee)
        print(f"Layer {_}")
    codee += "\n\n# thank you my tootls \n# hai1723 repo: github.com/werearecat/zeroobf"
    return codee

def main():
    parser = argparse.ArgumentParser(description="Encrypt Python code using various compression methods.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input file containing Python code.")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output file to save encrypted code.")
    
    args = parser.parse_args()

    # Read the input file with UTF-8 encoding
    with open(args.input, 'r', encoding='utf-8') as infile:
        codee = infile.read()

    # Encrypt the code
    encrypted_code = encryptcodegod(codee)

    # Write the encrypted code to the output file with UTF-8 encoding
    with open(args.output, 'w', encoding='utf-8') as outfile:
        outfile.write(encrypted_code)

if __name__ == "__main__":
    main()
