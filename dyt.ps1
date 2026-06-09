# Get the directory where this .ps1 file is located
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent

# Run the python interpreter from the virtual environment, targeting cli.py
& "$ScriptDir\venv\Scripts\python.exe" "$ScriptDir\cli.py" $args