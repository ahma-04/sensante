@echo off
title Etape 8 - Git : Sauvegarder version v4
cd /d C:\Users\LENOVO\sensante
color 0A

echo.
echo  ============================================================
echo   ETAPE 8 : Git - Sauvegarder la version v4
echo  ============================================================
echo.

echo  --- Etape 8.1 : Verifier que .env est ignore ---
echo.
echo  ^> git status
echo.
git status
echo.
echo  ============================================================
echo   Verification : .env n'apparait PAS dans la liste ci-dessus
echo  ============================================================
echo.
pause

echo.
echo  --- Etape 8.2 : Voir les fichiers commites ---
echo.
echo  ^> git log --oneline
echo.
git log --oneline
echo.
pause

echo.
echo  --- Etape 8.3 : Voir le tag v4 ---
echo.
echo  ^> git tag
echo.
git tag
echo.
pause

echo.
echo  --- Etape 8.4 : Detail du commit v4 ---
echo.
echo  ^> git show v4 --stat
echo.
git show v4 --stat
echo.
echo  ============================================================
echo   FIN - Faites votre capture (Win+Shift+S)
echo  ============================================================
echo.
pause
