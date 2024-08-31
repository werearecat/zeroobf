import argparse
import random
import bz2
import marshal

def reverse_bytes(byte_string):
    return byte_string[::-1]

def string_to_xor(byte_string):
    key = random.randint(1, 255)
    a = bytes([b ^ key for b in byte_string][::-1])
    xd = "([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) + ([]==[]) - ([]==[]) - ([]==[])"
    return f"bytes([b ^ {key} for b in {list(a)}][::{xd}])"

def hidden_int(int):
    a = str(int).encode()
    a = string_to_xor(a)
    return f"int({a})"

def string_to_bz2(byte_string):
    xd = f"{hidden_int(-1)}"
    reversed_bytes = reverse_bytes(byte_string)
    compressed = bz2.compress(reversed_bytes)
    reversed_compressed = reverse_bytes(compressed)
    return f"bz2.decompress({string_to_xor(reversed_compressed)}[::{xd}])[::{xd}]"

def RandomChinaWord():
    val = random.randint(0x4e00, 0x9fbf) 
    return chr(val)

def RandomChina(size: int):
    words = ""
    for i in range(size):
        words += RandomChinaWord()
    return words

def junk(codee):
    lay = [RandomChina(4),RandomChina(5),RandomChina(6),RandomChina(7),RandomChina(8)]
    random.shuffle(lay)
    c = lay[1]
    cc = lay[2]
    ccc = lay[3]
    code_ = string_to_bz2(codee.encode())
    data = f"""
def {c}():
    return {code_}

{ccc} = compile
{cc} = exec
{cc}({ccc}({c}(), 'zeroobf lmao', 'exec'))
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
    return f"import bz2, marshal\nexec(__import__('marshal').loads(__import__('{name}').decompress({string_to_bz2(compressed_code)})))"

def encryptcodegod(codee):
    oldcode = codee
    code = encryptcode(codee)
    for _ in range(2):
        print(f"Layer {_}")
        codee = junk(codee)
        print(len(codee))
        codee = encryptcode(codee)
        print(len(codee))
    codee += "\n\n# thank you my tootls \n# hai1723 repo: github.com/werearecat/zeroobf"
    size = len(codee) - len(oldcode)
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
