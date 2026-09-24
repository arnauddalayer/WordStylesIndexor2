@echo off
IF "%PROCESSOR_ARCHITEW6432%"=="" GOTO native
%SystemRoot%\Sysnative\cmd.exe /c %0 %*
exit

:native
:: Vérification de l'environnement virtuel
if not exist .venv (
    echo [ERREUR] L'environnement virtuel .venv n'existe pas.
    echo Veuillez executer W_install_requirements.bat pour initialiser l'environnement.
    pause
    exit /b
)

:: Activation de l'environnement virtuel
call .venv\Scripts\activate
if errorlevel 1 (
    echo [ERREUR] Echec de l'activation de l'environnement virtuel.
    pause
    exit /b
)

:: Exécution du script Python
python WordStyleIndexor.py --verbose
if errorlevel 1 (
    echo [ERREUR] L'execution du script a echoue.
    pause
) else (
    pause
)
