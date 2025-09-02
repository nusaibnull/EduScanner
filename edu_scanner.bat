@echo off
setlocal enabledelayedexpansion

:: User input
set /p max="Enter how many times to run (e.g. 1 - 20): "

:: Loop from 1 to %max%
for /L %%i in (1,1,%max%) do (
    start "Edu Scanner: %%i" cmd /k "py -3 edu_scanner.py"
	
    timeout /t 5 >nul
)

echo [✓] All tasks started.
pause
