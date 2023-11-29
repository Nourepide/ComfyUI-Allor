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

echo [Allor]: Searching for Python environments.

REM Check if the environment directory exists two levels up
if exist "..\..\venv\" goto venv

REM Check if the environment directory exists three levels up
if exist "..\..\..\python_embeded\" goto portable

REM Check if the environment directory exists in system
where /q python && if !ERRORLEVEL! equ 0 goto system

REM Error if the environment not exist
goto not_found_environment

:venv
REM Go two levels up from the current directory
cd ..\..

REM Check if the activate script exists in the venv
if exist "venv\Scripts\activate" (
    echo [Allor]: Found venv Python environment.

    REM Activate the virtual environment
    call venv\Scripts\activate

    REM Set the flag for venv activation
    set VENV_ACTIVATED=1

    REM Go back to the original directory
    cd !CURRENT_DIR!

    REM Check if the requirements.txt file exists in the current directory
    if exist "requirements.txt" (
        REM Install dependencies from the requirements.txt file
        pip install -r requirements.txt --no-warn-script-location --quiet
    ) else (
        echo [Allor]: requirements.txt not found in the current directory.
        exit /b
    )
)
goto git

:portable
REM Go three levels up from the current directory
cd ..\..\..

REM Check if python.exe exists in the python_embedded directory
if exist "python_embeded\python.exe" (
    echo [Allor]: Found portable Python environment.

    REM Set the flag for venv activation
    set VENV_ACTIVATED=2

    REM Set the Python executable to the python.exe in the python_embedded directory
    set PYTHON_EXECUTABLE=!cd!\python_embeded\python.exe

    REM Execute python.exe with the specified arguments
    call !PYTHON_EXECUTABLE! -s -m pip install -r !CURRENT_DIR!\requirements.txt --no-warn-script-location --quiet

    REM Go back to the original directory
    cd !CURRENT_DIR!
)
goto git

:system
set /p user_input=[Allor]: Only the system Python environment is detected. Should this be used for Allor dependencies? (y/N):

if /i "%user_input%"=="y" goto confirmed
if /i "%user_input%"=="yes" goto confirmed
goto not_found_environment

:confirmed
REM Set the flag for venv activation
set VENV_ACTIVATED=3

REM Execute python.exe with the specified arguments
call !PYTHON_EXECUTABLE! -s -m pip install -r !CURRENT_DIR!\requirements.txt --no-warn-script-location --quiet

REM Go back to the original directory
cd !CURRENT_DIR!
goto git

:not_found_environment
REM If neither venv nor python_embeded were found, print an error and exit
echo [Allor]: None of the Python environments were found.
exit /b

:git
where /q git && if !ERRORLEVEL! equ 0 (
    echo [Allor]: Git found.

    REM Check if the current directory is a git repository
    if not exist ".git" (
        echo [Allor]: This directory is not a git repository. Initializing a new repository.

        git init
        git remote add origin https://github.com/Nourepide/ComfyUI-Allor
        git fetch origin main
        git reset --hard origin/main
    ) else (
        echo [Allor]: This directory is already a git repository.
    )
) else (
    echo [Allor]: Git is not installed. Using GitPython instead.

    REM Run a Python script that uses GitPython to do the same thing
    call !PYTHON_EXECUTABLE! %~f0
)

REM Deactivate the virtual environment if it was activated
if !VENV_ACTIVATED! equ 1 (
    deactivate
)

echo [Allor]: Install complete successful.

endlocal
exit /b
'''
import git
from pathlib import Path

# Check if the current directory is a git repository
if not (Path('.git').exists() or Path('.git').is_dir()):
    from git import Repo

    print("[Allor]: This directory is not a git repository. Initializing a new repository.")

    repo = Repo.init()
    origin = repo.create_remote('origin', 'https://github.com/Nourepide/ComfyUI-Allor')
    origin.fetch('main')
    repo.git.reset('--hard', 'origin/main')
else:
    print('[Allor]: This directory is already a git repository.')
