#!/bin/bash

# Save the current directory
CURRENT_DIR=$(pwd)

# Check if the venv directory exists two levels up
if [ -d "../../venv" ]; then
    # Go two levels up from the current directory
    cd ../..

    # Check if the activate script exists in the venv
    if [ -f "venv/bin/activate" ]; then
        # Activate the virtual environment
        source venv/bin/activate

        # Go back to the original directory
        cd $CURRENT_DIR

        # Check if the requirements.txt file exists in the current directory
        if [ -f "requirements.txt" ]; then
            # Install dependencies from the requirements.txt file
            pip install -r requirements.txt

            # Check if git is installed
            if command -v git >/dev/null 2>&1; then
                echo "Git is installed."

                # Check if the current directory is a git repository
                if [ ! -d ".git" ]; then
                    echo "This directory is not a git repository. Initializing a new repository."
                    git init
                    git remote add origin https://github.com/Nourepide/ComfyUI-Allor
                    git pull origin master
                else
                    echo "This directory is already a git repository."
                fi
            else
                echo "Git is not installed. Using GitPython instead."

                # Run a Python script that uses GitPython to do the same thing
                python -c "
import git
from pathlib import Path

# Check if the current directory is a git repository
if not (Path('.git').exists() or Path('.git').is_dir()):
    print('This directory is not a git repository. Initializing a new repository.')
    repo = git.Repo.init()
    origin = repo.create_remote('origin', 'https://github.com/Nourepide/ComfyUI-Allor')
    origin.fetch()
    origin.pull(origin.refs[0].remote_head)
else:
    print('This directory is already a git repository.')
"
            fi

            # Deactivate the virtual environment
            deactivate
        else
            echo "Error: requirements.txt not found in the current directory."
        fi
    else
        echo "Error: activate script not found in the venv directory."
    fi
else
    echo "Error: venv directory not found."
fi
