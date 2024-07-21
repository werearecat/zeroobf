import random

def obfcode(input_file, output_file):
    # Đọc file với mã hóa UTF-8
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Chuyển mỗi ký tự thành mã nhị phân 8 bit
    binary_code = ' '.join(format(ord(c), '08b') for c in code)

    length = 1
    0 = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= length))
    1 = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= length))
    space = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= length))
    trash = "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= 1000))
    binary_code_hidden = binary_code.replace("0", f"{0}").replace("1", f"{1}").replace(" ", f"{space}")

    # Tạo mã nguồn để giải mã và thực thi
    obfuscated_code = f"""
# https://github.com/werearecat/zeroobf
# made with chatgpt :)
exec("".join(chr(int(b, 2)) for b in "{trash}{binary_code_hidden}{trash}".replace("{0}", "0").replace("{1}", "1").replace("{space}", " ").replace("{trash}", "").split()))
    """
    
    # Ghi file với mã hóa UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated_code)

obfcode('code.txt', 'code_obf.txt')
