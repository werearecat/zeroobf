def obfcode(input_file, output_file):
    # Đọc file với mã hóa UTF-8
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Chuyển mỗi ký tự thành mã nhị phân 8 bit
    binary_code = ' '.join(format(ord(c), '08b') for c in code)
    
    # Thay thế 0 và 1 bằng ký tự Unicode
    binary_code_hidden = binary_code.replace("0", "\u0674").replace("1", "\u0E47")

    # Tạo mã nguồn để giải mã và thực thi
    obfuscated_code = f"""
# https://github.com/werearecat/zeroobf
# made with chatgpt :)
exec("".join(chr(int(b, 2)) for b in "{binary_code_hidden}".replace("\u0674", "0").replace("\u0E47", "1").split()))
    """.replace(" ", f"\t")
    
    # Ghi file với mã hóa UTF-8
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated_code)

obfcode('code.txt', 'code_obf.txt')
