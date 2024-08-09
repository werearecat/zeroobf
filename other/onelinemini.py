import argparse
import random

def string_to_hex(string):
    return ''.join(f'\\x{ord(c):02x}' for c in string)

def RandomChinaWord():
    val = random.randint(0x4e00, 0x9fbf) 
    return chr(val)

def RandomChina(size: int):
    words = ""
    for i in range(size):
        words += RandomChinaWord()
    return words

def encode(text):
    # Bước 1: Đảo ngược chuỗi
    reversed_text = text[::-1]
    
    # Bước 2: Chuyển đổi từng ký tự thành mã ASCII và cộng thêm một giá trị cố định (ví dụ 3)
    encoded_chars = [(ord(char) + 3) for char in reversed_text]
    
    # Bước 3: Chuyển đổi lại mã ASCII thành ký tự
    encoded_text = ''.join([chr(num) for num in encoded_chars])
    
    return encoded_text


def obfcode(s):
    
    text = ''.join([chr(i) for i in range(0x4e00, 0x9fbf + 1)])
    newline = "\n"
    code = f"""
# https://github.com/werearecat/zeroobf
# no name :)
def WANNACRY(encoded_text):
    # Bước 1: Chuyển đổi từng ký tự thành mã ASCII và trừ đi giá trị cố định (ví dụ 3)
    decoded_chars = [(ord(char) - 3) for char in encoded_text]
    
    # Bước 2: Chuyển đổi lại mã ASCII thành ký tự
    reversed_text = ''.join([chr(num) for num in decoded_chars])
    
    # Bước 3: Đảo ngược chuỗi để phục hồi chuỗi gốc
    original_text = reversed_text[::-1]
    
    return original_text
exec(WANNACRY("{string_to_hex(encode(s))}"))
"""
    code = code.replace("WANNACRY(13)", "'\\n'")
    code = code.replace("WANNACRY", RandomChina(4))
    code = code.replace("text", RandomChina(15))
    
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
