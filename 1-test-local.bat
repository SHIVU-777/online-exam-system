@echo off
echo === Installing Flask and pytest ===
py -m pip install flask pytest
for %%v in (v1 v2 v3) do (
    echo === Testing %%v ===
    pushd %%v
    py -m pytest -q
    popd
)
echo.
echo Starting v1 on http://localhost:5000  (press Ctrl+C to stop)
cd v1
py app.py
