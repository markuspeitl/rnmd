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
import rnmd.config.mode_options as mode_options
from rnmd.config.mode_printer import print_if
import os

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
    group.add_argument('-rn','--rename', help="Rename installed global proxy script")
    group.add_argument('-p','--proxy', help="Create proxy file/fake binary to execute source document at location")
    group.add_argument('-b','--blocks', nargs='+', type=int, help="Execute specific code blocks")
    #group.add_argument('-rl','--runlabel', nargs='+', type=int, help="Run block by its names (first comment of each block)")
    group.add_argument('-e','--extract', action="store_true", help="Print the extracted code that would be run")
    group.add_argument('-c','--compile', help="Compile to target file - for compiled languages")
    group.add_argument('-r','--remove', action="store_true", help="Remove installed markdown execution proxy")
    group.add_argument('-l','--list', action="store_true", help="List all markdown proxies installed in notebook")
    group.add_argument('-check','--check', action="store_true", help="Check if the specified documents exists")
    group.add_argument('-ba','--backup', action="store_true", help="Create a backup of the specified document")
    group.add_argument('-bt','--backupto', help="Create a backup of the source document at the backupto specified location")
    group.add_argument('-a','--args',  nargs='*', help="Arguments to pass to the runtime")

    parser.add_argument('-s','--silent', action="store_true", help="Do not print status updates or exceptions to std out")
    parser.add_argument('-f','--force', action="store_true", help="Force operation without asking in case of conflicts")
    parser.add_argument('-local','--local', action="store_true", help="For debugging write local instance of rnmd into proxy - for debugging")
    #parser.add_argument('-a','--add', action="store_true", help="Add local notebook to path")

    # Parse the arguments
    arguments = parser.parse_args()
    doc_source = arguments.source

    #For silent and force
    mode_options.parse(arguments)
    set_global_options()

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
        rnmd.install_markdown.install(doc_source, arguments.install, local_instance = arguments.local)
    elif(arguments.installportable):
        rnmd.install_markdown.install_portable(doc_source, arguments.installportable, local_instance = arguments.local)
    elif(arguments.installquick):
        rnmd.install_markdown.install(doc_source, local_instance = arguments.local)
    elif(arguments.remove):
        rnmd.install_markdown.remove_install(doc_source)
    elif(arguments.backup):
        rnmd.install_markdown.backup_document(doc_source)
    elif(arguments.backupto):
        backup_to(doc_source, arguments.backupto)
    elif(arguments.check):
        print(check_exists(doc_source))
    elif(arguments.proxy):
        proxy_target = arguments.proxy
        rnmd.make_proxy.make_proxy(doc_source, proxy_target, local_instance = arguments.local)
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
        rnmd.runtime.run_markdown(doc_source, arguments.args)

def set_global_options():
    rnmd.install_markdown.mode_options = mode_options
    rnmd.make_proxy.mode_options = mode_options

def check_exists(doc_source):
    return document_exists(doc_source)

def backup_to(source_doc, target_file_dir):
    if(source_doc is not target_file_dir):
        backup_location = rnmd.install_markdown.copy_document_to(source_doc, target_file_dir)
        if(backup_location is None):
            print_if("Failed to back up " + source_doc + " to dir " + target_file_dir +"\n Make sure both paths exist", mode_options)
        else:
            print_if("Successfully backed up " + source_doc + " to dir " + target_file_dir, mode_options)

def run_proxy(doc_path, backup_path, args, command = "rnmd", update_backup = False):

    print("Start run proxy process:")
    print(doc_path)
    print(backup_path)
    print(args)
    print(command)
    print(update_backup)

    if(check_exists(doc_path)):

        if(update_backup):
            mode_options.force = True
            mode_options.silent = True
            set_global_options()
            backup_to(doc_path, backup_path)

        if(args is None):
            args = []

        if(command == "rnmd"):
            
            all_args = [command, doc_path] + ["--args"] + args
            run_command = (" ").join(all_args)
            print("Running command: " + run_command)
            os.system(run_command)
            #rnmd.runtime.run_markdown(doc_path, args)
        else:
            all_args = [command, doc_path] + args
            run_command = (" ").join(all_args)
            print("Running command: " + run_command)
            os.system(run_command)
        
        return 

    if(backup_path is None):
        return

    print("The markdown file " + doc_path +" linked to by this proxy does not exist.")
    print("Did you move the file -> if so please reinstall for the new path by: ")
    print("rnmd NEW_MARKDOWN_PATH --install SCRIPTNAME")

    print("Do you want to try to run the backup instead? (y/n)")
    answer = input()
    if(answer != "y"):
        return run_proxy(backup_path, None, args, command, update_backup = False)