# mkdir dist_linux
# chmod 777 dist_linux
# sudo chmod -R 777
venv\Scripts\Activate.ps1
pyinstaller --onefile --distpath=./dist_windows_exe ./src/main.py