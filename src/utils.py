def file_name(path):
    return path.split("/")[-1]


def is_locked(path):
    return path.endswith(".locked")