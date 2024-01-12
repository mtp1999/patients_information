@echo off
cd /d %~dp0

:: Path to virtual environment folder (change 'venv' if yours is named differently)
set VENV=venv

:: Activate the virtual environment
call "%VENV%\Scripts\activate.bat"

:: Run the Django server
echo Starting Django server...
cmd /k "python manage.py runserver"