import os

def read_file(path):
    with open(path, "rb") as f:
        return f.read()


def write_file(path, data):
    with open(path, "wb") as f:
        f.write(data)


def restore_original(path, data):
    # remove ONLY .locked extension
    if path.endswith(".locked"):
        path = path[:-7]

    write_file(path, data)
    return path