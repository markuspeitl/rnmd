import argparse
import script_extractor

parser = argparse.ArgumentParser(
    description="Compile markdown bash documentation to executable program scripts"
)

parser.add_argument('source', help="Path of the documentation file")
parser.add_argument('target', help="Output path for the resulting executable file")

# Parse the arguments
arguments = parser.parse_args()

source = arguments.source
target = arguments.target

code = script_extractor.extract_script_from_doc(source)

with open(target, "w+") as out_file:
    out_file.write(code)
