import random
import string
import base64
import argparse
import zlib
import re
import builtins
from python_minifier import minify as pyminify

def generate_obfuscated_name(name):
    """Generates a random obfuscated name based on the original function name."""
    return f"_{''.join(random.choices(string.ascii_letters + string.digits, k=100))}"

def functionobf(code):
    """Obfuscates built-in function names in the provided code while preserving execution."""
    functions = dir(builtins)
    
    # Filter only callable functions and exclude special methods
    function_names = [func for func in functions if callable(getattr(builtins, func)) and not func.startswith('__')]
    
    obfuscation_map = {}
    for func in function_names:
        obfuscated_name = generate_obfuscated_name(func)
        obfuscation_map[func] = obfuscated_name

        # Replace function names with their obfuscated versions
        code = re.sub(r'\b' + re.escape(func) + r'\b', obfuscated_name, code)
    
    # Generate code to restore original functions
    restore_code = "\n".join(f"{obfuscated_name} = {func}" for func, obfuscated_name in obfuscation_map.items())
    
    # Add restore code at the beginning of the obfuscated code
    obfuscated_code = f"{restore_code}\n\n{code}"
    
    return obfuscated_code

def obfcode(s):
    s = s.replace("\u0674", "a")
    code = """
# https://github.com/werearecat/zeroobf
# no name :)
\u0674 = '';
"""
    code += ''.join(f"""\u0674+='\\x{ord(c):02x}';""" for c in s)
    code += 'exec(\u0674)'.replace("exec", """getattr(__import__(base64.b64decode('YnVpbHRpbnM=').decode('utf-8')), base64.b64decode('ZXhlYw==').decode('utf-8'))""")
    code += ';\u0674=""'
    return code

class ZeroObfuscator:
    def __init__(self):
        self._valid_identifiers = [chr(x) for x in range(1000) if self.set_variable_from_char(chr(x))]
        self.zeroobf = self.generate_var(100)
        self.obfcode = f"""
# https://github.com/werearecat/zeroobf
# obf code
base64 = __import__("{self.string_to_hex('base64')}")
builtins = __import__("{self.string_to_hex('builtins')}")

{self.zeroobf}var = ""
{self.zeroobf}var1 = ""
{self.zeroobf}var2 = ""
{self.zeroobf}var3 = 0
{self.zeroobf}\u0674\u0674 = getattr(builtins, '{self.string_to_hex('exec')}')
deobfuscate_string = lambda s: ''.join(chr(((ord(c) - 200) % 256)) for c in s)
""".replace("\u0674", "a")
        self.zeroexec = f"{self.zeroobf}\u0674\u0674"
        print("ZeroObfuscator initialized.")

    def set_variable_from_char(self, char):
        """
        Thực hiện exec để gán giá trị cho biến có tên là ký tự đầu vào.
        Nếu exec gây lỗi, hàm trả về False.
        """
        if len(char) != 1:
            raise ValueError("Input must be a single character")
        
        try:
            # Tạo lệnh exec để gán giá trị cho biến
            exec(f"{char} = '{char}'")
            # Trả về True nếu exec thành công
            return True
        except Exception:
            # Xử lý lỗi và trả về False nếu có lỗi xảy ra
            return False

    def generate_var(self, length=10):
        length = random.randint(10, 25)
        random_string = '\u0674' * length
        return random_string

    def string_to_hex(self, s):
        return ''.join(f'\\x{ord(c):02x}' for c in s)

    def string_to_hex_fake(self, s):
        length = random.randint(1, 5)
        random_string = '\u0674' * length
        return random_string

    def generate_random_zeroes(self, length):
        return '\u0E47' * length

    def obfuscate_code(self, code):
        encoded_lines = ""
        total_lines = len(code.splitlines())
        obfuscate_string = lambda s: ''.join(chr(((ord(c) + 200) % 256)) for c in s)
        print(f"Obfuscating code: {total_lines} lines total.")
        
        for i, line in enumerate(code.splitlines(), start=1):
            lmao = f"\n{self.zeroobf}\u0674\u0674('')" * 5
            encoded_line = self.string_to_hex(obfuscate_string(base64.b64encode(line.encode('utf-8')).decode()))
            encoded_lines_haha = obfcode(f"""
{self.string_to_hex_fake(encoded_line)} = "{self.string_to_hex_fake(encoded_line)}"
{self.zeroobf}var += base64.b64decode(deobfuscate_string("{encoded_line}")).decode() + "\\n"
{self.zeroobf}var2 += f"{self.generate_random_zeroes(25)}"
{self.zeroobf}var3 += 1
if {self.zeroobf}var3 == {total_lines}:
    {self.zeroexec}({self.zeroobf}var) if {len(str(code))} == len(str({self.zeroobf}var)) else None
    {self.zeroobf}var = ""
{lmao}
""")
            compressed_code = zlib.compress(encoded_lines_haha.encode()).hex()
            encoded_lines += encoded_lines_haha
            print(f"Processed line {i}/{total_lines}. Now {len(encoded_lines)} bytes")

        final_code_old = self.obfcode + encoded_lines
        final_code = self.obfcode + f"""\nexec(zlib.decompress(bytes.fromhex("{zlib.compress(encoded_lines.encode()).hex()}")).decode())"""
        
        return functionobf(pyminify(final_code_old))
        # return functionobf(pyminify(final_code))

def main():
    parser = argparse.ArgumentParser(description='Zero Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    
    args = parser.parse_args()
    
    print(f"Reading input file: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    
    obfuscator = ZeroObfuscator()
    obfuscated_code = obfuscator.obfuscate_code(code)
    
    print(f"Writing obfuscated code to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)

if __name__ == '__main__':
    main()
