@echo off
REM ----------------------------------------------------
REM iengine.bat — wrapper to call your Python inference engine
REM Usage:   iengine <filename> <method>
REM Example: iengine test1.txt FC
REM ----------------------------------------------------

REM (1) If you’ve named your driver main.py:
python main.py %1 %2


REM (3) If you want silence on success, uncomment:
REM @rem exit /B 0
