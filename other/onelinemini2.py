import base64
import marshal
import bz2
import argparse

def encryptcode(codee):
    return "exec(__import__('marshal').loads(__import__('bz2').decompress({})))".format(repr(bz2.compress(marshal.dumps(compile(codee, '<string>', 'exec')))))

def obfuscate(content):
    hex_string = ''.join("\\x{}".format(hex(ord(c))[2:].zfill(2)) for c in base64.b64encode(content.encode()).decode())
    formatted_code = 'exec(__import__("base64").b64decode("{}".encode("utf-8")).decode("utf-8"))'.format(hex_string)
    return encryptcode(formatted_code)

def main():
    parser = argparse.ArgumentParser(description='1line Obfuscator')
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
