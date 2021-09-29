import os
import rnmd.extract_code
import rnmd.compile_markdown

default_compile_dir="/tmp/rnmd"
os.makedirs(default_compile_dir, exist_ok=True)

def run_markdown(source, args):
    print(args)

    temp_compile_path = os.path.join(default_compile_dir, os.path.basename(source))

    rnmd.compile_markdown.compile_markdown(source, temp_compile_path)

    command = ""
    if(args is None):
        command = temp_compile_path
    else:
        args = list(map(lambda arg: "\""+arg+"\"",args))
        all_args = [temp_compile_path] + args
        command = (" ").join(all_args)

    os.system(command)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Run markdown contained code"
    )
    parser.add_argument('source', help="Source of the documentation file")
    arguments = parser.parse_args()
    source = arguments.source

    run_markdown(source)
