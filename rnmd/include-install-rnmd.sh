
RNMD_LOCATION=$(whereis rnmd)

RNMD_LOCATION=""

if [ -z "$RNMD_LOCATION" ]; then
    echo "Could not locate rnmd which is required to run this script."
    read -p "Do you want to install it? (y/n)" answer

    if [ $answer = "y" ]; then
        
        PIP3_LOCATION=$(whereis pip3)
        PYTHON3_LOCATION=$(whereis python3)

        if [[ -z "$PIP3_LOCATION" || -z "$PYTHON3_LOCATION" ]]; then
            echo "Could not install 'rnmd' missing python3 or pip3!"
            echo "Please make sure that both python3 and pip3 is installed, before trying again!"
            exit
        fi

        pip3 install rnmd
    fi
fi