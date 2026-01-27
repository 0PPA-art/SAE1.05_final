# Script généré - SAE 1.05

$confirmation = Read-Host "Etes-vous bien certain(e) ? (OUI)"
if ($confirmation -eq "OUI") {
    Remove-Item -Path @(
        "C:\Users\sicha\Pictures\Numérisations\Numérisation_20250402.pdf"
    ) -Force -ErrorAction SilentlyContinue
    Write-Output "Suppression terminée."
} else {
    Write-Output "Opération annulée..."
}
