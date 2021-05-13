import os

from string import Template

current_script_dir = os.path.dirname(__file__)
installer_file_path = os.path.join(current_script_dir,"include-install-rnmd.sh")
template_file_path = os.path.join(current_script_dir,"proxy-template.txt")

with open(template_file_path, "r") as template_file:
    template_string = template_file.read()

with open(installer_file_path, "r") as installer_file:
    installer_code = installer_file.read()

#TODO replace by platform independent python script instead
proxy_template = Template(template_string)

def make_proxy(source_path, target_path, backup_path = None, relative = False, localInstall = False):

    #shebang = "#!/usr/bin/env python3"
    shebang = "#!/usr/bin/env bash"

    runner = ""
    runtime_path = "rnmd"

    if(localInstall):
        runner = "python3 "
        runtime_path = os.path.abspath(os.path.join(current_script_dir,"rnmd.py"))

    markdown_doc_path = os.path.abspath(source_path)

    if(relative):
        #Relative path from proxy file to markdown doc
        markdown_doc_path = os.path.relpath(markdown_doc_path, os.path.dirname(target_path));
        #Has to be added in bash so that the path is resolved from the proxies location (and not the caller directory)
        markdown_doc_path = os.path.join("`dirname $0`", markdown_doc_path)

    if(backup_path is None):
        backup_path = ""

    substitution_dict = { 
        'shebang':shebang,
        'installer_code': installer_code, 
        'runner': runner, 
        'runtime_path': runtime_path, 
        'markdown_doc_path': markdown_doc_path,
        'backup_path': backup_path
    }
    proxy_string = proxy_template.substitute(**substitution_dict)

    with open(target_path, "w+") as out_file:
        out_file.write(proxy_string)

    os.system("chmod +x " + target_path)

    print("Created proxy at: " + target_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Compile markdown bash documentation to executable program scripts"
    )

    parser.add_argument('source', help="Path of the documentation file")
    parser.add_argument('target', help="Output path for the resulting executable file")

    # Parse the arguments
    arguments = parser.parse_args()

    source = arguments.source
    target = arguments.target

    make_proxy(source,target)