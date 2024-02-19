#!/bin/bash
    mkdir -p "$HOME"/.modseeker 
    mv ** "$HOME"/.modseeker && cd .. && rm -fr ModSeeker
    echo "#!/bin/bash" > modseeker
    echo "python3 $HOME/.modseeker/main.py" >> modseeker
    chmod +x modseeker

    if sudo mv modseeker /usr/bin; then
        echo "ModSeeker installed successfully."
    else
        echo "Error: Unable to move modseeker to /usr/bin. Installation failed."
        exit 1
    fi


