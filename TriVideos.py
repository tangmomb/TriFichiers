import os
import cv2
import glob
import send2trash

def get_video_files(folder):
    extensions = ('*.mp4', '*.mov', '*.avi', '*.mkv')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(folder, ext)))
    return sorted(files)

def on_trackbar(val, cap):
    cap.set(cv2.CAP_PROP_POS_FRAMES, val)

def play_video_with_controls(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Erreur d'ouverture de la vidéo : {video_path}")
        return 'error'

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    window_name = "Lecture vidéo (espace=suppr, →=garder, esc=quitter)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    current_frame = 0

    # Trackbar liée à la vidéo
    def on_trackbar_wrapper(val):
        nonlocal current_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, val)
        current_frame = val

    cv2.createTrackbar('Position', window_name, 0, total_frames - 1, on_trackbar_wrapper)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        cv2.setTrackbarPos('Position', window_name, current_frame)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(30) & 0xFF

        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            return 'quit'
        elif key == 32:  # Espace
            cap.release()
            cv2.destroyAllWindows()
            return 'delete'
        elif key == 97: # a
            cap.release()
            cv2.destroyAllWindows()
            return 'keep'

    cap.release()
    cv2.destroyAllWindows()
    return 'keep'

def main():
    folder = input("Entrez le chemin du dossier contenant les vidéos : ").strip()
    if not os.path.isdir(folder):
        print("Chemin invalide.")
        return

    video_files = get_video_files(folder)
    print(f"{len(video_files)} vidéos trouvées.")

    for video_path in video_files:
        print(f"\nLecture de : {os.path.basename(video_path)}")

        action = play_video_with_controls(video_path)

        if action == 'quit':
            print("Arrêt du tri.")
            break
        elif action == 'delete':
            try:
                send2trash.send2trash(video_path)
                print("→ Supprimée (corbeille).")
            except Exception as e:
                print(f"Erreur suppression : {e}")
        elif action == 'keep':
            print("→ Conservée.")

if __name__ == "__main__":
    main()
