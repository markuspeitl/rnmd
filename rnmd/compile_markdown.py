import argparse
import rnmd.extract_code

def compile_markdown(source, target):

    code = rnmd.extract_code.extract_code_from_doc(source)

    with open(target, "w+") as out_file:
        out_file.write(code)

    print("Compiled markdown to " + out_file)

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

    code = compile_markdown(source,target)