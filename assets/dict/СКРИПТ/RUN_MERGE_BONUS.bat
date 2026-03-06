@echo off
chcp 65001 > nul
cd /d "C:\Users\User\Desktop\СЛОВОГРАЙ2\assets\dict\СКРИПТ"

python merge_bonus.py

echo.
echo DONE. Press any key...
pause > nul
