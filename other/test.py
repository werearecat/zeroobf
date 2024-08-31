import bz2
import random
import argparse

def string_to_xor(byte_string):
    key = random.randint(1, 255)
    a = bytes([b ^ key for b in byte_string][::-1])
    return f"bytes([b ^ {key} for b in {list(a)}][::-1])"

def obfuscate(content):
    a = string_to_xor(bz2.compress(content.encode()))
    code = f"""
def eexec():
    exec(bz2.decompress({a}))

exec(eexec.__code__)

    """
    return code

def main():
    parser = argparse.ArgumentParser(description='XOR Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-l', '--layer', type=int, default=1, help='Obfuscation layer (default: 1)')
    
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    
    for _ in range(args.layer):
        code = obfuscate(code)
        print(f"{_}\\{args.layer} obfuscated\n{len(code)} bytes!")
    
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(code)

if __name__ == '__main__':
    main()
