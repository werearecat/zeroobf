import argparse

def obfcode(s):
    newline = "\n"
    XD = ''.join(f"""+chr(ord('\\n') + {int(ord(c) - ord(newline))})""" for c in s)
    code = f"""
# https://github.com/werearecat/zeroobf
# no name :)
exec(''{XD})
"""
    code = code.replace("chr(ord('\\n') + 0)", "'\\n'")
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
