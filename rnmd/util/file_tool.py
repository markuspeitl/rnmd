import os

def get_file_contents(path):
    if(path is None):
        return None
    with open(path, "r") as documentation_file:
        documentation_contents = documentation_file.read()

    return documentation_contents

def is_file_exists(path):
    if(path is None):
        return False
    return os.path.exists(path) and os.path.isfile(path)