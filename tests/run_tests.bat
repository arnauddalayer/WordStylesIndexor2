@echo off
setlocal enabledelayedexpansion

IF "%PROCESSOR_ARCHITEW6432%"=="" GOTO native
%SystemRoot%\Sysnative\cmd.exe /c %0 %*
exit

:native
set "SCRIPT_DIR=%~dp0"
set "SRC_DIR=%SCRIPT_DIR%..\src"

if not exist "%SRC_DIR%\.venv\Scripts\activate.bat" (
    echo [ERREUR] Environnement virtuel introuvable dans "%SRC_DIR%\.venv".
    echo Veuillez d'abord executer W_install_requirements.bat dans le dossier src.
    pause
    exit /b 1
)
call "%SRC_DIR%\.venv\Scripts\activate"

set /a TOTAL=0
set /a ECHECS=0

rem Parcourt chaque sous-dossier de tests\ contenant un stylesAIndexer.txt
rem (permet d'ajouter de nouveaux TU sans modifier ce script)
for /d %%D in ("%SCRIPT_DIR%*") do (
    if exist "%%D\stylesAIndexer.txt" (
        set /a TOTAL+=1
        echo ======================================================
        echo   Test unitaire : %%~nxD
        echo ======================================================
        
        rem Pour chaque dossier de test, on genere les 4 combinaisons possibles
        for %%F in (csv json) do (
            for %%O in (style document) do (

                rem Création du sous-dossier spécifique pour l'ordre (ex: "%%D\out\style")
                rem Cela permet d'avoir un dossier unique par ordre pour ne pas écraser les fichiers.
                if not exist "%%D\out\%%O" mkdir "%%D\out\%%O"

                echo Traitement Format: %%F, Ordre: %%O
                python "%SRC_DIR%\WordStyleIndexor.py" --fichier-styles "%%D\stylesAIndexer.txt" --dossier-entree "%%D\docs" --dossier-sortie "%%D\out\%%O" --format %%F --ordre %%O
                
                if errorlevel 1 (
					echo [ECHEC] Le test %%~nxD [%%F/%%O] a retourne une erreur.
					set /a ECHECS+=1
				) else (
					echo [OK] Test %%~nxD [%%F/%%O] termine. Resultat dans %%D\out\%%O\rapport.%%F
				)
                echo.
            )
        )
    )
)

echo ======================================================
echo   Resultat : !TOTAL! test(s) execute(s), !ECHECS! echec(s)
echo ======================================================
pause
