@echo off

REM Save the current directory
set CURRENT_DIR=%cd%

REM Check if the venv directory exists two levels up
if exist "..\..\venv\" (
    REM Go two levels up from the current directory
    cd ..\..

    REM Check if the activate script exists in the venv
    if exist "venv\Scripts\activate" (
        REM Activate the virtual environment
        call venv\Scripts\activate

        REM Go back to the original directory
        cd %CURRENT_DIR%

        REM Check if the requirements.txt file exists in the current directory
        if exist "requirements.txt" (
            REM Install dependencies from the requirements.txt file
            pip install -r requirements.txt

            REM Check if git is installed
            where /q git
            if %ERRORLEVEL% equ 0 (
                echo Git is installed.

                REM Check if the current directory is a git repository
                if not exist ".git" (
                    echo This directory is not a git repository. Initializing a new repository.
                    git init
                    git remote add origin https://github.com/Nourepide/ComfyUI-Allor
                    git pull origin master
                ) else (
                    echo This directory is already a git repository.
                )
            ) else (
                echo Git is not installed. Using GitPython instead.

                REM Run a Python script that uses GitPython to do the same thing
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
            )

            REM Deactivate the virtual environment
            deactivate
        ) else (
            echo Error: requirements.txt not found in the current directory.
        )
    ) else (
        echo Error: activate script not found in the venv directory.
    )
) else (
    echo Error: venv directory not found.
)
