import os
import rnmd.make_proxy
import rnmd.configuration_manager
from rnmd.util.extract_document_content import extract_document_content, document_exists
from rnmd.util.file_tool import is_file_exists

backup_mode_enabled = True
backup_web_mds = True
delete_portable_src = False

def backup_document(source_doc_location):

    if(not document_exists(source_doc_location)):
        raise Exception("Invalid Path: Can not Wback up document that does not exist: " + source_doc_location)

    backup_path = rnmd.configuration_manager.get_backup_path()
    if(backup_path is None):
        raise Exception("Could not find notebook backup path in config.")

    return copy_document_to(source_doc_location, backup_path)

def path_has_extension(path):
    path_tuple = os.path.splitext(path)
    return path_tuple is not None and len(path_tuple) > 1 and len(path_tuple[1]) > 0

def valid_full_path_or_join(file_or_dir_path, join_file_name):
    if(path_has_extension(file_or_dir_path)):
        target_file_path = file_or_dir_path
        target_dir_path = os.path.dirname(file_or_dir_path)
    else:
        target_file_path = os.path.join(file_or_dir_path, join_file_name)
        target_dir_path = file_or_dir_path
        
    if(not os.path.exists(target_dir_path) or not os.path.isdir(target_dir_path)):
        raise Exception("Specified directory path (for file target) does not exist or is no directory.")

    return target_file_path

#Target patch = directory path or full file path
def copy_document_to(source_doc_location, target_path):

    if(not document_exists(source_doc_location)):
        raise Exception("Invalid Path: Can not copy document that does not exist: " + source_doc_location)

    source_doc_contents = extract_document_content(source_doc_location)
    if(source_doc_contents is None):
        raise Exception("Failed to read document contents.")

    source_doc_name = os.path.basename(source_doc_location)
    target_file_path = valid_full_path_or_join(source_doc_name, target_path)
    if(target_file_path is None):
        raise Exception("Failed to find a path to copy the document to.")

    with open(target_file_path,"w+") as target_file:
        target_file.write(source_doc_contents)

    return target_file_path

def move_document_to(source_doc_location, target_path):
    target_path = copy_document_to(source_doc_location, target_path)
    if(target_path is not None and delete_portable_src and is_file_exists(source_doc_location) and is_file_exists(target_path)):
        os.remove(source_doc_location)

    return target_path

def move_document_to_portable(source_doc_location):
    notebook_portable_path = rnmd.configuration_manager.get_portable_path()
    if(notebook_portable_path is None):
        raise Exception("Could not find notebook portable path in config.")

    return move_document_to(source_doc_location, notebook_portable_path)

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
            raise Exception("Overwrite operation aborted by user.")

        return os.path.join(os.path.dirname(target_path), new_name)

    return target_path

def find_bin_proxy_path(name_suggestion):
    notebook_bin_path = rnmd.configuration_manager.get_bin_path()
    if(notebook_bin_path is None):
        raise Exception("Could not find notebook bin path in config.")

    target_path = os.path.join(notebook_bin_path, name_suggestion)

    return handle_if_file_conflict(target_path)

def find_bin_proxy_path(source_file_path, name_suggestion):
    if(name_suggestion is None):
        new_name = os.path.splitext(os.path.basename(source_file_path))[0]

    target_path = find_bin_proxy_path(new_name)
    return target_path

def install(source_path, new_name = None):
    target_path = find_bin_proxy_path(source_path, new_name)
    if(target_path is None):
        raise Exception("Failed to find a path to save the proxy script to.")

    backup_path = None
    if(backup_mode_enabled):
        backup_path = backup_document(source_path)

    print("Installing proxy to target: " + target_path)
    rnmd.make_proxy.make_proxy(source_path, target_path, backup_path=backup_path , relative = True)

def install_portable(source_path, new_name = None):
    target_path = find_bin_proxy_path(source_path, new_name)
    if(target_path is None):
        raise Exception("Failed to find a path to save the proxy script to.")

    moved_document_path = move_document_to_portable(source_path)
    if(moved_document_path is None):
        raise Exception("Failed to move source document to portable directory in notebook")

    print("Installing proxy to target: " + target_path)
    rnmd.make_proxy.make_proxy(moved_document_path, target_path, relative = True)

def remove_install(target_name):

    notebook_bin_path = rnmd.configuration_manager.get_bin_path()
    if(notebook_bin_path is None):
        raise Exception("Could not find notebook bin path in config.")

    target_path = os.path.join(notebook_bin_path, target_name)

    if(not os.path.exists(target_path)):
        raise Exception("Target remove path " + target_path + " does not exist")

    if(ask_yes("Are you sure you want to remove " + target_name + "? (y/n)")):
        
        os.remove(target_path)

def list_installed():
    notebook_bin_path = rnmd.configuration_manager.get_bin_path()
    if(notebook_bin_path is None):
        raise Exception("Could not find notebook bin path in config.")

    print("Printing installed markdown proxies: ")
    proxy_names = os.listdir(notebook_bin_path)
    for name in proxy_names:
        print(name)