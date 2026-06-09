@echo off
:: Get the directory where this .bat file is located
set "DIR=%~dp0"

:: Run the python interpreter from the virtual environment, targeting cli.py
"%DIR%venv\Scripts\python.exe" "%DIR%cli.py" %*