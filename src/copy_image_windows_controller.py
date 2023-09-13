
# https://stackoverflow.com/questions/34322132/copy-image-to-clipboard
# https://stackoverflow.com/questions/7050448/write-image-to-windows-clipboard-in-python-with-pil-and-win32clipboard


# import ctypes
# from ctypes import wintypes
# # Constants for Windows API
# CF_HDROP = 15

# # Load necessary Windows functions from ctypes
# user32 = ctypes.windll.user32
# # Load necessary Windows functions from ctypes
# kernel32 = ctypes.windll.kernel32
# # Function to copy a list of file paths to the clipboard
# def copy_image_to_clipboard_on_windows(file_path):
#     file_paths = [file_path]
#     file_paths_str = '\0'.join(file_paths) + '\0\0'
#     buffer_size = len(file_paths_str.encode('utf-16le'))
    
#     hdrop = kernel32.GlobalAlloc(CF_HDROP, buffer_size)
#     pdrop = kernel32.GlobalLock(hdrop)
    
#     ctypes.windll.kernel32.MultiByteToWideChar(0, 0, file_paths_str, -1, pdrop, buffer_size)
    
#     kernel32.GlobalUnlock(hdrop)
    
#     ctypes.windll.ole32.CoInitialize(None)
    
#     ctypes.windll.user32.OpenClipboard(None)
#     ctypes.windll.user32.EmptyClipboard()
#     ctypes.windll.user32.SetClipboardData(CF_HDROP, hdrop)
#     ctypes.windll.user32.CloseClipboard()

# -------------------------------------------------------------------------
# Load the image
# image_path = 'C:/Users/m/Documents/files/ice.jpg'

# VERSION 2 ---------------------------------------------------------------------
# Convert the image to PNG, but does not copy gif animation

import os
import re
from tkinter import messagebox
from PIL import Image
import io
import win32clipboard
from io import BytesIO

import subprocess

from copy_file_windows_controller import copy_files_windows

class CopyImageWindowsController:
    def __init__(self):
        pass
    
    def copy_image_to_clipboard_on_windows(self, filepath):
        
        if self.is_gif_file(filepath):
            file_list = [filepath]
            copy_files_windows(file_list)
            return
        
        # In the following, we will insert data into windows clipboard.
        # Windows clipboard has mulitple "slots" and formats that you can set at once.
        # We will set both the "BMP" for lowtech apps, and "PNG" for apps that understand that
        
        # BMP (CF_DIB) - Copy as BMP to clipboard, works for: --------------------
        # Here we will set the "BMP" slot in the clipboard for lowtech apps
        # MS Paint and other low tech apps
        data = None
        if self.is_png_file(filepath):
            # Add a white background - If a white bg is not added, all png images will have black background in low teck apps
            image = Image.open(filepath)
            memory = io.BytesIO()                
            width, height = image.size
            white_background = Image.new("RGB", (width, height), (255, 255, 255))
            # Paste the original image onto the white background
            white_background.paste(image, (0, 0), image)
            white_background.save(memory, format='bmp')
            
            # Here img is PilImage object
            image.convert('RGB')
            image.save(memory, format='bmp')
            data = memory.getvalue()[14:]
        else:
            image = Image.open(filepath)
            memory = io.BytesIO()

            # Here img is PilImage object
            image.convert('RGB')
            image.save(memory, format='bmp')

            data = memory.getvalue()[14:]

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)        
        
        # PNG - Works for: ---------------------------------------
        # Here we will set the "PNG" slot in the clipboard for apps that understand transparency
        # Ms Word, Google Docs, Gmail
        image = Image.open(filepath)
        buffer = io.BytesIO()
        image.save(fp=buffer, format='PNG')
        clipboard_format = win32clipboard.RegisterClipboardFormat('PNG')
        # win32clipboard.OpenClipboard()
        # win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clipboard_format, buffer.getvalue())

        win32clipboard.CloseClipboard()

        buffer.close()

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



# VERSION 1 ---------------------------------------------------------------------
# Convert the image to BMP and add a white background for transparent images:

