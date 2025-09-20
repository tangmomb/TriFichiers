import os
import shutil
import FreeSimpleGUI as sg
from LocationInterface import POPUP_LOCATION

def ensure_dir_exists(path):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

def flatten_and_categorize(root_folder):
    photo_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    video_exts = {".mp4", ".mov", ".avi", ".mkv", ".wmv"}

    photos_folder = os.path.join(root_folder, "photos")
    videos_folder = os.path.join(root_folder, "videos")

    os.makedirs(photos_folder, exist_ok=True)
    os.makedirs(videos_folder, exist_ok=True)

    # Traiter d'abord les fichiers à la racine
    for file in os.listdir(root_folder):
        src_path = os.path.join(root_folder, file)
        if os.path.isfile(src_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in photo_exts:
                dst_folder = photos_folder
            elif ext in video_exts:
                dst_folder = videos_folder
            else:
                dst_folder = root_folder

            dst_path = os.path.join(dst_folder, file)

            # En cas de doublon, renommage
            if os.path.exists(dst_path):
                base, ext2 = os.path.splitext(file)
                i = 1
                while True:
                    new_name = f"{base}_{i}{ext2}"
                    new_dst_path = os.path.join(dst_folder, new_name)
                    if not os.path.exists(new_dst_path):
                        dst_path = new_dst_path
                        break
                    i += 1

            # Création dossier parent s'il manque
            ensure_dir_exists(dst_path)

            shutil.move(src_path, dst_path)

    # Parcourir les sous-dossiers et déplacer leurs fichiers
    for dirpath, dirnames, filenames in os.walk(root_folder, topdown=False):
        if dirpath == root_folder:
            continue
        for file in filenames:
            src_path = os.path.join(dirpath, file)
            ext = os.path.splitext(file)[1].lower()
            if ext in photo_exts:
                dst_folder = photos_folder
            elif ext in video_exts:
                dst_folder = videos_folder
            else:
                dst_folder = root_folder

            dst_path = os.path.join(dst_folder, file)

            # En cas de doublon, renommage
            if os.path.exists(dst_path):
                base, ext2 = os.path.splitext(file)
                i = 1
                while True:
                    new_name = f"{base}_{i}{ext2}"
                    new_dst_path = os.path.join(dst_folder, new_name)
                    if not os.path.exists(new_dst_path):
                        dst_path = new_dst_path
                        break
                    i += 1

            ensure_dir_exists(dst_path)

            shutil.move(src_path, dst_path)

        # Supprimer dossier vide
        try:
            os.rmdir(dirpath)
        except OSError as e:
            sg.popup(f"Impossible de supprimer {dirpath}: {e}", location=POPUP_LOCATION)

if __name__ == "__main__":
    folder_to_flatten = sg.popup_get_folder("Entrez le chemin du dossier à analyser :\nexemple : C:\\Dossier", location=POPUP_LOCATION)
    flatten_and_categorize(folder_to_flatten)
    sg.popup("Opération terminée.", location=POPUP_LOCATION)
