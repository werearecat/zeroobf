import argparse

def obfcode(s):
    code = """
# https://github.com/werearecat/zeroobf
# no name :)
\u0674 = '';
"""
    code += ''.join(f"""\u0674+='\\x{ord(c):02x}';""" for c in s)
    code += 'exec(\u0674)'
    code += ';\u0674=""'
    return code

def main():
    parser = argparse.ArgumentParser(description='1line Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    
    args = parser.parse_args()
    
    print(f"Reading input file: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    
    obfuscated_code = obfcode(code)
    
    print(f"Writing obfuscated code to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)

if __name__ == '__main__':
    main()
