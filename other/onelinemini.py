import argparse
import random

def string_to_hex(string):
    return ''.join(f'\\x{ord(c):02x}' for c in string)

def random_chinese_word():
    return chr(random.randint(0x4e00, 0x9fbf))

def random_chinese(size):
    return ''.join(random_chinese_word() for _ in range(size))

def encode(text):
    reversed_text = text[::-1]
    encoded_chars = [(ord(char) + 30) for char in reversed_text]
    return ''.join(chr(num) for num in encoded_chars)

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

def create_expression_with_target(target, depth=15):
    while True:
        expression = generate_long_expression(target, depth)
        try:
            if eval(expression) == target:
                return expression
        except ZeroDivisionError:
            continue
        except Exception as e:
            print(f"Error creating expression: {e}")

def obfuscate_code(source_code):
    encoded_text = encode(source_code)
    hex_encoded_text = string_to_hex(encoded_text)
    
    obfuscated_code = f"""
# https://github.com/werearecat/zeroobf
# no name :)
def obfuscated_function(encoded_text):
    decoded_chars = [(ord(char) - {create_expression_with_target(30)}) for char in encoded_text]
    reversed_text = ''.join(chr(num) for num in decoded_chars)
    return reversed_text[::-1]

exec(obfuscated_function("{hex_encoded_text}"))
"""
    obfuscated_code = obfuscated_code.replace("obfuscated_function(13)", "'\\n'")
    obfuscated_code = obfuscated_code.replace("obfuscated_function", random_chinese(4))
    obfuscated_code = obfuscated_code.replace("text", random_chinese(15))
    
    return obfuscated_code

def main():
    parser = argparse.ArgumentParser(description='1line Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    
    args = parser.parse_args()
    
    print(f"Reading input file: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    
    obfuscated_code = obfuscate_code(code)
    
    print(f"Writing obfuscated code to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)

if __name__ == '__main__':
    main()
