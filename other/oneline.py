import argparse

def encode(text):
    # Bước 1: Đảo ngược chuỗi
    reversed_text = text[::-1]
    
    # Bước 2: Chuyển đổi từng ký tự thành mã ASCII và cộng thêm một giá trị cố định (ví dụ 3)
    encoded_chars = [(ord(char) + 3) for char in reversed_text]
    
    # Bước 3: Chuyển đổi lại mã ASCII thành ký tự
    encoded_text = ''.join([chr(num) for num in encoded_chars])
    
    return encoded_text

def obfcode(s):
    newline = "\n"
    XD = ''.join(f"""+WANNACRY(chr({ord(encode(c))}))""" for c in s)
    code = f"""
# https://github.com/werearecat/zeroobf
# no name :)
def WANNACRY(encoded_text):A=[ord(A)-3 for A in encoded_text];B=''.join([chr(A)for A in A]);C=B[::-1];return C
exec(''{XD})
"""
    code = code.replace("chr(ord('\\n') + 0)", "'\\n'")
    code = code.replace("WANNACRY", "A")
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
