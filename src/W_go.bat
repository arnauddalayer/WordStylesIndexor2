@echo off
IF "%PROCESSOR_ARCHITEW6432%"=="" GOTO native
%SystemRoot%\Sysnative\cmd.exe /c %0 %*
exit

:native
:: Correction pour l'exécution en tant qu'administrateur
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%"

echo ======================================================
echo   Lancement de WordStyleIndexor
echo ======================================================

echo [INFO] Dossier actuel : %CD%

:: Vérification si le dossier est un dossier temporaire
echo %CD% | findstr /I "Temp" >nul
if %errorlevel% == 0 (
    echo [ERREUR] Il semble que vous executez le script depuis un dossier temporaire.
    echo Veuillez decompresser le fichier ZIP, ou deplacer le dossier de WordStyleIndexor2 avant de lancer l'installation.
    pause
    exit /b
)

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
