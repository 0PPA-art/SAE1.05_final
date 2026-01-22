# choisir_dossier.py
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

appli = QApplication(sys.argv) #application pour obtenir 
dossier = QFileDialog.getExistingDirectory(
    None,
    "Choisir le dossier à analyser",
    options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
)

if dossier:
    print(dossier.replace('\\', '/'))   # <-- c'est pour eviter les problemes dargument quand il vas choisir le dossier merci windows
else:
    print("")