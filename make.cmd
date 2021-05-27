@echo off
rem Make-Datei 
rem
set UIName=doubleManUI
echo Erzeuge  %UIName%.py aus %UIName%.ui
pyuic5 -x %UIName%.ui -o %UIName%.py

if not "%1%"=="full" goto Ende
rem .
rem del /S /Y .\dist\VidArchiver
rem set LD_LIBRARY_PATH=%PYTHONPATH%\Lib
rem pyinstaller -w -y -i %UIName%.ico -p %PYTHONPATH%\Lib --clean -p .\FilmDetails --hiddenimport FilmDetails\FilmDetailsUI.py -n %UIName% %UIName%.py
pyinstaller -w -y -i %UIName%.ico -p %PYTHONPATH%\Lib --clean -n %UIName% %UIName%.py
copy %UIName%.ico .\dist\%UIName%

:Ende
echo Fertig!

