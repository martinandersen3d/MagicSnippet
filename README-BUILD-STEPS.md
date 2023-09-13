# Create Python Binarys for Cross platform
- Windows Exe
- Linux Binary
- Linux .Appimage

# General steps:

**Windows:**

1. We will use Pythons Virtual Environment (VENV) to manage dependencies
2. We will use PyInstall to create the Exe file from .py file


**Linux:**
There is bash scripts for all the steps.

1. We will use Pythons Virtual Environment (VENV) to manage dependencies
2. We will use PyInstall to create the binary file from .py file
3. From the binary file we created, we will use Appimagetool to create .AppImage



# About Python Venv
This should not be added to source control


# Notes on Appimage

Naming convention - Use the same naming everywhere:

In the folder /build_appimage
the following must be the same name/wording:

- the folder "MyApp.AppDir" here you can change "MyApp"
- in build_appimage/MyApp.AppDir the file "MyApp.desktop" and "MyApp.png" must be the same
- /build_appimage/MyApp.AppDir/MyApp.desktop here "MyApp" can be changed
    - in this file, the "Name" and "icon" must be the same

Just follow the above and avoid any problems.

If you change name, you must update the 6_appimagetool_build.sh

# Notes on Windows and PyInstall - Exe start Slowness
- When i use the `pyinstall --onefile`, it creates ONE exe file. But the exe starts slow, like 1-2 sek.
- Solution: dont use the `--onefile` flag. It will create a directory with all needed files and one exe file - That starts Fast
- the flag `--noconfirm` skips some steps and build faster
to adjust what files is included in the Exe file, you can play with the `--exclude-module` here:

4_pyinstall_build_windows_no_console.ps1