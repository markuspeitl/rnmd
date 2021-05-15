silent = False
force = False

def parse(parsed_args):
    global silent
    global force
    if('silent' in parsed_args and parsed_args.silent):
        silent = parsed_args.silent
    if('force' in parsed_args and parsed_args.force):
        force = parsed_args.force