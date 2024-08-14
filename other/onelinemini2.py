import base64
import marshal
import bz2
import argparse

def encryptcode(codee):
    return "exec(__import__('marshal').loads(__import__('bz2').decompress({})))".format(repr(bz2.compress(marshal.dumps(compile(codee, '<string>', 'exec')))))

def obfuscate(content):
    b64_content = base64.b64encode(content.encode()).decode()
    index = 0
    OFFSET = 10
    VARIABLE_NAME = "___" * 1000
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + str(byte)
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VARIABLE_NAME}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))\n{VARIABLE_NAME}=""'
    return encryptcode(code)

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
