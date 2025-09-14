import os
import datetime
import FreeSimpleGUI as sg

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
                sg.popup(f"Erreur avec {chemin_complet} : {e}")

    return fichiers_trouves

if __name__ == "__main__":
    dossier = sg.popup_get_text("Chemin du dossier à scanner : ").strip()
    date_voulue = sg.popup_get_text("Date ? : jj/mm/aaaa : ").strip()  # format JJ/MM/AAAA

    resultats = trouver_fichiers_modifies(dossier, date_voulue)

    sg.popup(f"\nFichiers modifiés le {date_voulue} :")
    for chemin in resultats:
        sg.popup(chemin)

    sg.popup(f"\nTotal : {len(resultats)} fichier(s) trouvé(s).")
