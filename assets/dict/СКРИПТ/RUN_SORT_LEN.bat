@echo off
chcp 65001 > nul
cd /d "C:\Users\User\Desktop\СЛОВОГРАЙ2\assets\dict\СКРИПТ"

python sort_len_core_hard.py

echo.
echo DONE. Press any key...
pause > nul
