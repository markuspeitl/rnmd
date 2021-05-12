import os
import argparse
from script_extractor import extract_script_from_doc


parser = argparse.ArgumentParser(
    description="Compile markdown bash documentation to executable program scripts"
)

parser.add_argument('source', help="Source of the documentation file")

# Parse the arguments
arguments = parser.parse_args()

source = arguments.source

code = extract_script_from_doc(source)

print("PRINTING CODE:")
print(code+"\n")
print("RUNNING CODE:\n")
os.system(code)