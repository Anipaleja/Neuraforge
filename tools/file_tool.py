import os

def list_files(path='.'):
    return os.listdir(path)

def read_file(file):
    with open(file, 'r') as f:
        return f.read()

def write_file(file, content):
    with open(file, 'w') as f:
        f.write(content)