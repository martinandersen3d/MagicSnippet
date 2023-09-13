
import os
import io
import re
import subprocess
from PIL import Image
# Works with: PNG, Animated GIF
# Some applications can not insert a JPG file if the mimetype is set to PNG and reverse
# Some applications can not insert a PNG file if the mimetype is set to JPG and reverse
# Solution: Convert all JPG to PNG
# Converting all JPG to PNG gives the best application compatibility
# The raw image with all its bytes will be stored in the clipboard

class CopyImageLinuxController:
    def __init__(self):
        pass
    
    def copy_image_to_clipboard_on_linux(self, path: str):
        
        DISPLAY = os.environ.get("DISPLAY", ":0")
        # Copies the image at the given path into the system clipboard.
        
        if self.is_jpg_file(path):
            # Open the JPG image using Pillow
            with Image.open(path) as img:
                # Create an in-memory PNG image
                png_data = io.BytesIO()
                img.save(png_data, format="PNG")
                png_data.seek(0)  # Reset the file pointer

            cmd = f'xclip -d {DISPLAY} -selection clipboard -t image/png -i'
            subprocess.run(cmd, shell=True, input=png_data.getvalue(), check=False)
        else:
            cmd = f'xclip -d {DISPLAY} -selection clipboard -t image/png -i "{path}"'
            subprocess.run(cmd, shell=True, check=False)

    def is_gif_file(self, image_fullpath):
        # Extract the file extension
        _, file_ext = os.path.splitext(image_fullpath)
        
        # Remove the dot from the extension
        file_ext = file_ext[1:].lower()
        
        # Check if the extension matches jpg, gif, or png using regular expressions
        if re.match(r"^(gif)$", file_ext):
            return True
        return False


    def is_png_file(self, image_fullpath):
        # Extract the file extension
        _, file_ext = os.path.splitext(image_fullpath)
        
        # Remove the dot from the extension
        file_ext = file_ext[1:].lower()
        
        # Check if the extension matches jpg, gif, or png using regular expressions
        if re.match(r"^(png)$", file_ext):
            return True
        return False
    
    def is_jpg_file(self, image_fullpath):
        _, file_ext = os.path.splitext(image_fullpath)
        file_ext = file_ext[1:].lower()
        if re.match(r"^(jpg|jpeg)$", file_ext):
            return True
        return False
