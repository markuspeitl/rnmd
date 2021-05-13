from sys import platform
import os
import rnmd.configuration_manager

default_notebook_path = os.path.join(os.path.expanduser('~'),"rndb-notebook")

def input_confirmed(input):
    return input == "y"

def prompt_notebook_location():
    
    print("The default notebook markdown proxy code installation location is: " + default_notebook_path + "\n")
    print("Do you want to keep it that way? (y/n)")
    answer = input()
    if(input_confirmed(answer)):
        return default_notebook_path

    print("Please enter the path you want to choose: \n")
    entered_path = os.path.expanduser(input())

    if(os.path.isdir(entered_path)):
        return entered_path

    if not os.path.exists(entered_path):
        print("The directory you entered does not exist - do you want to create it? (y/n)")
        confirm_create = input()
        if(input_confirmed(confirm_create)):
            os.makedirs(entered_path, exist_ok=True)
            return entered_path

    print("Invalid directory - restarting \n")
    prompt_notebook_location()

def prompt_shell_config():
    print("\nPlease enter the path to the configuration file of your current shell.")
    print("Common values are ~/.bashrc, ~/.zshrc, ~/.profile")

    entered_path = os.path.expanduser(input())
    isFile = os.path.isfile(entered_path)
    if(isFile):
        return entered_path

    print(entered_path + " is not a file or does not exist - restarting")

    return prompt_shell_config()

def prompt_add_path(notebook_path):
    selected_notebook_bin_path = os.path.join(notebook_path,"bin")
    if not os.path.exists(selected_notebook_bin_path):
        os.makedirs(selected_notebook_bin_path, exist_ok=True)
    print("Do you want to add " + selected_notebook_bin_path + " to you path?")
    print("This will make markdown files installed with rnmd executable from anywhere on your system. (y/n)")
    add_to_path = input()
    if(not input_confirmed(add_to_path)):
        print("No path configured - installed files will have to be located inside your notebook to be executed")
        return None

    shell_config_location = prompt_shell_config()

    with open(shell_config_location,"a") as sh_config_file:
        comment = "#This entry makes the scripts installed by rnmd available to be run directly from anywhere\n"
        path_export = "export PATH=" + selected_notebook_bin_path + ":$PATH"
        
        with open(shell_config_location,"r") as sh_config_read_file:

            profile_contents = sh_config_read_file.read()
            if(path_export in profile_contents):
                print("Path export already found in selected profile configuration file - skipping adding line!")
                return selected_notebook_bin_path
        
        path_extension_string = comment + path_export

        sh_config_file.write(path_extension_string + "\n")

        print("Successfully added following lines to your " + shell_config_location + "\n")
        print(path_extension_string + "\n")

        #Add to current shell session as well
        #os.system(path_export)
        #os.system(". " + shell_config_location)

    return selected_notebook_bin_path

def is_platform_supported():
    if(platform == "linux"):
        return True
    elif(platform == "darwin"):
        print("OSX is not supported as platform yet - exiting\n")
        return False
    elif(platform == "win32"):
        print("Windows is not supported as platform yet - exiting\n")
        return False

def start_setup_process():

    platform_supported = is_platform_supported()
    if(not platform_supported):
        return

    selected_notebook_path = prompt_notebook_location();
    if not os.path.exists(selected_notebook_path):
        os.makedirs(selected_notebook_path, exist_ok=True)

    print("Storing notebook location in rnmd configuration at: " + rnmd.configuration_manager.get_config_path())
    rnmd.configuration_manager.set("NOTE_BOOK_DIR", selected_notebook_path)

    print("\nYou chose: " + selected_notebook_path + " as your notebook path.\n\n")

    added_path = prompt_add_path(selected_notebook_path)
    if(added_path is not None):
        print(added_path + " successfully added to your PATH environment\n")

    print("RNMD markdown runtime (install module) setup finished.")
    print("Please restart your terminal for changes to take effect.")

    #CURRENT_SHELL=$(ps | grep `echo $$` | awk '{ print $4 }')
    #echo "Detected shell is $CURRENT_SHELL"

if __name__ == "__main__":
    start_setup_process();