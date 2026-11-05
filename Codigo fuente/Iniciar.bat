@echo off
setlocal
pushd "%~dp0"
py -3 -B -c "import sys, tkinter; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 (
    py -3 -B main.py
) else (
    python -B -c "import sys, tkinter; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
    if errorlevel 1 (
        echo Se necesita Python 3.10 o superior con Tcl/Tk.
        echo Descarga Python desde https://www.python.org/downloads/windows/
        echo Marca la opcion de agregar Python a PATH durante la instalacion.
        pause
        popd
        exit /b 1
    )
    python -B main.py
)
set "resultado=%errorlevel%"
if not "%resultado%"=="0" pause
popd
exit /b %resultado%
