import os
import subprocess

def copy_file_linux_x11_gnome(fullpath):
    uris = f"copy\nfile://{fullpath}"
    encoded_data = f"{uris}".encode("utf-8")
    print(encoded_data)
    try:
        subprocess.run(["xclip", "-i", "-selection", "clipboard", "-t", "x-special/gnome-copied-files"], input=encoded_data)
    except Exception as e:
        print("An error occurred:", e)
        
def copy_file_linux_x11_other_programs(fullpath):
    uris = f"file://{fullpath}\r\n"
    encoded_data = f"{uris}".encode("utf-8")
    print(encoded_data)
    try:
        subprocess.run(["xclip", "-i", "-selection", "clipboard", "-t", "text/uri-list"], input=encoded_data)
    except Exception as e:
        print("An error occurred:", e)
        
def copy_file_linux_x11_wayland(fullpath):
    pass