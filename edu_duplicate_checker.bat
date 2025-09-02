@echo off
setlocal enabledelayedexpansion

:: User input
set /p max="Enter how many times to run (e.g. 1-20): "

:: Loop from 1 to %max%
for /L %%i in (1,1,%max%) do (
    start "GET_Title: %%i" cmd /k "py -3 duplicate_checker.py"
	
    timeout /t 5 >nul
)

echo [✓] All tasks started.
pause
