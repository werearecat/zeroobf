import random

def string_to_hex(s):
    return ''.join(f'\\x{ord(c):02x}' for c in s)

def obfcode(input_file, output_file):
    # Đọc file với mã hóa UTF-8
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Chuyển mỗi ký tự thành mã nhị phân 8 bit
    binary_code = ' '.join(format(ord(c), '08b') for c in code)

    length = 1
    a0 = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= length))
    a1 = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= length))
    space = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= length))
    fake = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= 1000))
    exectest = getattr(__import__('builtins'), 'exec')
    binary_code_hidden = binary_code[::-len(str(exectest))].replace("0", f"{a0}").replace("1", f"{a1}").replace(" ", f"{space}")

    # Tạo mã nguồn để giải mã và thực thi
    exec_ = "\u0674\u0674e\u0674\u0674x\u0674\u0674e\u0674\u0674c"

    obfuscated_code = f"""
'''
# https://github.com/werearecat/zeroobf
# made with chatgpt :)
{chr(10) * 1000}
'''
{exec_} = getattr(__import__('{string_to_hex("builtins")}'), '{string_to_hex("exec")}');{exec_}("".join(chr(int(b, 2)) for b in "{binary_code_hidden}"[::-len(str({len(str(exectest))}))].replace("{a0}", "0").replace("{a1}", "1").replace("{space}", " ").replace("{fake}", "{fake}").split()))
    """
    
    # Ghi file với mã hóa UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated_code)

obfcode('code.py', 'code_obf.py')
