def print_if(text, mode_options):
    if(mode_options is None or not mode_options.silent):
        print(text)