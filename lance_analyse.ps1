# forcer le dossier en dossier courant
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path #scripteDir prend le chemin
Set-Location -Path $scriptDir -ErrorAction Stop

# cherche la commande py
$pythonCommands = @("py") 
$python = $null
#recherche la première commande Python qui existe sur #l’ordinateur, parmi une liste.
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

# partie Choix du dossier
#On commence à le choisir ici avec dossierRaw ,et 2>$null est une redirection d'erreur
$dossierraw = & $python ".\scripte_1.py" 2>$null # ces juste pour avoir le scripte python stocker dans la variable
$dossier = $dossierraw.Trim() # Trim() sert  à supprimer les espace inutile si jamais

#on previent qu'il y a un dossier
Write-Host "Dossier : $dossier"

# Chemin absolu du script d'analyse
$analyseScript = Join-Path -Path $scriptDir -ChildPath "scripte2.py"
#$futurechemin = cmdassemblerdechemin #dossierdebase ciblescripte.ps1 insertunnomdefichier

Write-Host "Exécution : $python `"$analyseScript`" `"$dossier`""

& $python $analyseScript $dossier


#crée un fichier json pour obtenir un aperçus du scripte analyse
$jsonPath = Join-Path -Path $scriptDir -ChildPath "gros_fichiers.json"

if (Test-Path $jsonPath -PathType Leaf) {
    Write-Host "gros_fichiers.json cree"
    # partie interface
    $interfaceScript = Join-Path -Path $scriptDir -ChildPath "scripte3.py"
    & $python $interfaceScript
} else {
    Write-Host "gros_fichiers.json impossible cree"
}
pause