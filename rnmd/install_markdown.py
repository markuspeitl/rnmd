import os
import rnmd.make_proxy
import rnmd.configuration_manager
from rnmd.util.extract_document_content import extract_document_content


backup_mode_enabled = True
backup_web_mds = True

def backup_document(source_location):

    backup_path = rnmd.configuration_manager.get_backup_path()
    if(backup_path is None):
        return None

    target_file_path = os.path.join(backup_path, os.path.basename(source_location))

    source_doc_contents = extract_document_content(source_location)

    if(source_doc_contents is None):
        return None

    with open(target_file_path,"w+") as target_file:
        target_file.write(source_doc_contents)

    return target_file_path

def ask_yes(text):
    print(text)
    answer = input()
    if(answer == "y"):
        return True
    return False

def handle_if_file_conflict(target_path):
    if(os.path.exists(target_path)):
        if(ask_yes("'" + target_path + "' already exists, do you want to overwrite it. (y/n)")):
            return target_path
            
        print("Enter Different Name? (leave empty for aborting operation)")
        new_name = input()

        if(new_name is None or len(new_name) == 0):
            return None

        return os.path.join(os.path.dirname(target_path), new_name)

    return target_path

def install(source_path, new_name = None):

    if(new_name is None):
        new_name = os.path.splitext(os.path.basename(source_path))[0]

    notebook_bin_path = rnmd.configuration_manager.get_bin_path()
    if(notebook_bin_path is None):
        return None

    target_path = os.path.join(notebook_bin_path, new_name)

    target_path = handle_if_file_conflict(target_path)

    if(target_path is None):
        return

    backup_path = None

    if(backup_mode_enabled):
        backup_path = backup_document(source_path)

    print("Installing proxy to target: " + target_path)
    rnmd.make_proxy.make_proxy(source_path, target_path, backup_path=backup_path , relative = True)

def remove_install(target_name):

    notebook_bin_path = rnmd.configuration_manager.get_bin_path()
    if(notebook_bin_path is None):
        return None
    target_path = os.path.join(notebook_bin_path, target_name)

    if(not os.path.exists(target_path)):
        print("Target remove path " + target_path + " does not exist")
        return

    if(ask_yes("Are you sure you want to remove " + target_name + "? (y/n)")):
        
        os.remove(target_path)

def list_installed():
    notebook_bin_path = rnmd.configuration_manager.get_bin_path()
    if(notebook_bin_path is None):
        return None

    print("Printing installed markdown proxies: ")
    proxy_names = os.listdir(notebook_bin_path)
    for name in proxy_names:
        print(name)