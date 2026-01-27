Write-Output "Script PowerShell pour supprimer des fichiers sans confirmation"
Write-Output "Attention : cette suppression est définitivement ..."
$reponse = Read-Host "Veuillez confirmer la suppression de tous ces fichiers : (OUI)"
if ($reponse -eq "OUI") {
    $confirmation = Read-Host "Etes-vous bien certain(e) ? (OUI)"
    if ($confirmation -eq "OUI") {
        Remove-Item -Path "C:\Users\sicha\Pictures\Numérisations\Numérisation_20250402.pdf" -Force
    } else {
        Write-Output "Opération annulée..."
    }
} else {
    Write-Output "Opération annulée..."
}
