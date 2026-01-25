import sys
import json
from pathlib import Path #juste mieux que os.path
from typing import List, Tuple

def scan_fichiers(racine: Path, max_count: int = 100, min_size_mb: float = 10.0) -> List[Tuple[str, int]]:
    min_size = int(min_size_mb * 1024 * 1024) # conversion de notre taille de fichier de Mo en octets
    fichiers: List[Tuple[str, int]] = [] #besoin d'une liste pour stocker la taille du fichier

    print(f"Scan récursif de : {racine}")
    print("veuillez patienter :")
#partie assez bizzare avec un peut de d'IA, mais qui est necessaire car manque de solution
    for item in racine.rglob("*"): # parcours récursif de tous les fichiers et dossiers contenus dans racine et ses #sous-dossiers rglob = version “récursive” de glob de globale
        if item.is_file(): #on vas supprimer sur notre analyse les dossiers et regarder uniquement a l interieur
            try: # voir le site www.w3schools.com. Mais il vas teste un bloc de code et voir si il y a une erreur
                size = item.stat().st_size #size vas récup les donnees du fichier
                if size >= min_size:
                    fichiers.append((str(item), size))
            except (PermissionError, FileNotFoundError, OSError):
                pass  # on ignore les erreurs d'accès pour obtenir le fichier

    # Tri décroissant par taille
    fichiers.sort(key=lambda x: x[1], reverse=True)
    return fichiers[:max_count]


if __name__ == "__main__":
    dossier = Path(sys.argv[1]).resolve()

    if not dossier.is_dir():
        sys.exit(1)

    fichiers1 = scan_fichiers(dossier)

    # Préparation pour json : on double les backslashes sous Windows
    data = [[chemin.replace("\\", "\\\\"), taille] for chemin, taille in =fichiers1]

    with open("gros_fichiers.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)