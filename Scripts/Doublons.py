import os
import hashlib
from tqdm import tqdm
from send2trash import send2trash
import FreeSimpleGUI as sg
from LocationInterface import POPUP_LOCATION

def hash_fichier(path, chunk_size=8192):
    """Retourne le hash SHA256 du fichier (lecture par blocs)"""
    sha = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha.update(chunk)
        return sha.hexdigest()
    except Exception as e:
        print(f"⚠️ Erreur lecture : {path} — {e}")
        return None

def trouver_doublons(dossier):
    """Retourne un dict {hash: [liste de chemins]}"""
    hash_map = {}
    fichiers = []

    # Étape 1 : Lister tous les fichiers
    for root, _, files in os.walk(dossier):
        for file in files:
            fichiers.append(os.path.join(root, file))

    print(f"🔍 {len(fichiers)} fichiers à analyser...\n")

    # Étape 2 : Calculer les hash avec barre de progression
    for chemin in tqdm(fichiers, desc="🔄 Calcul des empreintes SHA256"):
        h = hash_fichier(chemin)
        if h:
            hash_map.setdefault(h, []).append(chemin)

    return {k: v for k, v in hash_map.items() if len(v) > 1}

def supprimer_doublons(dossier):
    doublons = trouver_doublons(dossier)
    total = 0
    print(f"\n📁 {len(doublons)} groupes de doublons détectés.\n")

    for h, fichiers in tqdm(doublons.items(), desc="🗑️ Suppression des doublons"):
        originaux = fichiers[1:]  # on garde le 1er, on supprime les autres
        for fichier in originaux:
            try:
                send2trash(fichier)
                total += 1
            except Exception as e:
                print(f"❌ Erreur suppression : {fichier} — {e}")
    sg.popup(f"\n✅ {total} doublons envoyés à la corbeille.", location=POPUP_LOCATION)

if __name__ == "__main__":
    chemin = sg.popup_get_folder("📁 Dossier à scanner pour doublons :\nexemple : C:\\Dossier", location=POPUP_LOCATION)
    if not os.path.exists(chemin):
        print("❌ Chemin invalide.")
    else:
        supprimer_doublons(chemin)
