import os
import argparse
import rnmd.extract_code

def compile_markdown(source_location, target_path):

    code, language = rnmd.extract_code.extract_code_from_doc(source_location)

    shebang = ""
    if("bash" in language):
        shebang = "#!/usr/bin/env bash"
    elif("python" in language):
        shebang = "#!/usr/bin/env python"
    elif("js" in language):
        shebang = "#!/usr/bin/env node"

    code = shebang + "\n" + code

    with open(target_path, "w+") as out_file:
        out_file.write(code)

    os.system("chmod +x " + target_path)

    #print("Compiled markdown to " + target_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Compile markdown bash documentation to executable program scripts"
    )
    parser.add_argument('source', help="Path of the documentation file")
    parser.add_argument('target', help="Output path for the resulting executable file")

    arguments = parser.parse_args()

    source = arguments.source
    target = arguments.target

    code = compile_markdown(source, target)