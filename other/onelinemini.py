import base64
import marshal
import bz2
import argparse

def encryptcode(codee):
    compiled_code = compile(codee, '<string>', 'exec')
    compressed_code = bz2.compress(marshal.dumps(compiled_code))
    compressed_code_str = repr(compressed_code)
    return f"exec(__import__('marshal').loads(__import__('bz2').decompress({compressed_code_str}))"

def obfuscate(content):
    content = encryptcode(content)
    compiled_code = compile(content, "<string>", "exec")
    bytecode = compiled_code.co_code
    byte_values = list(bytecode)
    obfuscated_code = f'exec(types.CodeType(0, 0, 0, 0, 0, b"{bytes(byte_values).decode("latin1")}", (), (), (), "", "", 0, b""))'
    return obfuscated_code

def main():
    parser = argparse.ArgumentParser(description='1line Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    parser.add_argument('-l', '--layer', type=int, default=1, help='Obfuscation layer (default: 1)')

    args = parser.parse_args()


        
    print(f"Reading input file: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    for _ in range(args.layer):
        code = obfuscate(code)
        print(f"{_}\{args.layer} obfuscated\n{len(code)} bytes!")
    
    print(f"Writing obfuscated code to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(code)

if __name__ == '__main__':
    main()
