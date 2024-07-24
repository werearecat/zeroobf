import base64
import codecs
import marshal
import zlib

def xor_encrypt(codee, key=42):
    return ''.join(chr(ord(c) ^ key) for c in codee)

def obfuscate_string(s):
    return ''.join(chr(((ord(c) + 3) % 256)) for c in s)

def custom_substitution(codee):
    return ''.join(chr(ord(c) + 5) for c in codee)

def functionobf(x):
    x = f"""getattr(__import__(base64.b64decode('YnVpbHRpbnM=').decode('utf-8')), base64.b64decode('{base64.b64encode(x).decode()}').decode('utf-8'))"""
    return x.replace("base64", f"__import__('base64')")

def functionobfall(code):
    """Replace all built-in function names in the code with their obfuscated versions."""
    # Get a list of all built-in functions, excluding 'getattr' and '__import__'
    function_names = [name for name in dir(builtins) if callable(getattr(builtins, name)) and name not in ['getattr', '__import__']]

    # Replace each function name in the code with its obfuscated version
    for func_name in function_names:
        code = code.replace(func_name, functionobf(func_name))
    
    return code

def super_obfcode(codee):
    # Compile and marshal the code
    codee = functionobfall(codee)
    compiled_code = compile(codee, '<string>', 'exec')
    marshaled_code = marshal.dumps(compiled_code)
    # Apply Base64 encoding
    base64_encoded = base64.b64encode(marshaled_code).decode()
    # Apply XOR encryption
    xor_encrypted = xor_encrypt(base64_encoded)
    # Apply custom substitution
    substituted_code = custom_substitution(xor_encrypted)
    # Apply obfuscation
    obfuscated_code = obfuscate_string(substituted_code)
    # Apply zlib compression
    compressed_code = zlib.compress(obfuscated_code.encode())

    # Final decryption function (one line)
    final_code = f'import zlib, base64, marshal\n'\
        f'def xor_encrypt(codee, key=42):\n'\
        f'    return "".join(chr(ord(c) ^ key) for c in codee)\n'\
        f'def obfuscate_string(s):\n'\
        f'    return "".join(chr((ord(c) - 3) % 256) for c in s)\n'\
        f'def custom_substitution(codee):\n'\
        f'    return "".join(chr(ord(c) - 5) for c in codee)\n'\
        f'def decrypt_code(encrypted_code):\n'\
        f'    decompressed_code = zlib.decompress(encrypted_code).decode()\n'\
        f'    deobfuscated_code = obfuscate_string(decompressed_code)\n'\
        f'    unsubstituted_code = custom_substitution(deobfuscated_code)\n'\
        f'    base64_encoded = xor_encrypt(unsubstituted_code)\n'\
        f'    marshaled_code = base64.b64decode(base64_encoded)\n'\
        f'    compiled_code = marshal.loads(marshaled_code)\n'\
        f'    exec(compiled_code)\n'\
        f'decrypt_code({repr(compressed_code)})'

    return final_code

# Example usage
print(super_obfcode('print("Hello World!")'))
