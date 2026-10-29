@echo off
REM Create an EMPTY repo named online-exam-system on GitHub first.
git init
git branch -M main
git remote add origin https://github.com/SHIVU-777/online-exam-system.git

git checkout -b v1
git add v1 k8s .gitignore README.md *.bat
git commit -m "v1: MCQ quiz"
git push -u origin v1

git checkout -b v2
git add v2
git commit -m "v2: auto score"
git push -u origin v2

git checkout -b v3
git add v3
git commit -m "v3: result page"
git push -u origin v3

git checkout main
git merge v3
git push -u origin main
pause
