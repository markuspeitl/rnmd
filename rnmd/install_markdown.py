import os
import rnmd.make_proxy
import rnmd.configuration_manager

def get_notebook_path():
    """notebook_path = os.path.join(os.path.expanduser('~'), "rndb-notebook")

    if not os.path.exists(notebook_path):
        os.makedirs(notebook_path, exist_ok=True)

    notebook_bin_path = os.path.join(notebook_path, "bin")
    if not os.path.exists(notebook_bin_path):
        os.makedirs(notebook_bin_path, exist_ok=True)

    return notebook_path"""

    stored_notebook_path = rnmd.configuration_manager.get("NOTE_BOOK_DIR")

    if(stored_notebook_path is not None):
        return os.path.expanduser(stored_notebook_path)

    return stored_notebook_path

def install(source_path, new_name = None):

    if(new_name is None):
        new_name = os.path.splitext(os.path.basename(source_path))[0]

    stored_notebook_path = get_notebook_path()

    if(stored_notebook_path is None):
        print("Can not install document before a notebook path is defined!")
        print("Please run 'rnmd --setup' to setup the notebook path and make sure that ~/.config/rnmd/config.json exists")
        return

    notebook_bin_path = os.path.join(get_notebook_path(), "bin")
    target_path = os.path.join(notebook_bin_path, new_name)

    print("Installing proxy to target: " + target_path)
    rnmd.make_proxy.make_proxy(source_path, target_path, relative = True)