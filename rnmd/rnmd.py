#!/usr/bin/env python
import os
import argparse
import rnmd.runtime
import rnmd.make_proxy
import rnmd.compile_markdown

def main():

    parser = argparse.ArgumentParser(
        description="Compile markdown bash documentation to executable program scripts"
    )

    parser.add_argument('source', help="Source of the documentation file to consume - .md is executed when no other option specified later \
        possible to be a path or and URL")
    parser.add_argument('-p','--proxy', help="Create proxy file/fake binary to execute source document at location")
    parser.add_argument('-c','--compile', help="Compile to target file - for compiled languages")
    parser.add_argument('-p','--print', help="Print the extracted code that would be run")
    parser.add_argument('-b','--block', help="Execute specific code blocks")
    parser.add_argument('-i','--install', help="Create an extensionless proxy for doc and install at a location inside path")

    # Parse the arguments
    arguments = parser.parse_args()

    doc_source = arguments.source
    proxy_target = arguments.proxy
    compile_target = arguments.compile

    if(proxy_target is None and compile_target is None):
        rnmd.runtime.run_markdown(doc_source)
    elif(proxy_target is not None):
        rnmd.make_proxy.make_proxy(doc_source, proxy_target)
    elif(compile_target is not None):
        rnmd.compile_markdown.compile_markdown(doc_source, compile_target)