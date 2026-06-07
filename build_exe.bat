@echo off
REM Build CodeVault EXE on Windows
REM Make sure PyInstaller is installed: pip install -r requirements.txt

echo Building CodeVault EXE...
pyinstaller build_exe.spec --clean

echo.
echo Build complete! Your EXE is in the dist/CodeVault folder
echo Run: dist\CodeVault\CodeVault.exe
pause
