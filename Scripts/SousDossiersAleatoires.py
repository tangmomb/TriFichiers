import os
import random
import shutil
import FreeSimpleGUI as sg
from LocationInterface import POPUP_LOCATION

def randomize_files_in_subfolders(root_folder, num_subfolders=5, max_depth=3):
    if not os.path.isdir(root_folder):
    sg.popup("Le dossier spécifié n'existe pas.", location=POPUP_LOCATION)
        return

    # Récupérer tous les fichiers dans le dossier racine et ses sous-dossiers
    files = []
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for f in filenames:
            files.append(os.path.join(dirpath, f))

    if not files:
        print("Aucun fichier trouvé.")
        return

    print(f"{len(files)} fichiers trouvés. Création des sous-dossiers aléatoires...")

    # Génération des sous-dossiers aléatoires
    all_paths = []
    for i in range(num_subfolders):
        path = root_folder
        depth = random.randint(1, max_depth)
        for d in range(depth):
            folder_name = f"folder_{i}_{d}_{random.randint(1000, 9999)}"
            path = os.path.join(path, folder_name)
            if not os.path.exists(path):
                os.makedirs(path)
            if path not in all_paths:
                all_paths.append(path)

    print(f"{len(all_paths)} dossiers (tous niveaux) disponibles pour placement.")

    # Déplacer les fichiers
    for src in files:
        file = os.path.basename(src)
        dest_folder = random.choice(all_paths)  # Choisir un dossier aléatoire parmi tous les niveaux
        dest = os.path.join(dest_folder, file)

        # Gérer les doublons
        if os.path.exists(dest):
            base, ext = os.path.splitext(file)
            i = 1
            while os.path.exists(os.path.join(dest_folder, f"{base}_{i}{ext}")):
                i += 1
            dest = os.path.join(dest_folder, f"{base}_{i}{ext}")

        shutil.move(src, dest)
        print(f"Déplacé : {file} -> {dest_folder}")

    sg.popup("Opération terminée.", location=POPUP_LOCATION)

if __name__ == "__main__":
    folder_to_randomize = sg.popup_get_folder("Entrez le chemin du dossier racine :\nexemple : C:\\Dossier", location=POPUP_LOCATION)
    num_folders = int(sg.popup_get_text("Combien de sous-dossiers créer ? (ex: 10) : ", location=POPUP_LOCATION).strip())
    depth = int(sg.popup_get_text("Profondeur max des sous-dossiers ? (ex: 3) : ", location=POPUP_LOCATION).strip())
    randomize_files_in_subfolders(folder_to_randomize, num_folders, depth)
