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

def make_proxy(source, target):

    doc_path = os.path.abspath(source)
    runner = "python3"
    runtime_path = os.path.abspath("run_md.py")

    install_runner = "python3"
    installer_location = os.path.abspath("installer.sh")

    with open(target, "w+") as out_file:

        proxy_content = ""
        proxy_content += install_runner + " " + installer_location + "\n"
        proxy_content += runner + " " + runtime_path + " " + doc_path + "\n"

        out_file.write(proxy_content)

    print("Created proxy at: " + target)

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