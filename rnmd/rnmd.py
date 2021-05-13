#!/usr/bin/env python

import argparse
import rnmd.runtime
import rnmd.make_proxy
import rnmd.compile_markdown
import rnmd.extract_code

def main():

    defaultInstallDir="~/.rnmd-proxies"

    parser = argparse.ArgumentParser(
        description="Compile markdown bash documentation to executable program scripts"
    )

    parser.add_argument('source', help="Source of the documentation file to consume - .md is executed when no other option specified later \
        possible to be a path or and URL")
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i','--install', action="store_true", help="Create an extensionless proxy for doc and install at a location inside path")
    group.add_argument('-p','--proxy', help="Create proxy file/fake binary to execute source document at location")
    group.add_argument('-b','--block', help="Execute specific code blocks", type=int)
    group.add_argument('-e','--extract', action="store_true", help="Print the extracted code that would be run")
    group.add_argument('-c','--compile', help="Compile to target file - for compiled languages")

    # Parse the arguments
    arguments = parser.parse_args()

    doc_source = arguments.source
    proxy_target = arguments.proxy
    compile_target = arguments.compile


    if(arguments.install):
        print("Not Implemented")
    elif(arguments.proxy):
        rnmd.make_proxy.make_proxy(doc_source, proxy_target)
    elif(arguments.block):
        rnmd.runtime.run_markdown(doc_source)
    elif(arguments.extract):
        code = rnmd.extract_code.extract_code_from_doc(doc_source)
        print("Code extracted from file " + doc_source + ": \n")
        print(code)
    elif(arguments.compile):
        rnmd.compile_markdown.compile_markdown(doc_source, compile_target)
    else:
        rnmd.runtime.run_markdown(doc_source)