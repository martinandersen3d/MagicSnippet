# mkdir dist_linux
# chmod 777 dist_linux
# sudo chmod -R 777
venv\Scripts\Activate.ps1
# pyinstaller --noconsole --onefile --distpath=./dist_windows_exe ./src/main.py

# Note: --noconsole, disables a stupid popup console window when the app launch and have a GUI. Only use this flag, if you have a CLI app.

# TODO: The generated EXE file takes 1-2 seconds to start.. that is not good enougth
# TODO: Solution: If i remove "--onefile" it will create a directory with files and one exe, this is really fast.

# pyinstaller --onefile --noconsole --exclude-module tcl --exclude-module tk --exclude-module _tkinter --distpath=./dist_windows_exe ./src/main.py
# pyinstaller --noconsole --exclude-module tcl --exclude-module tk --distpath=./dist_windows_exe ./src/main.py

# pyinstaller --noconsole --exclude-module tcl `
# --exclude-module tk `
# --exclude-module _tkinter `
# --exclude-module readline `
# --exclude-module docutils `
# --exclude-module unittest `
# --exclude-module pydoc `
# --exclude-module email `
# --exclude-module html `
# --exclude-module http `
# --exclude-module xml `
# --exclude-module concurrent `
# --exclude-module queue `
# --exclude-module test `
# --exclude-module easy_install `
# --exclude-module setuptools `
# --exclude-module distribute `
# --exclude-module pip `
# --exclude-module wheel `
# --distpath=./dist_windows_exe ./src/main.py

# I think this is the optimal _minimal_ starter settings, enable more if needed - depending on you project requirement

pyinstaller --noconsole `
--exclude-module tcl `
--exclude-module _bz2 `
--exclude-module _decimal `
--exclude-module _hashlib `
--exclude-module _lzma `
--exclude-module _socket `
--exclude-module _ssl `
--exclude-module bz2 `
--exclude-module concurrent `
--exclude-module distribute `
--exclude-module distutils `
--exclude-module doctest `
--exclude-module docutils `
--exclude-module easy_install `
--exclude-module email `
--exclude-module gzip `
--exclude-module html `
--exclude-module http `
--exclude-module http `
--exclude-module IPython `
--exclude-module lzma `
--exclude-module nose `
--exclude-module nose2 `
--exclude-module packaging `
--exclude-module pip `
--exclude-module pkg_resources `
--exclude-module pydoc `
--exclude-module pyreadline `
--exclude-module pytest `
--exclude-module queue `
--exclude-module readline `
--exclude-module readline `
--exclude-module setuptools `
--exclude-module setuptools `
--exclude-module sqlite3 `
--exclude-module tarfile `
--exclude-module test `
--exclude-module tk `
--exclude-module unittest `
--exclude-module unittest `
--exclude-module wheel `
--exclude-module xml `
--exclude-module xml `
--exclude-module zipfile `
--exclude-module zlib `
--distpath=./dist_windows_exe ./src/main.py



