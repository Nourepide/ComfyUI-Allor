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
