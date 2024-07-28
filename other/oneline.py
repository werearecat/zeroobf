import argparse

def obfcode(s):
    newline = "\n"
    XD = ''.join(f"""+chr(ord('\\n') + {int(ord(c) - ord(newline))})""" for c in s)
    code = f"""
# https://github.com/werearecat/zeroobf
# no name :)
exec(''{XD})
"""
    code = code.replace("chr(ord('\\n') + 0)", "'\\n'") # new line

    code = code.replace("chr(ord('\n') + 38)", "str(False + False + False + False + False + False + False + False + False + False)") # 0
    code = code.replace("chr(ord('\n') + 39)", "str(True + False + False + False + False + False + False + False + False + False)") # 1
    code = code.replace("chr(ord('\\n') + 40)", "str(True + True + False + False + False + False + False + False + False + False)") # 2
    code = code.replace("chr(ord('\\n') + 41)", "str(True + True + True + False + False + False + False + False + False + False)") # 3
    code = code.replace("chr(ord('\\n') + 42)", "str(len(str("exec")))") # 4
    code = code.replace("chr(ord('\\n') + 43)", "str(True + True + True + True + True + False + False + False + False + False)") # 5
    code = code.replace("chr(ord('\\n') + 44)", "str(True + True + True + True + True + True + False + False + False + False)") # 6
    code = code.replace("chr(ord('\\n') + 45)", "str(True + True + True + True + True + True + True + False + False + False)") # 7
    code = code.replace("chr(ord('\\n') + 46)", "str(True + True + True + True + True + True + True + True + False + False)") # 8
    code = code.replace("chr(ord('\\n') + 47)", "str(True + True + True + True + True + True + True + True + True + False)") # 9
    
    code = code.replace("True", "([]==[])").replace("False", "(()==[])")
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
