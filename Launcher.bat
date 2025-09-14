@echo off
REM Récupérer le dossier où est lancé le .bat
set BASE_DIR=%~dp0

REM Supprimer le backslash final pour éviter les problèmes
set BASE_DIR=%BASE_DIR:~0,-1%

REM Activer l'environnement virtuel dans Scripts/
call "%BASE_DIR%\venv\Scripts\activate"

REM Lancer le script Python dans le même dossier
python "%BASE_DIR%\Launcher.py"

REM Laisser la console ouverte pour voir les inputs
exit
