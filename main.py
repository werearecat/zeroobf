import argparse
import random
import bz2
import zlib
import gzip
import lzma
import marshal

def string_to_xor(byte_string):
    key = random.randint(1, 255)
    a = bytes([b ^ key for b in byte_string])
    return f"bytes([b ^ {key} for b in {list(a)}])"

def junk(codee):
    c = 'a' + str(random.randint(999999999999, 99999999999999))
    key = random.randint(1, 255)
    code_ = ''.join(chr(ord(c) ^ key) for c in codee)
    junk2 = """
expr1 = (((x - 3) * 4 + (x + 2)) ** 3 - ((x / 2) + 5) * (x % 4)) / (x - 2)
expr2 = ((((x + 7) - 2) * 5) ** 2 + ((x * 3) + 8) * (x % 5)) / (x - 4)
expr3 = (((x * 2 + 3) * 6 - (x + 5)) ** 2 + ((x / 3) - 7) * (x % 2)) / (x + 4)
expr4 = (((x - 4) * 5 + 6) ** 2 - (x * 2) * (x % 4)) / (x + 3)
expr5 = ((x / 2 + 8) * 3 - (x - 1)) ** 2 + ((x * 4) - 6) * (x % 6) / (x - 1)
expr6 = (((x + 3) * 2 - (x - 6)) ** 2 + ((x * 5) + 4) * (x % 3)) / (x + 5)
expr7 = (((x - 2) * 4 + 7) ** 3 - (x / 4) * (x % 5)) / (x + 2)
expr8 = (((x * 3) - 8) * 2 + (x + 1)) ** 2 - ((x / 5) + 3) * (x % 7) / (x - 5)
expr9 = (((x + 4) * 6 - 3) ** 2 + (x / 2) * (x % 4)) / (x + 1)
expr10 = (((x * 2 + 9) - 6) * 3) ** 2 - ((x - 3) / 2) * (x % 5) / (x - 6)
""" * 10
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

{junk2}

{c}()
    """
    return data



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
    for _ in range(2):
        codee = junk(codee)
        codee = encryptcode(codee)
        print(f"Layer {_}")
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
