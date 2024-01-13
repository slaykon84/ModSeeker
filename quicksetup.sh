#!/bin/bash

if [ "$1" = "install" ]; then

    mkdir -p "$HOME"/.modseeker && cd "$HOME"/.modseeker
    if git clone https://github.com/slaykon84/ModSeeker; then
        echo "Git clone successful."
    else
        echo "Error: Git clone failed. Installation aborted."
        rm -fr "$HOME"/.modseeker
        exit 1
    fi

    mv ModSeeker/** "$HOME"/.modseeker && rm -fr ModSeeker
    echo "#!/bin/bash" > modseeker
    echo "python3 $HOME/.modseeker/main.py" >> modseeker
    chmod +x modseeker

    if mv modseeker /usr/bin; then
        echo "ModSeeker installed successfully."
    else
        if sudo mv modseeker /usr/bin; then
            echo "ModSeeker installed successfully."
        else
            echo "Error: Unable to move modseeker to /usr/bin. Installation failed."
            exit 1
        fi
    ficp

elif [ "$1" = "remove" ]; then
    cd "$HOME"
    rm -fr .modseeker
    if [ -e /usr/bin/modseeker ]; then
        rm /usr/bin/modseeker
        echo "ModSeeker removed successfully."
    else
        if sudo rm /usr/bin/modseeker; then
            echo "ModSeeker removed successfully."
        else
            echo "ModSeeker not found in /usr/bin. Nothing to remove."
        fi
    fi

else
    echo "Usage: ./quicksetup.sh [install|remove]"
    exit 1
fi
