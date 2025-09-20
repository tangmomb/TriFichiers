import os
import datetime
import FreeSimpleGUI as sg
from LocationInterface import POPUP_LOCATION

def trouver_fichiers_modifies(folder_path, date_cible_str):
    # Convertir la date cible en objet datetime.date
    date_cible = datetime.datetime.strptime(date_cible_str, "%d/%m/%Y").date()

    fichiers_trouves = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            chemin_complet = os.path.join(root, file)
            try:
                modif_time = os.path.getmtime(chemin_complet)
                modif_date = datetime.date.fromtimestamp(modif_time)
                if modif_date == date_cible:
                    fichiers_trouves.append(chemin_complet)
            except Exception as e:
                sg.popup(f"Erreur avec {chemin_complet} : {e}", location=POPUP_LOCATION)

    return fichiers_trouves

if __name__ == "__main__":
    dossier = sg.popup_get_folder("Chemin du dossier à scanner :\nexemple : C:\\Dossier", location=POPUP_LOCATION)
    date_voulue = sg.popup_get_text("Date ? : jj/mm/aaaa : ", location=POPUP_LOCATION).strip()  # format JJ/MM/AAAA

    sg.popup("Voir console pour les résultats.", location=POPUP_LOCATION).strip()

    resultats = trouver_fichiers_modifies(dossier, date_voulue)

    print(f"\nFichiers modifiés le {date_voulue} :")
    for chemin in resultats:
        print(chemin)

    print(f"\nTotal : {len(resultats)} fichier(s) trouvé(s).")
