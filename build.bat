@echo off
echo ============================================
echo   Network Commands - Building .exe
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install from https://python.org
    pause
    exit /b 1
)

REM Install PyInstaller if not present
echo [1/3] Installing PyInstaller...
pip install pyinstaller --quiet

REM Build the .exe and embed the application icon
echo [2/3] Building NetCommands.exe...
pyinstaller --clean --onefile --noconsole --name "NetCommands" --icon "icon.ico" --add-data "icon.ico;." netcmds.py

echo.
echo [3/3] Done!
echo.
echo Output: dist\NetCommands.exe
echo.
pause
