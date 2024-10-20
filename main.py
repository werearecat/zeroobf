import argparse
import random
import bz2
import marshal
import sys

def reverse_bytes(byte_string):
    return byte_string[::-1]

def RandomChina(size: int):
    return "".join(random.choices([chr(x) for x in range(sys.maxunicode) if chr(x).isidentifier()], k=random.randint(1, size)))

def import_gen(name):
    return f"__import__(bytes({list(name.encode())}).decode())"

def pack(string):
    pack =  string.encode()
    xd = f"eval(bytes.fromhex({repr(pack.hex())}))"
    return xd

def encryptstring(string):
    if isinstance(string, bytes):
        pack =  string[::-1]
        xd = f"bytes({list(pack)}[::-1])"
        return xd
    elif isinstance(string, str):
        pack =  string[::-1].encode()
        xd = f"bytes({list(pack)}[::-1]).decode()"
        return xd

def getexec(s):
    xd = f"getattr(__import__(bytes([115, 110, 105, 116, 108, 105, 117, 98][::-1]).decode()), bytes([108, 97, 118, 101][::-1]).decode())(bytes([99, 101, 120, 101][::-1]))({repr(s)})"
    return xd


def byte_to_bytel(byte_string):
    a = list(byte_string)[::-1]
    return f"bytes({a}[::-1])"

def hidden_int(int):
    a = str(int).encode()
    a = byte_to_bytel(a)
    return f"int({a})"

def string_to_bz2(byte_string):
    xd = f"{hidden_int(-1)}"
    reversed_bytes = reverse_bytes(byte_string)
    compressed = bz2.compress(reversed_bytes)
    reversed_compressed = reverse_bytes(compressed)
    return f"{import_gen('bz2')}.decompress({byte_to_bytel(reversed_compressed)}[::{xd}])[::{xd}]"





def junk(codee):
    lay = [RandomChina(4),RandomChina(5),RandomChina(6),RandomChina(7),RandomChina(8)]
    random.shuffle(lay)
    c = lay[1]
    cc = lay[2]
    ccc = lay[3]
    code_ = string_to_bz2(codee.encode())
    data = f"""
{ccc} = compile
{cc} = exec
{cc}({ccc}({code_}, 'zeroobf lmao', 'exec'))
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
    return f"exec({import_gen('marshal')}.loads({import_gen(name)}.decompress({string_to_bz2(compressed_code)})))"

def encryptcodegod(codee):
    oldcode = codee
    code = encryptcode(codee)
    code = getexec(codee)
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
