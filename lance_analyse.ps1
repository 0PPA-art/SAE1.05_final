# ./lance_analyse.ps1

# === FORCER le dossier du script comme dossier courant ===
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path $scriptDir -ErrorAction Stop

Write-Host "(U:\Bureau\SAE1.05) : $(Get-Location)"

# cherche la commande py
$pythonCommands = @("py") 
$python = $null
#merci internet de m expliquer, Elle essaie de trouver la première commande Python qui existe vraiment sur #l’ordinateur de l’utilisateur, parmi une liste de noms possibles.
foreach ($cmd in $pythonCommands) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $python = $cmd
        break
   }
}
#Si elle n’existe pas
if (-not $python) {
    Write-Host "exit 1"
    pause
    exit 1
}

#Write-Host "Python détecté : $python"

# partie Choix du dossier
#On commence à le choisir ici avec dossierRaw ,et 2>$null est une redirection d'erreur rappel des cours d'Hensel
$dossierraw = & $python ".\scripte_1.py" 2>$null # ces juste pour avoir le scripte python stocker dans la variable
$dossier = $dossierraw.Trim() # Trim() sert  à supprimer les espace inutile si jamais

#On previent si y pas de dossier
if (-not $dossier -or $dossier -eq "") {
    Write-Host "pas de dossier"
    pause
    exit
}
# previent si le dossier est impossible à ouvrir merci mes cours de BTS
if (-not (Test-Path $dossier -PathType Container)) {
    Write-Host "pas possible ce dossier → $dossier"
    pause
    exit
}
#on previent qu'il y a un dossier
Write-Host "Dossier : $dossier"

# Lancement analyse (avec chemin)
Write-Host "Lancement"

# Chemin absolu du script d'analyse
$analyseScript = Join-Path -Path $scriptDir -ChildPath "scripte2.py" #$futurechemin = cmdassemblerdechemin #dossierdebase ciblescripte.ps1 insertunnomdefichier

Write-Host "Exécution : $python `"$analyseScript`" `"$dossier`""

& $python $analyseScript $dossier

# partie interface
#crée un fichier json pour obtenir un aperçus du scripte analyse
$jsonPath = Join-Path -Path $scriptDir -ChildPath "gros_fichiers.json"

if (Test-Path $jsonPath -PathType Leaf) {
    Write-Host "gros_fichiers.json cree"
    
    $interfaceScript = Join-Path -Path $scriptDir -ChildPath "scripte3.py"
    & $python $interfaceScript
} else {
    Write-Host "gros_fichiers.json impossible cree"
}

Write-Host ""
pause