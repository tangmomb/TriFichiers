import FreeSimpleGUI as sg
import subprocess, sys, os

# --- Thème bleu marine ---
sg.theme("DarkGrey10")

# --- Liste des scripts ---

Dossier = os.path.dirname(os.path.abspath(__file__)) + "/Scripts/"

SCRIPTS = {
    "Déplacer photos": {
        "file": Dossier + "CopierPhotoVersDossierPrecis.py",
        "desc": "Ouvre une interface pour déplacer des photos d'un dossier à un autre avec 2 touches (oui = Espace / non = A)"
    },
    "Doublons": {
        "file": Dossier + "Doublons.py",
        "desc": "Déplace les doublons détectés dans un dossier à la corbeille"
    },
    "Nombre de fichiers": {
        "file": Dossier + "NombreDeFichiers.py",
        "desc": "Compte le nombre total de fichiers dans un dossier et ses sous-dossiers"
    },
    "Poids des vidéos/photos": {
        "file": Dossier + "Poids.py",
        "desc": "Calcule le poids total des fichiers images et vidéos dans un dossier et ses sous-dossiers"
    },
    "Ramène à la racine": {
        "file": Dossier + "RameneFichiersALaRacine.py",
        "desc": "Déplace tous les fichiers d'un dossier et ses sous-dossiers vers la racine, dans des dossiers photos et vidéos"
    },
    "Tri photos": {
        "file": Dossier + "TriPhotos.py",
        "desc": "Ouvre les photos d'un dossier une par une, avec la possibilité de les supprimer ou non (oui = Espace / non = A)"
    },
    "Tri videos": {
        "file": Dossier + "TriVideos.py",
        "desc": "Ouvre les vidéos d'un dossier une par une, avec la possibilité de les supprimer ou non (oui = Espace / non = A)"
    },
    "Trouver les fichiers d'une date précise": {
        "file": Dossier + "TrouverFichierDuneDatePrecise.py",
        "desc": "Trouve et liste les fichiers créés à une date précise dans un dossier et ses sous-dossiers"
    },
    "Créer des sous-dossiers aléatoires": {
        "file": Dossier + "SousDossiersAleatoires.py",
        "desc": "Crée des sous-dossiers aléatoires dans un dossier et y déplace les fichiers. Permet de simuler un désordre."
    },
}

# --- Construire le layout ---
layout_scroll = [
    [sg.Text("📂 Tri Photos/Vidéos", font=("Poppins", 18, "bold"), justification="left", expand_x=True)],
    [sg.Text("Choisissez une action :", font=("Poppins", 12), pad=(0,10))]
]

button_map = {}
for i, (name, info) in enumerate(SCRIPTS.items()):
    btn_key = f'-BTN-{i}-'
    layout_scroll.append([sg.Button(name, size=(32,1), key=btn_key, font=("Poppins", 10), pad=(5,10))])
    layout_scroll.append([sg.Text(info["desc"], size=(38, 3), auto_size_text=False, text_color="lightgray", font=("Roboto", 10))])
    layout_scroll.append([sg.Frame('', [[]], size=(100,1), background_color="#3c5076", pad=(20,10), relief=sg.RELIEF_FLAT)])
    button_map[btn_key] = info["file"]

layout = [
    [sg.Column(layout_scroll, size=(350, 520), scrollable=True, vertical_scroll_only=True)],
    [sg.Button("Quitter", button_color=("white", "firebrick4"), size=(12,1))]
    ]

# --- Créer la fenêtre ---
window = sg.Window("Launcher", layout, size=(350, 580), resizable=True, finalize=True, element_justification="left", location=(200, 200))
window.BringToFront()


# --- Boucle principale ---
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Quitter"):
        break
    if event in button_map:
        script_path = os.path.join(os.getcwd(), button_map[event])
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path])
        else:
            sg.popup_error(f"Script non trouvé : {script_path}")

window.close()
