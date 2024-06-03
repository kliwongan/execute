# Execute code within safe sandbox
import ast
import resource
import subprocess
import os

"""
Security concepts here were taken from: 
https://healeycodes.com/running-untrusted-python-code
https://stackoverflow.com/questions/3068139/how-can-i-sandbox-python-in-pure-python

I would've tried somehow patching in a virtual machine or using
the (updated) PyPy sandbox project to execute the code
instead of what I have here, but I didn't have time to rig it up.
An interesting concept would have been to run the code on a WebAssembly sandbox
on the browser instead of in the backend
"""

MEMORY_LIMIT = 1
CPU_TIME_LIMIT = 60
WRITE_LIMIT = 2000

BAD_CALLS = {"exec", "eval"}
GOOD_IMPORTS = {"pandas", "scipy"}


def set_mem_limit():
    # virtual memory
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
    # cpu time
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_TIME_LIMIT, CPU_TIME_LIMIT))
    # write limit i.e. don't allow an infinite stream to stdout/stderr
    resource.setrlimit(resource.RLIMIT_FSIZE, (WRITE_LIMIT, WRITE_LIMIT))


def check_unsafe_code(code: str):
    """
    Checks if the code is unsafe (or not) by
    parsing the code in an AST and checking for a list of
    undesireable code constructs

    Returns True if unsafe, False otherwise
    """
    tree = ast.parse(code)
    for i in ast.walk(tree):
        if isinstance(i, ast.Call) and i.func.id in BAD_CALLS:
            print(i)
            return True
        if isinstance(i, ast.ImportFrom) and i.module not in GOOD_IMPORTS:
            print(i)
            return True
        if isinstance(i, ast.Import):
            print(i)
            for name in i.names:
                if name.name not in GOOD_IMPORTS:
                    return True

    return False


def exec_code_secure(code: str):
    """
    Executes the code in a sandbox and returns the output
    of the code execution
    """
    # set_mem_limit()
    output = ""
    try:
        with open("temp.py", "w") as text_file:
            text_file.write(code)
        result = subprocess.run(["python3", "temp.py"], capture_output=True)
        os.remove("temp.py")
        output += "======== OUT ========= \n"
        output += result.stdout.decode("utf-8")
        output += "\n"
        output += "======== ERR ========= \n"
        output += result.stderr.decode("utf-8")
        output += "\n"
    except Exception as e:
        # Cleanup
        if os.path.isfile("temp.py"):
            os.remove("temp.py")
        output = "Error in executing code!"
        print(e)

    return output
