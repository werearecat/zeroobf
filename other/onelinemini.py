import argparse
import random

def RandomChinaWord():
    val = random.randint(0x4e00, 0x9fbf) 
    return chr(val)

def RandomChina(size: int):
    words = ""
    for i in range(size):
        words += RandomChinaWord()
    return words

def generate_long_expression(target, depth=15):
    expression = str(target)
    for _ in range(depth):
        operation = random.choice(['+', '-', '*', '/'])
        next_number = random.randint(1, 10)
        if operation == '/':
            next_number = max(1, random.randint(1, 10))  # Ensure non-zero divisor
        expression = f"({expression} {operation} {next_number})"
        if operation == '+':
            target -= next_number
        elif operation == '-':
            target += next_number
        elif operation == '*':
            target /= next_number
        elif operation == '/':
            target *= next_number
    return expression

def create_expression_with_target(target, depth=25):
    while True:
        expression = generate_long_expression(target, depth)
        try:
            if eval(expression) == target:
                return expression
        except ZeroDivisionError:
            continue
        except Exception as e:
            print(f"Error creating expression: {e}")

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
    shuffled_text = ''.join(random.sample(text, len(text)))
    newline = "\n"
    XD = ''.join(f"""+WANNACRY({create_expression_with_target(ord(encode(c)))})""" for c in s)
    code = f"""
# https://github.com/werearecat/zeroobf
# no name :)
def WANNACRY(encoded_int):A=chr(encoded_int);B=[ord(A)-3 for A in A];C=''.join([chr(A)for A in B]);D=C[::-1];return D
exec(''{XD})
"""
    code = code.replace("WANNACRY(13)", "'\\n'")
    code = code.replace("WANNACRY", RandomChina(4))
    code = code.replace("encoded_int", RandomChina(5))
    
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
