import sys
import json
import random
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QColor

# Import des 4 classes fournies (nécessaires pour l'interface)
from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons

# Constantes
NB_MAX = 100
NB_PAGE = 25
FICHIER_JSON = "gros_fichiers.json"  # pour notre fichier Json


# Fonction pour la couleur du camembert
def generer_couleurs(nb: int) -> list[QColor]:
    random.seed(42)
    couleurs = []
    for _ in range(nb):
        r = random.randint(60, 240)
        g = random.randint(60, 240)
        b = random.randint(60, 240)
        couleurs.append(QColor(r, g, b))
    return couleurs


# Fonction pour le fichier json
def charger_donnees_json() -> list[list]:
    try:
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Corrige les doubles backslashes Windows
        return [[chemin.replace("\\\\", "\\"), taille] for chemin, taille in data]
    except Exception as e:
        print(f"Erreur lecture {FICHIER_JSON} : {e}")
        return []


def generer_script_suppression(fichiers, pages_legendes, fenetre):
    selectionnes = []

    for leg in pages_legendes:
        etats = leg.recupere_etats_cases_a_cocher()
        for i, coche in enumerate(etats):
            if coche:
                idx = leg.num_legende_start + i
                if idx < len(fichiers):
                    chemin = fichiers[idx][0]
                    selectionnes.append(chemin)

    if not selectionnes:
        QMessageBox.information(fenetre, "Information", "Aucun fichier sélectionné.")
        return

    # Confirmation utilisateur
    msg = f"Supprimer {len(selectionnes)} fichier(s) ?\n\nContinuer ?"
    reponse = QMessageBox.question(fenetre, "Confirmation", msg,
                                   QMessageBox.Yes | QMessageBox.No)

    if reponse != QMessageBox.Yes:
        return

    fichier_ps1 = "supprimer_fichiers.ps1"
    with open(fichier_ps1, "w", encoding="utf-8") as f:
        f.write("# Script généré- SAE 1.05\n\n")
        f.write('if ($confirm -eq "OUI") {\n')
        f.write('    Remove-Item -Path `\n')
        for chemin in selectionnes:
            # Échappe les backslashes pour PowerShell
            chemin_esc = chemin.replace("\\", "\\\\").replace('"', '\\"')
            f.write(f'        "{chemin_esc}", `\n')
        f.write('        -Force -ErrorAction SilentlyContinue\n')
        f.write('}\n')

    QMessageBox.information(fenetre, "Succès",
                            f"Script créé : {fichier_ps1}\n\nExécutez-le avec PowerShell.")


def construire_interface(fichiers, couleurs, fenetre):
    pages_legendes = []

    # Onglet Camembert
    cam = Camembert(fichiers, couleurs)
    fenetre.add_onglet("Camembert", cam.dessine_camembert())

    # Onglets Légendes (25 par page)
    nb_pages = (len(fichiers) + NB_PAGE - 1) // NB_PAGE

    for num_page in range(nb_pages):
        debut = num_page * NB_PAGE
        leg = Legendes(
            liste_fichiers=fichiers,
            liste_couleurs=couleurs,
            num_legende_start=debut,
            nb_legende_par_page=NB_PAGE
        )
        widget_leg = leg.dessine_legendes()
        titre = f"Légende {num_page + 1}"
        fenetre.add_onglet(titre, widget_leg)
        pages_legendes.append(leg)

    # Bouton de suppression
    repertoire_base = str(Path.cwd().resolve())  # dossier scanné

    def callback_generation():
        generer_script_suppression(fichiers, pages_legendes, fenetre)

    boutons = Boutons(repertoire_base, callback_generation)
    widget_boutons = boutons.dessine_boutons()
    fenetre.add_onglet("IHM", widget_boutons)  # onglet pour la suppression de fichiers

    return pages_legendes


if __name__ == "__main__":
    app = QApplication(sys.argv)

    fichiers = charger_donnees_json()
    if not fichiers:
        QMessageBox.critical(None, "Erreur", f"Aucun fichier trouvé dans {FICHIER_JSON}")
        sys.exit(1)

    couleurs = generer_couleurs(len(fichiers))
    fenetre = Onglets()
    pages_legendes = construire_interface(fichiers, couleurs, fenetre)
    fenetre.show()
    sys.exit(app.exec_())
