import bz2

def obfuscate(content):
    code = """
def eexec():
    exec("print('hi')")

exec(eexec.__code__)

    """
