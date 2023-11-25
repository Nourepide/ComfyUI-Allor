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
