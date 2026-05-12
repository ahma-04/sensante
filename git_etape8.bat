@echo off
title Etape 8 - Git v4
cd /d C:\Users\LENOVO\sensante
color 0A

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
echo  (fichiers stagges avec succes)
git status --short
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 3 : git commit
echo  ============================================================
echo.
git commit -m "Lab 5 : integration LLM Groq + /explain (v4)" 2>nul || echo  Deja commite - arbre de travail propre
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 4 : git log --oneline
echo  ============================================================
echo.
git log --oneline
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 5 : git tag v4
echo  ============================================================
echo.
git tag 2>nul
echo  Tags existants :
git tag
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

cls
echo.
echo  ============================================================
echo   COMMANDE 6 : git show v4 --stat
echo  ============================================================
echo.
git show v4 --stat
echo.
echo  >>> Faites la capture maintenant (Win+Shift+S) <<<
pause

echo.
echo  ============================================================
echo   FIN DE L ETAPE 8 - Toutes les captures effectuees !
echo  ============================================================
pause
