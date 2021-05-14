import os

def get_file_contents(path):
    with open(path, "r") as documentation_file:
        documentation_contents = documentation_file.read()

    return documentation_contents

def is_file_exists(path):
    return os.path.exists(path) and os.path.isfile(path)