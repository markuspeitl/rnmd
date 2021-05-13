import os

from string import Template
template = Template(
    """
    if [ -f "$installer_location" ]; then
        $install_runner $installer_location
    fi
    $runner $runtime_path $doc_path
    """
)

debugging = False
current_script_dir = os.path.dirname(__file__)

def make_proxy(source_path, target_path, relative=False, localInstall=False):

    runner = ""
    runtime_path = "rnmd"

    if(localInstall):
        runner = "python3 "
        runtime_path = os.path.abspath(os.path.join(current_script_dir,"rnmd.py"))

    doc_path = os.path.abspath(source_path)

    if(relative):
        #Relative path from proxy file to markdown doc
        doc_path = os.path.relpath(doc_path, os.path.dirname(target_path));
        #Has to be added in bash so that the path is resolved from the proxies location (and not the caller directory)
        doc_path = os.path.join("`dirname $0`", doc_path)

    install_runner = "python3 "
    installer_location = os.path.abspath("installer.sh")

    with open(target_path, "w+") as out_file:

        proxy_content = ""
        proxy_content += install_runner + installer_location + "\n"
        proxy_content += runner + runtime_path + " " + doc_path + "\n"

        out_file.write(proxy_content)

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