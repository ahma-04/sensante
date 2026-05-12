cd C:\Users\LENOVO\sensante

Clear-Host
Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host "   COMMANDE 1 : git status" -ForegroundColor Cyan
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host ""
git status
Write-Host ""
Write-Host "  >>> Faites la capture maintenant (Win+Shift+S) <<<" -ForegroundColor Yellow
Read-Host "  Appuyez sur ENTREE pour continuer"

Clear-Host
Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host "   COMMANDE 2 : git add ." -ForegroundColor Cyan
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host ""
git add .
Write-Host "  (fichiers stagues avec succes)" -ForegroundColor Green
Write-Host ""
Write-Host "  >>> Faites la capture maintenant (Win+Shift+S) <<<" -ForegroundColor Yellow
Read-Host "  Appuyez sur ENTREE pour continuer"

Clear-Host
Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host '   COMMANDE 3 : git commit -m "Lab 5 : integration LLM Groq + /explain (v4)"' -ForegroundColor Cyan
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host ""
git commit -m "Lab 5 : integration LLM Groq + /explain (v4)"
Write-Host ""
Write-Host "  >>> Faites la capture maintenant (Win+Shift+S) <<<" -ForegroundColor Yellow
Read-Host "  Appuyez sur ENTREE pour continuer"

Clear-Host
Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host "   COMMANDE 4 : git push origin main" -ForegroundColor Cyan
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host ""
git push origin main
Write-Host ""
Write-Host "  >>> Faites la capture maintenant (Win+Shift+S) <<<" -ForegroundColor Yellow
Read-Host "  Appuyez sur ENTREE pour continuer"

Clear-Host
Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host "   COMMANDE 5 : git tag v4" -ForegroundColor Cyan
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host ""
git tag v4
Write-Host "  Tags existants :" -ForegroundColor Green
git tag
Write-Host ""
Write-Host "  >>> Faites la capture maintenant (Win+Shift+S) <<<" -ForegroundColor Yellow
Read-Host "  Appuyez sur ENTREE pour continuer"

Clear-Host
Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host "   COMMANDE 6 : git push origin v4" -ForegroundColor Cyan
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host ""
git push origin v4
Write-Host ""
Write-Host "  >>> Faites la capture maintenant (Win+Shift+S) <<<" -ForegroundColor Yellow
Read-Host "  Appuyez sur ENTREE pour continuer"

Clear-Host
Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host "   COMMANDE 7 : git log --oneline" -ForegroundColor Cyan
Write-Host "  ============================================================" -ForegroundColor Cyan
Write-Host ""
git log --oneline
Write-Host ""
Write-Host "  >>> Faites la capture maintenant (Win+Shift+S) <<<" -ForegroundColor Yellow
Read-Host "  Appuyez sur ENTREE pour terminer"

Write-Host ""
Write-Host "  ============================================================" -ForegroundColor Green
Write-Host "   FIN - Toutes les captures effectuees !" -ForegroundColor Green
Write-Host "  ============================================================" -ForegroundColor Green
Read-Host "  Appuyez sur ENTREE pour fermer"
