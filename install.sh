#!/bin/bash

# Save the current directory
CURRENT_DIR=$(pwd)

VENV_ACTIVE=false

echo -e "\e[34m[Allor]\e[0m: Searching for Python environments."

if [ -d "../../venv" ]; then
    echo -e "\e[34m[Allor]\e[0m: Found venv Python environment."

    cd ../..

    # Check if the activate script exists in the venv
    if [ -f "venv/bin/activate" ]; then
        # Activate the virtual environment
        source venv/bin/activate

        VENV_ACTIVE=true

        # Go back to the original directory
        cd $CURRENT_DIR
    else
      echo -e "\e[31m[Allor]\e[0m: Activation script not found."
      exit 1
    fi
elif command -v python3 &> /dev/null; then
    printf "\e[34m[Allor]\e[0m: Only the system Python environment is detected. Should this be used for Allor dependencies? (y/N): "
    read answer

    [[ $answer =~ ^[yY] ]] || echo -e "\e[31m[Allor]\e[0m: None of the Python environments were found." && exit 1
else
    echo -e "\e[31m[Allor]\e[0m: None of the Python environments were found."
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo -e "\e[34m[Allor]\e[0m: Install dependencies from the requirements.txt file."
    pip install -r requirements.txt --no-warn-script-location --quiet --disable-pip-version-check
else
    echo -e "\e[31m[Allor]\e[0m: requirements.txt not found in the current directory."
    exit 1
fi

if command -v git >/dev/null 2>&1; then
    echo -e "\e[34m[Allor]\e[0m: Git found."

    # Check if the current directory is a git repository
    if [ ! -d ".git" ]; then
        echo -e "\e[34m[Allor]\e[0m: This directory is not a git repository. Initializing a new repository."

        git init
        git remote add origin https://github.com/Nourepide/ComfyUI-Allor
        git pull origin master
    else
        echo -e "\e[34m[Allor]\e[0m: This directory is already a git repository."
    fi
else
    echo -e "\e[34m[Allor]\e[0m: Git is not installed. Using GitPython instead."

    # Run a Python script that uses GitPython to do the same thing
    python -c '
import git

from git import Repo
from pathlib import Path

# Check if the current directory is a git repository
if not (Path(".git").exists() or Path(".git").is_dir()):
    print("\033[94m[Allor]\033[0m: This directory is not a git repository. Initializing a new repository.")

    repo = Repo.init()
    origin = repo.create_remote("origin", "https://github.com/Nourepide/ComfyUI-Allor")
    origin.fetch("main")
    repo.git.reset("--hard", "origin/main")
else:
    print("\033[94m[Allor]\033[0m: This directory is already a git repository.")
'
fi

if [ $VENV_ACTIVE ]; then
    deactivate
fi

echo -e "\e[32m[Allor]\e[0m: Install complete successful."
