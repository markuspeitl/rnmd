import os
import json
import rnmd.config.defaults as defaults

configuration_dir_path = os.path.join(os.path.expanduser('~'), ".config", "rnmd")
configuration_file_path = os.path.join(configuration_dir_path, "config.json")

def setup_configuration():
    if not os.path.exists(configuration_dir_path):
        os.makedirs(configuration_dir_path, exist_ok=True)

def get_config():
    if(os.path.exists(configuration_file_path)):
        with open(configuration_file_path, "r") as config_read_file:
            config_content_string = config_read_file.read()
            return json.loads(config_content_string)
    return {}

def save_config(config):

    setup_configuration()
    with open(configuration_file_path, "w+") as config_write_file:
        
        config_json_string = json.dumps(config)
        config_write_file.write(config_json_string)

def get_config_path():
    return configuration_file_path
    
def set(key, value):
    config = get_config()
    config[key] = value
    save_config(config)

def get(key):
    config = get_config()
    if(key not in config):
        return None
    return config[key]


# Get specific directories

def get_config_dir_entry(key):
    dir_path = get(key)

    if(dir_path is None):
        return None

    expanded_path = os.path.expanduser(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    return expanded_path

def get_notebook_path():
    stored_notebook_path = get_config_dir_entry(defaults.notebook_key)

    if(stored_notebook_path is None):
        print("Can not get notebook path before it is defined!")
        print("Please run 'rnmd --setup' to setup the notebook path and make sure that ~/.config/rnmd/config.json exists")
        
    return stored_notebook_path

def get_bin_path():
    stored_bin_path = get_config_dir_entry(defaults.bin_key)

    if(stored_bin_path is None):
        print("Can not install document before a notebook path is defined!")
        print("Please run 'rnmd --setup' to setup the notebook path and make sure that ~/.config/rnmd/config.json exists")
        
    return stored_bin_path

def get_portable_path():
    stored_portable_path = get_config_dir_entry(defaults.portable_key)

    if(stored_portable_path is None):
        print("Can not portable install document before a notebook path is defined!")
        print("Please run 'rnmd --setup' to setup the notebook path and make sure that ~/.config/rnmd/config.json exists")
        
    return stored_portable_path

def get_backup_path():
    backup_path = get_config_dir_entry(defaults.backup_key)

    if(backup_path is None):
        print("Can not backup document before a notebook path is defined!")
        print("Please run 'rnmd --setup' to setup the notebook path and make sure that ~/.config/rnmd/config.json exists")
        
    return backup_path