@echo off
set USER=shivanesh77
echo === Docker login (enter your DockerHub password/token) ===
docker login -u %USER%
for %%v in (v1 v2 v3) do (
    echo === Building and pushing %%v ===
    docker build -t %USER%/online-exam:%%v %%v
    docker push %USER%/online-exam:%%v
)
echo.
echo Done. Check https://hub.docker.com/r/%USER%/online-exam/tags
pause
