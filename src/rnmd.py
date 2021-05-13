#!/usr/bin/env python
import os
import argparse
import runtime
parser = argparse.ArgumentParser(
    description="Compile markdown bash documentation to executable program scripts"
)

parser.add_argument('source', help="Source of the documentation file to consume - .md is executed when no other option specified later \
    possible to be a path or and URL")
parser.add_argument('-p','--proxy', help="Create proxy file/fake binary to execute source document at location")
parser.add_argument('-c','--compile', help="Compile to target file - for compiled languages")

# Parse the arguments
arguments = parser.parse_args()

doc_source = arguments.source
proxy_target = arguments.proxy
compile_target = arguments.compile

if(proxy_target is None and compile_target is None):
    runtime.run_markdown(doc_source)
elif(proxy_target is not None):
    os.system("python3 mk_proxy.py " + doc_source)
elif(compile_target is not None):
    os.system("python3 compile_md.py " + doc_source)
