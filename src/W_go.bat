@echo off
IF "%PROCESSOR_ARCHITEW6432%"=="" GOTO native
%SystemRoot%\Sysnative\cmd.exe /c %0 %*
exit

:native
call .venv\Scripts\activate
python WordStyleIndexor.py --verbose
pause