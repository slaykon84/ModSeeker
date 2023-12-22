#!/bin/bash

if [ "$1" = "install" ] || [ -z "$1" ]; then
    IFS='/' read -ra parts <<< "$SHELL"  
    shel="${parts[3]}"
    mkdir "$HOME"/.modseeker && cd "$HOME"/.modseeker || exit
    git clone https://github.com/slaykon84/ModSeeker
    mv ModSeeker/** . && rm -fr ModSeeker
    echo "#!/bin/bash" > modseeker
    echo "python3 $HOME/.modseeker/main.py" >> modseeker
    chmod +x modseeker
    cd ..

    if [[ $shel == "bash" ]]; then
        echo "export PATH=\"\$HOME/.modseeker:\$PATH\"" >> "$HOME"/.bashrc
    elif [[ $shel == "zsh" ]]; then
        echo "export PATH=\"\$HOME/.modseeker:\$PATH\"" >> "$HOME"/.zshrc
    fi

elif [ "$1" = "remove" ]; then
    cd "$HOME"
    rm -fr .modseeker
fi
