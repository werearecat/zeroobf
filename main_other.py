import random
import base64
import argparse
import zlib
from python_minifier import minify as pyminify
import marshal

def encryptcode(codee):
    # Tối giản mã nguồn (minify)
    print(f"{len(codee)} bytes no minify")
    codee = pyminify(codee)
    print(f"{len(codee)} bytes minify")
    compliecode = compile(codee, '<string>', 'exec')
    dump = marshal.dumps(compliecode)
    dump_repr = repr(dump)  # Chuyển đổi thành chuỗi biểu diễn
    return f"exec(__import__('marshal').loads({dump_repr}))"

def obfcode(input_file, output_file):
    # Đọc file với mã hóa UTF-8
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Chuyển mỗi ký tự thành mã nhị phân 8 bit
    binary_code = ' '.join(format(ord(c), '08b') for c in code)
    
    # Thay thế 0 và 1 bằng ký tự Unicode
    binary_code_hidden = binary_code.replace("0", "\\t").replace("1", "\\r").replace(" ", "\\n")

    # Tạo mã nguồn để giải mã và thực thi
    obfuscated_code = f"""
# https://github.com/werearecat/zeroobf
# made with chatgpt :)
exec("".join(chr(int(b, 2)) for b in "{binary_code_hidden}".replace("\\t", "0").replace("\\r", "1").replace("\\n", " ").split()))
    """
    
    print(f"{len(str(obfuscated_code))} bytes binary obf")
    # Ghi file với mã hóa UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated_code)

def obfcodee(s):
    code = """
# https://github.com/werearecat/zeroobf
# no name :)
\u0674 = '';
"""
    code += ''.join(f"""\u0674+='\\x{ord(c):02x}';""" for c in s)
    code += 'exec(\u0674)'
    code += ';\u0674=""'
    print(f"{len(str(code))} bytes hex")
    return code

class ZeroObfuscator:
    def __init__(self):
        self._valid_identifiers = [chr(x) for x in range(1000) if self.set_variable_from_char(chr(x))]
        self.zeroobf = self.generate_var(100)
        self.obfcode = f"""
# https://github.com/werearecat/zeroobf
# obf code

base64 = __import__("{self.string_to_hex("base64")}")

{self.zeroobf}var = ""
{self.zeroobf}var1 = ""
{self.zeroobf}var2 = ""
{self.zeroobf}var3 = 0
{self.zeroobf}\u0674\u0674 = getattr(__import__('{self.string_to_hex("builtins")}'), '{self.string_to_hex("exec")}')
deobfuscate_string = lambda s: ''.join(chr(((ord(c) - 200) % 256)) for c in s)

"""
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
        except Exception as e:
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
            encoded_lines_haha = f"""
{self.string_to_hex_fake(encoded_line)} = "{self.string_to_hex_fake(encoded_line)}"
{self.zeroobf}var += base64.b64decode(deobfuscate_string("{encoded_line}")).decode() + "\\n"
{self.zeroobf}var2 += f"{self.generate_random_zeroes(25)}"
{self.zeroobf}var3 += 1
if {self.zeroobf}var3 == {total_lines}:
    {self.zeroexec}({self.zeroobf}var) if {len(str(code))} == len(str({self.zeroobf}var)) else None
    {self.zeroobf}var = ""
{lmao}
"""
            compressed_code = zlib.compress(encoded_lines_haha.encode()).hex()
            encoded_lines += encoded_lines_haha
            print(f"Processed line {i}/{total_lines} Now {len(encoded_lines)} bytes")

        final_code_old = self.obfcode + encoded_lines
        final_code = self.obfcode + f"""\nexec(zlib.decompress(bytes.fromhex("{zlib.compress(encoded_lines.encode()).hex()}")).decode())"""
        
        return final_code_old.replace("var1", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("var2", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("var3", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("var", f"\u0674\u0674\u0674\u0674\u0674\u0674").replace("deobfuscate_string", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("base64", f"\u0674\u0674\u0674\u0674_\u0674\u0674_\u0674\u0674")
        # return final_code.replace("var1", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("var2", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("var3", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("var", f"\u0674\u0674\u0674\u0674\u0674\u0674").replace("deobfuscate_string", f"\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674\u0674").replace("base64", f"\u0674\u0674\u0674\u0674_\u0674\u0674_\u0674\u0674")

def main():
    parser = argparse.ArgumentParser(description='Zero Obfuscator')
    parser.add_argument('-i', '--input', required=True, help='Input file')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    
    args = parser.parse_args()
    
    print(f"Reading input file: {args.input}")
    with open(args.input, 'r', encoding='utf-8') as file:
        code = file.read()
    
    obfuscator = ZeroObfuscator()
    obfuscated_code = encryptcode(obfcodee(obfuscator.obfuscate_code(code)))
    
    print(f"Writing obfuscated code to: {args.output}")
    with open(args.output, 'w', encoding='utf-8') as file:
        file.write(obfuscated_code)
    obfcode(args.output, args.output)

if __name__ == '__main__':
    main()
