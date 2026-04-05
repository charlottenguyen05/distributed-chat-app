@echo off
echo Starting 4 User Interface

:: Start servers
start "UI 0" cmd /k python UserInterface.py 10000
start "UI 1" cmd /k python UserInterface.py 10001
start "UI 2" cmd /k python UserInterface.py 10002
