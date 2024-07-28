import argparse
import marshal

def encryptcode(codee):
    compliecode = compile(codee, '<string>', 'exec')
    dump = marshal.dumps(compliecode)
    return f"exec(marshal.loads({dump}))"

def obfcode(s):
    s = encryptcode(s)
    XD_Anti = chr(len(str(exec)))
    XD_Anti2 = "chr(len(str(\u0674\u0674\u0674)))"
    XD = ''.join(f"""+chr(ord({XD_Anti2}) + {int(ord(c) - ord(XD_Anti))})""" for c in s)
    code = f"""
# https://github.com/werearecat/zeroobf
# no name :)
\u0674\u0674\u0674=exec;_NO(''{XD})
"""
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
