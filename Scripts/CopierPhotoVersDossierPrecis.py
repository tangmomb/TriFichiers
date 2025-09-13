import os
import cv2
import shutil
import numpy as np
from tqdm import tqdm
import FreeSimpleGUI as sg

def resize_with_padding(img, size=1000):
    h, w = img.shape[:2]
    scale = size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)

    # Redimensionnement avec ratio conservé
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Créer un carré noir (bandes noires)
    canvas = np.zeros((size, size, 3), dtype=np.uint8)

    # Calcul pour centrer l'image
    x_offset = (size - new_w) // 2
    y_offset = (size - new_h) // 2

    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas

def main():
    source_dir = sg.popup_get_text("Chemin du dossier contenant les images :")
    dest_dir = sg.popup_get_text("Chemin du dossier de destination :")

    if not os.path.isdir(source_dir):
        sg.popup("Erreur : le dossier source n'existe pas.")
        return
    if not os.path.isdir(dest_dir):
        sg.popup("Le dossier de destination n'existe pas, création...")
        os.makedirs(dest_dir)

    valid_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
    images = [f for f in os.listdir(source_dir) if f.lower().endswith(valid_ext)]

    if not images:
        print("Aucune image trouvée dans le dossier.")
        return

    total_images = len(images)
    print(f"{total_images} images trouvées.")
    print("Contrôles : [ESPACE] = Déplacer, [A] = Suivant, [Q] = Quitter")

    cv2.namedWindow('Image Viewer', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image Viewer', 1000, 1000)

    with tqdm(total=total_images, desc="Progression", unit="image") as pbar:
        for img_name in images:
            img_path = os.path.join(source_dir, img_name)
            img = cv2.imread(img_path)

            if img is None:
                print(f"Impossible de lire {img_name}, passage à la suivante.")
                pbar.update(1)
                continue

            # Redimensionner avec bandes noires
            display_img = resize_with_padding(img, size=1000)
            cv2.imshow('Image Viewer', display_img)

            while True:
                key = cv2.waitKey(0) & 0xFF
                if key == 32:  # ESPACE
                    shutil.move(img_path, os.path.join(dest_dir, img_name))
                    print(f"Image déplacée : {img_name}")
                    break
                elif key == ord('a') or key == ord('A'):
                    print(f"Passage à la suivante : {img_name}")
                    break
                elif key == ord('q') or key == ord('Q'):
                    print("Sortie du programme...")
                    cv2.destroyAllWindows()
                    return

            pbar.update(1)

    cv2.destroyAllWindows()
    print("Toutes les images ont été affichées.")

if __name__ == "__main__":
    main()
