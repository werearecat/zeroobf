import random
import base64
import argparse
import zlib

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
{self.zeroobf}var3 = 0
"""
        self.zeroexec = f"{self.zeroobf}隐藏"
        self.zeroif = f"{self.zeroobf}隐藏_"
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
        length = random.randint(100, 250)
        random_string = '\t' * length
        return random_string

    def string_to_hex(self, s):
        return ''.join(f'\\x{ord(c):02x}' for c in s)

    def string_to_hex_fake(self, s):
        return ''.join(f'\t\t\t\t\t' for c in s)

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
{self.zeroif} {self.zeroobf}var3 == {total_lines}:
    {self.zeroexec}({self.zeroobf}var)
    {self.zeroobf}var = ""
"""
            compressed_code = zlib.compress(encoded_lines_haha.encode()).hex()
            encoded_lines += encoded_lines_haha
            print(f"Processed line {i}/{total_lines} Now {len(encoded_lines)} bytes")

        final_code_old = self.obfcode + encoded_lines
        final_code = self.obfcode + f"""\nexec(zlib.decompress(bytes.fromhex("{zlib.compress(encoded_lines.encode()).hex()}")).decode())"""
        
        return final_code_old.replace("var1", f"\t\t\t\t").replace("var2", f"\t\t\t\t\t").replace("var3", f"\t\t\t\t\t\t").replace("var", f"\t\t\t")
        # return final_code.replace("var1", f"\t\t\t\t").replace("var2", f"\t\t\t\t\t").replace("var3", f"\t\t\t\t\t\t").replace("var", f"\t\t\t")
