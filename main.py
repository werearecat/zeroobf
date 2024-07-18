import random
import base64
import argparse
import zlib

class ZeroObfuscator:
    def __init__(self):
        self._valid_identifiers = [chr(x) for x in range(1000) if self.set_variable_from_char(chr(x))]
        self.zeroobf = self.generate_var()
        self.obfcode = f"""
import base64
import zlib
# https://github.com/werearecat/zeroobf
# obf code
{self.zeroobf}var = ""
{self.zeroobf}var1 = ""
{self.zeroobf}var2 = ""
{self.zeroobf}var3 = 0
{self.zeroobf}隐藏 = exec
"""
        self.zeroexec = f"{self.zeroobf}隐藏"
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
        except Exception as e:
            # Xử lý lỗi và trả về False nếu có lỗi xảy ra
            return False

    def generate_var(self):
        length = random.randint(100, 250)
        return '\u200b' * length

    def string_to_hex(self, s):
        return ''.join(f'\\x{ord(c):02x}' for c in s)

    def string_to_hex_fake(self, s):
        return ''.join(f'隐藏_{ord(c):02x}' for _ in s)

    def generate_random_zeroes(self, length):
        return '\\x00' * length

    def obfuscate_code(self, code):
        encoded_lines = ""
        total_lines = len(code.splitlines())
        print(f"Obfuscating code: {total_lines} lines total.")
        
        for i, line in enumerate(code.splitlines(), start=1):
            encoded_line = base64.b64encode(line.encode('utf-8')).decode()
            encoded_lines_haha = f"""
{self.zeroobf}var1 += "{self.string_to_hex_fake(encoded_line)}"
{self.zeroobf}var += base64.b64decode("{encoded_line}").decode() + "\\n"
{self.zeroobf}var2 += f"{self.generate_random_zeroes(20)}"
{self.zeroobf}var3 += 1
if {self.zeroobf}var3 == {total_lines}:
    {self.zeroexec}({self.zeroobf}var)
    {self.zeroobf}var = ""
"""
            encoded_lines += encoded_lines_haha
            print(f"Processed line {i}/{total_lines} Now {len(encoded_lines)} bytes")

        final_code_old = self.obfcode + encoded_lines
        final_code = self.obfcode + f"""\nexec(zlib.decompress(bytes.fromhex("{zlib.compress(encoded_lines.encode()).hex()}")).decode())"""
        
        return final_code_old

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
