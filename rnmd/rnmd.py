#!/usr/bin/env python

import argparse
import rnmd.runtime
import rnmd.make_proxy
import rnmd.compile_markdown
import rnmd.extract_code
import rnmd.setup_manager
import rnmd.install_markdown
from rnmd.util.extract_document_content import document_exists
import rnmd

def main():

    parser = argparse.ArgumentParser(
        description="Compile markdown bash documentation to executable program scripts"
    )

    basegroup = parser.add_mutually_exclusive_group()
    basegroup.add_argument('source', nargs='?', help="Source of the documentation file to consume - .md is executed when no other option specified later \
        possible to be a path or and URL")
    basegroup.add_argument('-setup','--setup', action="store_true", help="Setup the rnmd configuration and add make your proxies executable from anywhere")
    basegroup.add_argument('-v','--version', action="store_true", help="Show rnmd version")
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument('-i','--install', help="Create an extensionless proxy for doc and install at a notbook location inside path")
    group.add_argument('-ip','--installportable', help="Moves the consumed document into the notebook and links the proxy so that the notbook can be transferred to another machine without breaking links")
    group.add_argument('-iq','--installquick', action="store_true", help="Installs the document to the notebook with the same name as the document")
    group.add_argument('-p','--proxy', help="Create proxy file/fake binary to execute source document at location")
    group.add_argument('-b','--blocks', nargs='+', type=int, help="Execute specific code blocks")
    group.add_argument('-e','--extract', action="store_true", help="Print the extracted code that would be run")
    group.add_argument('-c','--compile', help="Compile to target file - for compiled languages")
    group.add_argument('-r','--remove', action="store_true", help="Remove installed markdown execution proxy")
    group.add_argument('-l','--list', action="store_true", help="List all markdown proxies installed in notebook")
    group.add_argument('-check','--check', action="store_true", help="Check if the specified documents exists")
    group.add_argument('-ba','--backup', action="store_true", help="Create a backup of the specified document")
    group.add_argument('-bt','--backupto', help="Create a backup of the source document at the backupto specified location")

    #parser.add_argument('-s','--silent', help="Do not print status updates to std out")

    # Parse the arguments
    arguments = parser.parse_args()

    doc_source = arguments.source

    #ps | grep `echo $$` | awk '{ print $4 }'

    if(arguments.list):
        rnmd.install_markdown.list_installed()
        exit()
    if(arguments.setup):
        rnmd.setup_manager.start_setup_process()
        exit()
    if(arguments.version):
        print(rnmd.__version__)
        exit()
    if(doc_source is None):
        print("rnmd.py: error: the following arguments are required: 'source' or '--setup'")
        exit()
    elif(arguments.install):
        rnmd.install_markdown.install(doc_source, arguments.install)
    elif(arguments.installportable):
        rnmd.install_markdown.install_portable(doc_source, arguments.install)
    elif(arguments.installquick):
        rnmd.install_markdown.install(doc_source)
    elif(arguments.remove):
        rnmd.install_markdown.remove_install(doc_source)
    elif(arguments.backup):
        rnmd.install_markdown.backup_document(doc_source)
    elif(arguments.backupto):
        if(doc_source is not arguments.backupto):
            backup_location = rnmd.install_markdown.backup_document_to(doc_source, arguments.backupto)
            if(backup_location is None):
                print("Failed to back up " + doc_source + " to dir " + arguments.backupto +"\n Make sure both paths exist")
            else:
                print("Successfully backed up " + doc_source + " to dir " + arguments.backupto)
    elif(arguments.check):
        print(document_exists(doc_source))
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