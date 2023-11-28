0<0# : ^
'''
@echo off
setlocal enabledelayedexpansion

REM Save the current directory
set CURRENT_DIR=!cd!

REM Initialize a flag for venv activation
set VENV_ACTIVATED=0

REM Initialize a variable for the Python executable
set PYTHON_EXECUTABLE=python

REM Check if the venv directory exists two levels up
if exist "..\..\venv\" (
    REM Go two levels up from the current directory
    cd ..\..

    REM Check if the activate script exists in the venv
    if exist "venv\Scripts\activate" (
        REM Activate the virtual environment
        call venv\Scripts\activate

        REM Set the flag for venv activation
        set VENV_ACTIVATED=1

        REM Go back to the original directory
        cd !CURRENT_DIR!

        REM Check if the requirements.txt file exists in the current directory
        if exist "requirements.txt" (
            REM Install dependencies from the requirements.txt file
            pip install -r requirements.txt
        ) else (
            echo Error: requirements.txt not found in the current directory.
        )
    )
)

if exist "..\..\..\python_embeded\" (
    REM Go three levels up from the current directory
    cd ..\..\..

    REM Check if python.exe exists in the python_embedded directory
    if exist "python_embeded\python.exe" (
        REM Set the flag for venv activation
        set VENV_ACTIVATED=2

        REM Set the Python executable to the python.exe in the python_embedded directory
        set PYTHON_EXECUTABLE=!cd!\python_embeded\python.exe
        
        echo !PYTHON_EXECUTABLE!

        REM Execute python.exe with the specified arguments
        call !PYTHON_EXECUTABLE! -s -m pip install -r !CURRENT_DIR!\requirements.txt --no-warn-script-location

        REM Go back to the original directory
        cd !CURRENT_DIR!
    )
)

REM If neither venv nor python_embeded were found, print an error and exit
if !VENV_ACTIVATED! equ 0 (
    echo Error: Neither venv nor python_embeded were found.
    exit /b
)

where /q git
if !ERRORLEVEL! equ 0 (
    echo Git is installed.

    REM Check if the current directory is a git repository
    if not exist ".git" (
        echo This directory is not a git repository. Initializing a new repository.
        git init
        git remote add origin https://github.com/Nourepide/ComfyUI-Allor
        git fetch origin main
        git reset --hard origin/main
    ) else (
        echo This directory is already a git repository.
    )
) else (
    echo Git is not installed. Using GitPython instead.

    REM Run a Python script that uses GitPython to do the same thing
    call !PYTHON_EXECUTABLE! %~f0
)

REM Deactivate the virtual environment if it was activated
if !VENV_ACTIVATED! equ 1 (
    deactivate
)

endlocal
exit /b 0
'''
import git
from pathlib import Path

# Check if the current directory is a git repository
if not (Path('.git').exists() or Path('.git').is_dir()):
    print('This directory is not a git repository. Initializing a new repository.')
    repo = git.Repo.init()
    origin = repo.create_remote('origin', 'https://github.com/Nourepide/ComfyUI-Allor')
    origin.fetch()
    origin_ref = origin.refs[0]
    repo.git.reset('--hard', origin_ref.remote_head)
else:
    print('This directory is already a git repository.')
