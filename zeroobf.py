import random
import base64
import argparse
import zlib
from python_minifier import minify as pyminify

class ZeroObfuscator:
    def __init__(self):
        self._valid_identifiers = [chr(x) for x in range(1000) if self.set_variable_from_char(chr(x))]
        self.zeroobf = self.generate_var(100)
        self.obfcode = f"""
import base64
import zlib
# https://github.com/werearecat/zeroobf
# obf code
{self.zeroobf}var = ""
{self.zeroobf}var1 = ""
{self.zeroobf}var2 = ""
"""
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

    def generate_var(self, length=10):
        valid = random.choice(self._valid_identifiers)
        valid2 = random.choice(self._valid_identifiers)
        valid = valid * 10
        valid2 = valid2 * 10
        return ''.join(f'{valid}{valid2}_{random.randint(0, 255):02x}' for _ in range(length))

    def string_to_hex(self, s):
        return ''.join(f'\\x{ord(c):02x}' for c in s)

    def string_to_hex_fake(self, s):
        return ''.join(f'隐藏_{ord(c):02x}' for c in s)

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
"""
            compressed_code = zlib.compress(encoded_lines_haha.encode()).hex()
            encoded_lines += f"""\nexec(zlib.decompress(bytes.fromhex("{compressed_code}")).decode())"""
            print(f"Processed line {i}/{total_lines} Now {len(encoded_lines)} bytes")

        final_code = self.obfcode + encoded_lines
        final_code += f"\n\nexec({self.zeroobf}var)"
        print("minify code")
        minified_code = pyminify(final_code)
        print(f"minify {len(final_code)} bytes => {len(minified_code)} bytes")
        print("Code obfuscation complete.")
        return minified_code
