import os
import cv2
import glob
import send2trash
import numpy as np
from tqdm import tqdm
import FreeSimpleGUI as sg
from LocationInterface import POPUP_LOCATION

def get_image_files(folder):
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.webp')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(folder, ext)))
    return sorted(files)

def resize_with_padding(img, size=1000):
    h, w = img.shape[:2]
    scale = size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    canvas = np.zeros((size, size, 3), dtype=np.uint8)
    x_offset = (size - new_w) // 2
    y_offset = (size - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas

def show_image_with_controls(image_path):
    img = cv2.imread(image_path)
    if img is None:
        sg.popup(f"Impossible de lire {image_path}", location=POPUP_LOCATION)
        return 'error'

    display_img = resize_with_padding(img, size=1000)
    window_name = "Visionnage photos (espace=suppr, a=suivante, esc=quitter)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1000, 1000)
    cv2.imshow(window_name, display_img)

    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == 27:  # ESC
            cv2.destroyAllWindows()
            return 'quit'
        elif key == 32:  # Espace
            cv2.destroyAllWindows()
            return 'delete'
        elif key == 97:  # a
            cv2.destroyAllWindows()
            return 'keep'

def main():
    folder = sg.popup_get_folder("Entrez le chemin du dossier contenant les photos :\nexemple : C:\\Dossier", location=POPUP_LOCATION)
    if not os.path.isdir(folder):
        sg.popup("Chemin invalide.", location=POPUP_LOCATION)
        return

    image_files = get_image_files(folder)
    total_files = len(image_files)
    sg.popup(f"{total_files} photos trouvées.\nContrôles : [ESPACE] = Corbeille, [A] = Suivant, \n[ESC] = Quitter", location=POPUP_LOCATION)

    with tqdm(total=total_files, desc="Progression", unit="photo") as pbar:
        for image_path in image_files:
            print(f"\nVisionnage de : {os.path.basename(image_path)}")

            action = show_image_with_controls(image_path)

            if action == 'quit':
                print("Arrêt du tri.")
                break
            elif action == 'delete':
                try:
                    send2trash.send2trash(image_path)
                    print("→ Supprimée (corbeille).")
                except Exception as e:
                    print(f"Erreur suppression : {e}")
            elif action == 'keep':
                print("→ Conservée.")

            pbar.update(1)

if __name__ == "__main__":
    main()
