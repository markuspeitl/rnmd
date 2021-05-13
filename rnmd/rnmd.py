#!/usr/bin/env python

import os
import argparse
import rnmd.runtime
import rnmd.make_proxy
import rnmd.compile_markdown
import rnmd.extract_code
import rnmd.setup_manager

def main():

    parser = argparse.ArgumentParser(
        description="Compile markdown bash documentation to executable program scripts"
    )

    basegroup = parser.add_mutually_exclusive_group()
    basegroup.add_argument('source', nargs='?', help="Source of the documentation file to consume - .md is executed when no other option specified later \
        possible to be a path or and URL")
    basegroup.add_argument('-setup','--setup', action="store_true", help="Setup the rnmd configuration and add make your proxies executable from anywhere")
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('-i','--install', help="Create an extensionless proxy for doc and install at a location inside path")
    group.add_argument('-p','--proxy', help="Create proxy file/fake binary to execute source document at location")
    group.add_argument('-b','--blocks', nargs='+', type=int, help="Execute specific code blocks")
    group.add_argument('-e','--extract', action="store_true", help="Print the extracted code that would be run")
    group.add_argument('-c','--compile', help="Compile to target file - for compiled languages")

    # Parse the arguments
    arguments = parser.parse_args()

    doc_source = arguments.source

    #ps | grep `echo $$` | awk '{ print $4 }'
    
    if(arguments.setup):
        #os.system("bash " + os.path.join(os.path.dirname(__file__),"setup-manager.sh"))
        rnmd.setup_manager.start_setup_process()
        exit()

    if(doc_source is None):
        print("rnmd.py: error: the following arguments are required: 'source' or '--setup'")
        exit()

    elif(arguments.install):
        install_name = arguments.install
        install_dir = os.path.join(os.path.expanduser('~'),"rndb-notebook", "bin")
        #doc_dir = os.path.join(Path.home(),"rndb-notebook", "docs")
        install_bin = os.path.join(install_dir, install_name)
        os.system("mkdir -p " + install_dir)
        print("target: " + install_bin)
        rnmd.make_proxy.make_proxy(doc_source, install_bin)
    elif(arguments.proxy):
        proxy_target = arguments.proxy
        rnmd.make_proxy.make_proxy(doc_source, proxy_target)
    elif(arguments.blocks):
        rnmd.runtime.run_markdown(doc_source)
    elif(arguments.extract):
        code = rnmd.extract_code.extract_code_from_doc(doc_source)
        print("Code extracted from file " + doc_source + ": \n")
        print(code)
    elif(arguments.compile):
        compile_target = arguments.compile
        rnmd.compile_markdown.compile_markdown(doc_source, compile_target)
    else:
        rnmd.runtime.run_markdown(doc_source)