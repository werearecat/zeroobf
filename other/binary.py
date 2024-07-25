def string_to_binary(s):
    return ''.join(format(ord(char), '08b') for char in s)

def obf_binary(code):
    decode_def = "def decode_bin(b):b=b.replace('ŏ','1').replace('ŏ̆','0');A=int(b,2);return A.to_bytes((A.bit_length()+7)//8,'big').decode()"
    binary_destory = string_to_binary(code).replace('0', 'ŏ̆').replace('1', 'ŏ')
    code = f"""
{decode_def}
exec(decode_bin("{binary_destory}"))
"""
    return code

print(obf_binary("print('hello :)')"))
