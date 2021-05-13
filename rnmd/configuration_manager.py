import os
import json

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