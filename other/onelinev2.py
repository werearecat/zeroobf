import argparse
import marshal

def string_to_hex(string):
    return ''.join(f'\\x{ord(c):02x}' for c in string)

def split_string(text):
    # Tính toán điểm chia chuỗi
    mid_index = len(text) // 2
    # Tách chuỗi thành hai phần
    first_part = text[:mid_index]
    second_part = text[mid_index:]
    return first_part, second_part

def split_string1(text):
    first_part, second_part = split_string(text)
    return first_part

def split_string2(text):
    first_part, second_part = split_string(text)
    return second_part

def obfcode(s):
    s = f"""
# you are good
exec("{string_to_hex(split_string1(s))}" + "{string_to_hex(split_string2(s))}")
"""
    s = f"""
# you are good
exec("{string_to_hex(split_string1(s))}" + "{string_to_hex(split_string2(s))}")
"""
    s = f"""
# you are good
exec("{string_to_hex(split_string1(s))}" + "{string_to_hex(split_string2(s))}")
"""
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
