import re
import random

def generate_random_string():
    return '\u0674\u0674' * random.randint(100, 250)

def obfuscate_code(code):
    # Tìm tất cả các định nghĩa hàm
    function_names = re.findall(r'def\s+(\w+)\s*\(', code)
    # Tìm tất cả các định nghĩa lớp
    class_names = re.findall(r'class\s+(\w+)\s*:', code)
    # Tìm tất cả các biến toàn cục
    variable_names = re.findall(r'\b(\w+)\s*=', code)

    # Kết hợp tất cả các tên để thay thế
    all_names = set(function_names + class_names + variable_names)

    for name in all_names:
        random_string = generate_random_string()
        code = code.replace(name, random_string)
    
    return code

def obfuscate_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        code = file.read()
    
    obfuscated_code = obfuscate_code(code)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)

if __name__ == "__main__":
    obfuscate_file('main.py', 'main_obfuscated.py')
