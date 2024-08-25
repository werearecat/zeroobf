import argparse
import random
import bz2
import marshal

def reverse_bytes(byte_string):
    return byte_string[::-1]

def string_to_xor(byte_string):
    key = random.randint(1, 255)
    a = bytes([b ^ key for b in byte_string][::-1])
    return f"bytes([b ^ {key} for b in {list(a)}][::-1])"

def string_to_bz2(byte_string):
    reversed_bytes = reverse_bytes(byte_string)
    compressed = bz2.compress(reversed_bytes)
    reversed_compressed = reverse_bytes(compressed)
    return f"bz2.decompress({string_to_xor(reversed_compressed)}[::-1])[::-1]"

def junk(codee):
    c = 'a' + str(random.randint(999999999999, 99999999999999))
    code_ = string_to_bz2(codee.encode())
    data = f"""
def {c}():
    {c} = {code_}
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
        exec({c})
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
        ('bz2', bz2.compress, bz2.decompress)
    ]
    name, compress_func, _ = random.choice(methods)
    compressed_code = compress_func(marshal.dumps(compiled_code))
    return f"import random, bz2, marshal\nexec(__import__('marshal').loads(__import__('{name}').decompress({string_to_bz2(compressed_code)})))"

def encryptcodegod(codee):
    oldcode = codee
    for _ in range(2):
        print(f"Layer {_}")
        codee = junk(codee)
        print(len(codee))
        codee = encryptcode(codee)
        print(len(codee))
    codee += "\n\n# thank you my tootls \n# hai1723 repo: github.com/werearecat/zeroobf"
    size = len(oldcode) - len(codee)
    print(f'add {size} bytes in your code')
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
