import subprocess

def execute(command, inp=None):
    com = command.split()
    out = subprocess.run(com,capture_output=True, input = inp, text=True)
    return out.returncode
    