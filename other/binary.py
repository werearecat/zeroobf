import random

def obfcode(input_file, output_file):
    # Đọc file với mã hóa UTF-8
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Chuyển mỗi ký tự thành mã nhị phân 8 bit
    binary_code = ''.join(format(ord(c), '08b') for c in code)

    # Tạo các ký tự tàng hình và ký tự vớ vẩn
    a0 = chr(random.choice([0x200B, 0x200C, 0x200D, 0xFEFF]))
    a1 = chr(random.choice([0x200B, 0x200C, 0x200D, 0xFEFF]))
    space = chr(random.choice([0x200B, 0x200C, 0x200D, 0xFEFF]))
    trash = ''.join(random.choices([chr(x) for x in range(0x2000, 0x200F)] + [chr(x) for x in range(0xFEFF, 0xFFFF)] + [chr(x) for x in range(0x0000, 0x001F)], k=1000))

    # Thay thế các bit nhị phân bằng các ký tự tàng hình và thêm ký tự vớ vẩn
    binary_code_hidden = binary_code.replace("0", a0).replace("1", a1).replace(" ", space)
    obfuscated_code = f"""
# https://github.com/werearecat/zeroobf
# made with chatgpt :)
exec("".join(chr(int(b, 2)) for b in "{trash}{binary_code_hidden}{trash}".replace("{a0}", "0").replace("{a1}", "1").replace("{space}", " ").split()))
    """

    # Ghi file với mã hóa UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated_code)

obfcode('code.txt', 'code_obf.txt')
