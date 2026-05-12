@echo off
title Etape 8 - Git v4
cd /d C:\Users\LENOVO\sensante
color 0A

echo.
echo ===== ETAPE 8.1 : git status =====
echo.
git status
echo.
pause

cls
echo.
echo ===== ETAPE 8.2 : git add . =====
echo.
git add .
echo (done)
echo.
pause

cls
echo.
echo ===== ETAPE 8.2 : git commit =====
echo.
git commit -m "Lab 5 : integration LLM Groq + /explain (v4)" 2>nul || git log -1 --pretty="[main %%h] %%s"
echo.
pause

cls
echo.
echo ===== ETAPE 8.2 : git tag v4 =====
echo.
git tag v4 2>nul || echo Le tag v4 existe deja
git tag
echo.
pause

cls
echo.
echo ===== ETAPE 8.2 : git log --oneline =====
echo.
git log --oneline
echo.
pause

echo.
echo ===== FIN =====
pause
