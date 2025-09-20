import os
import FreeSimpleGUI as sg
from LocationInterface import POPUP_LOCATION

# Dossier à analyser
FOLDER_PATH = sg.popup_get_folder("Entrez le chemin du dossier à analyser :\nexemple : C:\\Dossier", location=POPUP_LOCATION)

# Extensions des fichiers images et vidéos (en minuscules)
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'}

total_size_images = 0
total_size_videos = 0

for root, _, files in os.walk(FOLDER_PATH):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        file_path = os.path.join(root, file)
        try:
            size = os.path.getsize(file_path)
        except OSError:
            size = 0
        
        if ext in IMAGE_EXTENSIONS:
            total_size_images += size
        elif ext in VIDEO_EXTENSIONS:
            total_size_videos += size

def sizeof_fmt(num, suffix='B'):
    # Convertit taille en format lisible (Ko, Mo, Go...)
    for unit in ['','Ki','Mi','Gi','Ti']:
        if abs(num) < 1024.0:
            return f"{num:.2f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.2f} Pi{suffix}"

sg.popup(f"Total images size: {sizeof_fmt(total_size_images)}", location=POPUP_LOCATION)
sg.popup(f"Total videos size: {sizeof_fmt(total_size_videos)}", location=POPUP_LOCATION)
