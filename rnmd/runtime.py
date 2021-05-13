import os
import rnmd.extract_code

def run_markdown(source):
    code = rnmd.extract_code.extract_code_from_doc(source)

    print("PRINTING CODE:")
    print(code+"\n")
    print("RUNNING CODE:\n")
    os.system(code)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Run markdown contained code"
    )
    parser.add_argument('source', help="Source of the documentation file")
    arguments = parser.parse_args()
    source = arguments.source

    run_markdown(source)
