@echo off
title Etape 8 - Git v4
cd /d C:\Users\LENOVO\sensante
color 0A

cls
echo.
echo  ============================================================
echo   COMMANDE 1 : git status
echo  ============================================================
echo.
git status
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 2 : git add .
echo  ============================================================
echo.
git add .
echo  (done - fichiers stagues)
git status --short
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 3 : git commit -m "Lab 5 : integration LLM Groq + /explain (v4)"
echo  ============================================================
echo.
git commit -m "Lab 5 : integration LLM Groq + /explain (v4)"
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 4 : git push origin main
echo  ============================================================
echo.
git push origin main
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 5 : git tag v4
echo  ============================================================
echo.
git tag v4
echo  Tags existants :
git tag
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 6 : git push origin v4
echo  ============================================================
echo.
git push origin v4
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 7 : git log --oneline
echo  ============================================================
echo.
git log --oneline
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

echo.
echo  ============================================================
echo   FIN - Toutes les captures effectuees !
echo  ============================================================
pause
