import marshal
import bz2
import argparse

def xor_encrypt_decrypt(data, key):
    """Encrypt or decrypt data using XOR with the given key."""
    return bytes([b ^ key for b in data])

def encryptcode(codee):
    compiled_code = compile(codee, '<string>', 'exec')
    compressed_code = bz2.compress(marshal.dumps(compiled_code))
    compressed_code_str = repr(compressed_code)
    return f"exec(__import__('marshal').loads(__import__('bz2').decompress({compressed_code_str})))"

def obfuscate(content, key=0x42):  # Default XOR key is 0x42
    # XOR encrypt the content
    xor_content = xor_encrypt_decrypt(content.encode(), key)
    hex_content = ''.join(f'\\x{byte:02x}' for byte in xor_content)
    
    index = 0
    OFFSET = 10
    VARIABLE_NAME = "___" * 1000
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(hex_content) / OFFSET) + 1):
        _str = hex_content[index:index + OFFSET]
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    
    code += f'exec(__import__("builtins").bytes.fromhex({VARIABLE_NAME}).decode().encode("latin1"))'
    return encryptcode(code)

def main():
    parser = argparse.ArgumentParser(description='1line Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-l', '--layer', type=int, default=1, help='Obfuscation layer (default: 1)')
    parser.add_argument('-k', '--key', type=int, default=0x42, help='XOR key (default: 0x42)')

    args = parser.parse_args()

    print(f"Reading input file: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    for _ in range(args.layer):
        code = obfuscate(code, key=args.key)
        print(f"{_}\{args.layer} obfuscated\n{len(code)} bytes!")
    
    print(f"Writing obfuscated code to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(code)

if __name__ == '__main__':
    main()
