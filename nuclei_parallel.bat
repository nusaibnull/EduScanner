@echo off
setlocal enabledelayedexpansion

:: Ask user how many report files to process
set /p max="Enter how many input files to scan (e.g. 1 - 20): "

:: Create output\nuclei folder if not exists
if not exist output\nuclei (
    mkdir output\nuclei
)

:: Loop from 1 to %max%
for /L %%i in (1,1,%max%) do (
    echo [*] Running nuclei on reports/%%i.txt
    start "Nuclei: %%i" cmd /k "nuclei -l reports/%%i.txt -t nuclei-templates-main -severity critical,high -o output\nuclei\nuclei_out_%%i.txt"
    timeout /t 10 >nul
)

echo [✓] All nuclei scans started in parallel.
pause
