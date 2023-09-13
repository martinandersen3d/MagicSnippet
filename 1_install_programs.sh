#  RUN AS SUDO

mkdir src 
touch ./src/requirements.txt
touch ./src/main.py
sudo apt-get update
sudo apt-get install python3
pip3 install --upgrade pip