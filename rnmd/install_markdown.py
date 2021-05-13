import os
import rnmd.make_proxy
import rnmd.configuration_manager
import shutil

backup_mode_enabled = True

def get_notebook_path():
    stored_notebook_path = rnmd.configuration_manager.get("NOTE_BOOK_DIR")

    if(stored_notebook_path is not None):
        return os.path.expanduser(stored_notebook_path)

    return stored_notebook_path

def backup_document(source_path, notebook_dir):
    notebook_doc_path = os.path.join(notebook_dir, "backup-doc")

    os.makedirs(notebook_doc_path, exist_ok=True)

    target_file = os.path.join(notebook_doc_path, os.path.basename(source_path))
    shutil.copyfile(source_path, target_file)
    return target_file

def handle_if_file_conflict(target_path):
    if(os.path.exists(target_path)):
        print("'" + target_path + "' already exists, do you want to overwrite it. (y/n)")
        answer = input()
        if(answer == "y"):
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

    stored_notebook_path = get_notebook_path()

    if(stored_notebook_path is None):
        print("Can not install document before a notebook path is defined!")
        print("Please run 'rnmd --setup' to setup the notebook path and make sure that ~/.config/rnmd/config.json exists")
        return

    notebook_bin_path = os.path.join(stored_notebook_path, "bin")
    target_path = os.path.join(notebook_bin_path, new_name)

    target_path = handle_if_file_conflict(target_path)

    if(target_path is None):
        return

    backup_path = None

    if(backup_mode_enabled):
        backup_path = backup_document(source_path, stored_notebook_path)

    print("Installing proxy to target: " + target_path)
    rnmd.make_proxy.make_proxy(source_path, target_path, backup_path=backup_path , relative = True)

    