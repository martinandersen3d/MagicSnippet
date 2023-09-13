# mkdir dist_linux
# chmod 777 dist_linux
# sudo chmod -R 777
source venv/bin/activate
pyinstaller --onefile --distpath=./dist_linux_binary ./src/main.py