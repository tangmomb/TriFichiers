import os
import FreeSimpleGUI as sg
from LocationInterface import POPUP_LOCATION

def count_files(folder):
    total_files = 0
    for root, dirs, files in os.walk(folder):
        total_files += len(files)
    return total_files

if __name__ == "__main__":
    folder_path = sg.popup_get_folder("Entrez le chemin du dossier à analyser :\nexemple : C:\\Dossier", location=POPUP_LOCATION)
    
    if not os.path.isdir(folder_path):
        sg.popup(f"Erreur : le chemin '{folder_path}' n'existe pas ou n'est pas un dossier.", location=POPUP_LOCATION)
    else:
        total = count_files(folder_path)
        sg.popup(f"Nombre total de fichiers dans '{folder_path}' et ses sous-dossiers : {total}", location=POPUP_LOCATION)
