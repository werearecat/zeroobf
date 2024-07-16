import random
import base64
import argparse
import zlib

class ZeroObfuscator:
    def __init__(self):
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
    
    def generate_var(self, length=10):
        return ''.join(f'__{random.randint(0, 255):02x}__zeroobf__' for _ in range(length))

    def string_to_hex(self, s):
        return ''.join(f'\\x{ord(c):02x}' for c in s)

    def string_to_hex_fake(self, s):
        return ''.join(f'__{ord(c):02x}__zeroobf___\\x00\\x00' for c in s)

    def generate_random_zeroes(self, length):
        return '\\x00' * length

    def obfuscate_code(self, code):
        encoded_lines = ""
        for line in code.splitlines():
            encoded_line = base64.b64encode(line.encode('utf-8')).decode()
            encoded_lines_haha = f"""
{self.zeroobf}var1 += "{self.string_to_hex_fake(encoded_line)}"
{self.zeroobf}var += base64.b64decode("{encoded_line}").decode() + "\\n"
{self.zeroobf}var2 += f"{self.generate_random_zeroes(20)}"
"""
            encoded_lines += f"""exec(zlib.decompress("{zlib.compress(encoded_lines_haha)}"))"""
        final_code = self.obfcode + encoded_lines
        final_code += f"\n\nexec({self.zeroobf}var)"
        return final_code

# obf code
# obfuscator = ZeroObfuscator()
# obfuscated_code = obfuscator.obfuscate_code("print('hi')")
def main():
    parser = argparse.ArgumentParser(description='Zero Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    
    obfuscator = ZeroObfuscator()
    obfuscated_code = obfuscator.obfuscate_code(code)
    
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)

if __name__ == '__main__':
    main()