# def copy_image_to_clipboard_on_windows(filepath):
    
#     clip_type = win32clipboard.CF_DIB
    
#     image = Image.open(filepath)

#     # Create a new image with a white background
#     white_bg = Image.new("RGB", image.size, (255, 255, 255))
    
#     # Paste the non-transparent parts of the image onto the white background
#     white_bg.paste(image, mask=image.split()[3])
    
#     output = BytesIO()
#     white_bg.convert("RGB").save(output, "BMP")
#     data = output.getvalue()[14:]
#     output.close()

#     win32clipboard.OpenClipboard()
#     win32clipboard.EmptyClipboard()
#     win32clipboard.SetClipboardData(clip_type, data)
#     win32clipboard.CloseClipboard()


# GHND doenst work ---------------------------------------------------------------------------

# import win32clipboard
# import win32con
# import ctypes
# import os

# def copy_image_to_clipboard_on_windows(filepath):


#     # Specify the file path you want to put in the clipboard
#     file_path = filepath

#     # Open the clipboard
#     win32clipboard.OpenClipboard()

#     try:
#         # Calculate the size of DROPFILES structure and file path
#         file_size = len(file_path.encode('utf-16')) + 2  # Length in bytes including the null terminator
#         dropfiles_size = ctypes.sizeof(ctypes.c_void_p) + file_size
        
#         # Allocate global memory object
#         h_mem = ctypes.windll.kernel32.GlobalAlloc(win32con.GHND, dropfiles_size)
        
#         # Lock the memory object
#         mem_data = ctypes.windll.kernel32.GlobalLock(h_mem)
        
#         # Create the DROPFILES structure in memory
#         dropfiles = (ctypes.c_void_p).from_address(mem_data)
#         dropfiles.value = ctypes.sizeof(ctypes.c_void_p)
        
#         # Copy the file path after the DROPFILES structure
#         file_path_encoded = file_path.encode('utf-16')
#         ctypes.memmove(mem_data + ctypes.sizeof(ctypes.c_void_p), file_path_encoded, file_size)
        
#         # Unlock the memory object
#         ctypes.windll.kernel32.GlobalUnlock(h_mem)
        
#         # Set the clipboard data using CF_HDROP format
#         win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, h_mem)
        
#         print("File path copied to clipboard successfully.")
#     except Exception as e:
#         print("An error occurred:", e)
#     finally:
#         # Close the clipboard
#         win32clipboard.CloseClipboard()
#         print("Closing Clipboard")



# CF_TYPES = {win32clipboard.CF_TEXT: 'CF_TEXT',
#             win32clipboard.CF_BITMAP: 'CF_BITMAP',
#             win32clipboard.CF_METAFILEPICT: 'CF_METAFILEPICT',
#             win32clipboard.CF_SYLK: 'CF_SYLK',
#             win32clipboard.CF_DIF: 'CF_DIF',
#             win32clipboard.CF_TIFF: 'CF_TIFF',
#             win32clipboard.CF_OEMTEXT: 'CF_OEMTEXT',
#             win32clipboard.CF_DIB: 'CF_DIB',
#             win32clipboard.CF_PALETTE: 'CF_PALETTE',
#             win32clipboard.CF_PENDATA: 'CF_PENDATA',
#             win32clipboard.CF_RIFF: 'CF_RIFF',
#             win32clipboard.CF_WAVE: 'CF_WAVE',
#             win32clipboard.CF_UNICODETEXT: 'CF_UNICODETEXT',
#             win32clipboard.CF_ENHMETAFILE: 'CF_ENHMETAFILE',
#             win32clipboard.CF_HDROP: 'CF_HDROP',
#             win32clipboard.CF_LOCALE: 'CF_LOCALE',
#             win32clipboard.CF_DIBV5: 'CF_DIBV5',

#             0x0080: 'CF_OWNERDISPLAY',
#             0x0081: 'CF_DSPTEXT',
#             0x0082: 'CF_DSPBITMAP',
#             0x008E: 'CF_DSPENHMETAFILE'}
