
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import subprocess
import markdown

from app_settings_controller import AppSettingsController
from copy_file_linux_controller import copy_file_linux_x11_gnome, copy_file_linux_x11_other_programs
from copy_html_linux_controller import copy_html_to_clipboard_linux
from copy_image_linux_controller import CopyImageLinuxController
from copy_markdown_as_HTML_linux_controller import copy_markdown_as_HTML_clipboard_linux
from ui_popup_toast_copied import UiPopupToastCopied
if os.name == 'nt':
    from copy_html_windows_controller import HtmlClipboard, PutHtml
    from copy_file_controller import copy_files_windows
    from copy_image_windows_controller import CopyImageWindowsController
# from copy_image_controller import copy_image_to_clipboard_on_windows
# import asyncio
from ui import *
# from FileList import *
from search_algo import *
from ui_dialog_browserlink import UiBrowserLinkWindow
from ui_dialog_directory_settings import *
from ui_dialog_new_file import *
from ui_dialog_filepath_exclude import *
from ui_panel_codeviewer import FilePreviewQualityEnum, TextDisplayFrame
from directory_settings_controller import *
from file_controller import *
import pyperclip
import time
import pyautogui

class Controller:
    def __init__(self, root, app_version):
        
        self.app_version = app_version
        
        # On linux, there is two main ways you can run your desktop "x11" or "wayland". Check wich one is used.
        # This is important since some commandline tools, doesn't work on both.
        # x11 is the oldest and wayland is the newest 
        self.linux_session_type = "" # Can be "x11" or "wayland"
        if os.name == 'posix':
            # Run the command and capture its output
            result = subprocess.run('echo $XDG_SESSION_TYPE', stdout=subprocess.PIPE, text=True, shell=True)
            # Get the output and remove any leading/trailing whitespace
            self.linux_session_type = result.stdout.strip()
        
        self.AppSetting = AppSettingsController(self)
        self.DirectorySetting = DirectorySettingsController(self)
        # root is the tk.Tk() from Main.py
        self.root = root
        self.Ui = Ui( root, self)
        # self.set_statusbar('Loading..')
        self.alt_pressed = False
        self.shift_pressed = False
        self.ctrl_pressed = False
        # EVENT BINDINGS ------------------------------------
        
        # Globel hotkeys
        self.root.bind('<F1>', self.menu_copy_fullpath_to_clipboard)
        self.root.bind('<F2>', self.menu_copy_filename_to_clipboard)
        self.root.bind('<F3>', self.menu_copy_folderpath_to_clipboard)

        self.root.bind('<F4>', self.menu_copy_file_like_filemanager)
        self.root.bind('<F5>', self.menu_copy_file_linux_x11_other_programs)
        
        self.root.bind('<Control-d>', self.menu_open_selected_file_in_vscode)
        self.root.bind('<Control-e>', self.menu_open_selected_file_in_filemanager)
        self.root.bind('<Control-h>', self.menu_copy_HTML_as_formatted_text_to_clipboard)
        self.root.bind('<Control-m>', self.menu_copy_markdown_as_HTML_formatted_text_to_clipboard)
        self.root.bind('<Control-n>', self.menu_new_file)
        self.root.bind('<Control-o>', self.menu_open_file)
        self.root.bind('<Control-k>', self.menu_open_selected_file)
        self.root.bind('<Control-s>', self.menu_file_save_file_as)
        
        # Hack_: To make shift pressed detection work, we will have a method to detect when shifted is pressed and set a variable for that
        # self.root.entry.bind('<KeyPress>', self.on_entry_keyrelease)
        self.root.entry.setup_on_keypress(self.on_entry_keyrelease)
        
        self.root.entry.bind('<KeyRelease>', self.on_shift_keyrelease)
        # self.root.entry.bind('<Return>', 'event generate %W <Tab>')
        # self.root.entry.bind('<Return>', lambda x:self.root.event_generate('<Tab>'))
        self.root.entry.bind('<Down>', lambda x:self.root.event_generate('<Tab>'))
        self.root.entry.bind("<Alt-BackSpace>", self.on_entry_alt_backspace)
        self.root.listbox.bind("<Alt-BackSpace>", self.on_entry_alt_backspace)
        # self.root.listbox.bind("<Shift-Return>", self.on_entry_shift_enter)
        # When the keyboard key is in downward position
        self.root.listbox.bind('<KeyPress>', self.on_listbox_keypress)
        self.root.listbox.bind('<KeyRelease>', self.on_listbox_keyrelease)
        # When the keyboard key is in upward position
        # self.root.listbox.bind('<KeyRelease>', self.on_listbox_keyrelease)
        self.root.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        # self.listbox.bind('<<ListboxFocused>>', self.on_listbox_focus)
        # self.listbox.bind('<Double-1>', self.on_listbox_doubleclick)

        # self.root.code_block.bind("<MouseWheel>", self.on_mousewheel_code_block)
        # Enter is the mouseover mouse over
        # self.root.code_block.bind("<Enter>", self.on_mousewheel_code_block)
        # A list, with FilePath classes, from FileList.py
        
        # Search inside files panel
        self.show_search_in_files_panel = False
        
        # When previewing files, i dont load the full file. But only the first x lines. 
        self.has_loaded_full_file = False
        self.file_preview_quality = FilePreviewQualityEnum.NOTDEFINED

        self.filePathList = []
        
        # A filtered list, with FilePath classes, from FileList.py
        self.filteredFilePathList = []
        
        # A search inside files list, with FilePath classes, from FileList.py. This runs after the filteredFilePathList
        self.searchInsideFilesList = []
        
        # A list of strings, that will be showed in the ui "listbox"
        self.outputList = []
        
        # Content of the selected file
        self.file_fullpath =""
        self.file_content =""
        self.file_content_length = 0
        self.line_count = 0
        
        # We need to load the filelist asynchronous
        # self.loop = asyncio.get_event_loop()
        # task = asyncio.ensure_future(self.initialize_listbox())
        # self.loop.run_until_complete(task)
        
        # In order to have the window rendered already
        # Update will force the window to show, we need this.before we run the after method below.
        self.root.update()
        # Execute code on the main thread
        
        self.root.after(0, self.initialize_listbox())
        # self.root.listbox.focus_set()
        end_index = self.root.listbox.index("end")
        if end_index > 0:
            self.root.listbox.select_set(0,0)
            self.on_listbox_select(0)
        
        self.check_that_xclip_is_installed_on_linux()
        
        self.root.entry.focus_set()
   
    # Entry Events Methods ----------------------------------------------------------------

    def on_entry_keyrelease_debounce(self, event):
        pass

    def on_entry_keyrelease(self, event):
        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()
        print(event.keysym)
        end_index = self.root.listbox.index("end")
        if end_index > 0 and event.keysym == 'Down':
                pass
                
        self.on_shared_keyrelease(event)
        self.filter_list(self.filePathList)
        if end_index > 0:
            if self.show_search_in_files_panel:
                self.on_search_inside_files(False)
            _filePath = self.filteredFilePathList[0]
            fullpath = _filePath.fullpath
            self.update_right_preview_panel(fullpath, FilePreviewQualityEnum.SUPERFAST)
            
            self.set_statusbar(fullpath)
        else:
            self.set_code_view_content("")
            self.file_fullpath = ""
            self.set_statusbar("No Match")
            self.Ui.code_panel.hide()
            
            
    def reset_entry(self, event):
        self.root.entry.delete(0, 'end')
        self.root.entry.focus_set()
        
    def on_entry_alt_backspace(self, event):
        self.reset_entry(0)
        
    def on_entry_shift_enter(self, event):
        self.reset_entry(0)

    # Search Inside Files Methods ----------------------------------------------------------------

    def on_search_inside_files(self, update_codeview = True):

        search_inside_text = self.Ui.SearchInsideFiles.search_entry.get()
        contentList = []
        self.outputList = []
        self.searchInsideFilesList = []
        
        
        if search_inside_text == "":
            messagebox.showinfo("Search inside files", "Search Inside Files: No text to search for.")
            self.Ui.SearchInsideFiles.search_entry.focus()
            
        if search_inside_text != "":
            for _filepath in self.filteredFilePathList.copy():
                if self.does_filecontent_contains_string(_filepath.fullpath, search_inside_text):
                    contentList.append(_filepath)
            
            self.searchInsideFilesList = contentList
            for _filepath in self.searchInsideFilesList:
                self.outputList.append(" " + _filepath.nicename)
            
            self.filteredFilePathList = self.searchInsideFilesList 
            
            
            self.reset_listbox()
            
            for line in self.outputList:
                self.root.listbox.insert("end", line)
            
            if len(self.outputList) > 0:
                if self.show_search_in_files_panel and update_codeview:
                    _filePath = self.searchInsideFilesList[0]
                    fullpath = _filePath.fullpath
                    self.update_right_preview_panel(fullpath)
                    
                    self.set_statusbar(fullpath)
            else:
                self.set_code_view_content("")
                self.file_fullpath = ""
                self.set_statusbar("No Match")
                self.Ui.code_panel.hide()

    def does_filecontent_contains_string(self, file_path, search_string):
        if os.name == 'nt':
            file_path = file_path.replace("/", "\\")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, start=1):
                    if search_string.lower() in line.lower():
                        return True
            return False
        except:
            return False
        return False
    # Listbox Events Methods ----------------------------------------------------------------
   
    def on_listbox_select(self, event):
        # display element selected on list
        # print('(event) previous:', event.widget.get('active'))
        # print('(event)  current:', event.widget.get(event.widget.curselection()))
        # print('---')

        selected_index = self.root.listbox.curselection()
        if selected_index:
            # An item is selected.
            selected_index = self.root.listbox.curselection()[0]
            _filePath = self.filteredFilePathList[selected_index]
            fullpath = _filePath.fullpath
            self.file_fullpath = _filePath.fullpath
            
            # txt = self.read_file_as_string(fullpath)
            # self.set_code_view_content(txt)
            self.update_right_preview_panel(fullpath, FilePreviewQualityEnum.SUPERFAST)
            
            self.set_statusbar(fullpath)
            
            
    def on_listbox_keypress(self, event):
        print(event.keysym)
        
        if event.keysym == '1' and event.state == 4:  # Check for Ctrl key (state=4)
            self.menu_copy_fullpath_to_clipboard(event)
            
        if self.ctrl_pressed or self.alt_pressed:
            return None
        
        if event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift_pressed = True
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl_pressed = True
            return None
        if event.keysym == "Alt_L":
            self.alt_pressed = True
            return None
        

        
        try:
            char = event.keysym
            # check if char is an uppercase letter
            if ord(char) >= 65 and ord(char) <= 90:
                self.focus_entry_and_insert_char_at_end(char)
                print(char, "is an uppercase letter")

            # check if char is a lowercase letter
            if ord(char) >= 97 and ord(char) <= 122:
                self.focus_entry_and_insert_char_at_end(char)
                print(char, "is a lowercase letter")

            # check if char is a digit
            if ord(char) >= 48 and ord(char) <= 57:
                print(char, "is a digit")
        except:
          pass        
        
        # get text from entry
        try:
            print(event.keysym)
            print(event.widget.curselection()[0])
            if event.keysym == 'Up' and event.widget.curselection()[0] == 0 or event.keysym == 'BackSpace':
                self.root.entry.focus_set()
                self.root.listbox.selection_clear(0, tk.END),
                self.root.listbox.select_set(0,0)
        except:
            print('An exception occurred - 1651')
            # self.root.entry.focus_set()
        
        self.on_shared_keyrelease(event)
        
    def on_shift_keyrelease(self, event):
        if event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift_pressed = False
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl_pressed = False
        if event.keysym == "Alt_L":
            self.alt_pressed = False
        print('Listbox - KEYUP')
        
    def on_listbox_keyrelease(self, event):
        if event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift_pressed = False
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl_pressed = False
            return None
        if event.keysym == "Alt_L":
            self.alt_pressed = False
            return None
    
    def focus_entry_and_insert_char_at_end(self, char):
        # get the length of the current text
        text_len = len(self.root.entry.get())

        # set focus to the Entry widget
        self.root.entry.focus_set()

        # insert the character 'A' at the end of the text
        self.root.entry.insert(text_len, char)

    # ListBox Reload ------------------------------------------------------------------
    def listbox_reload(self):
        self.filePathList = []
        
        # A filtered list, with FilePath classes, from FileList.py
        self.filteredFilePathList = []
        
        # A list of strings, that will be showed in the ui "listbox"
        self.outputList = []
        
        # Content of the selected file
        self.file_fullpath =""
        self.file_content =""
        self.file_content_length = 0
        
        self.initialize_listbox()

    # Code View  ----------------------------------------------------------------
    def set_code_view_content(self, txt, file_ext="", quality = FilePreviewQualityEnum.NOTDEFINED):
        self.Ui.code_panel.set_code_to(txt, file_ext, quality)

        # Scroll to the top of the widget
        self.Ui.code_panel.scroll_to_top()
 
    # In preview mode, we do the following optimization:
    # To avoid loading huge files, and waiting, we only load the first 10000 bytes of the text file
    def set_code_view_content_preview(self, fullpath, quality=FilePreviewQualityEnum.NOTDEFINED):
        self.file_fullpath = fullpath
        if quality != FilePreviewQualityEnum.FULLQUALITY:
            self.has_loaded_full_file = False
        txt = ""
        line_ending = ""
        detected_bom = ""
        file_size_bytes = 0
        
        
        filesize = self.get_file_size(fullpath)
        if filesize != None:
          file_size_bytes = filesize

        try:
            with open(fullpath, 'rb') as file:
                # Read the first 10,000 bytes of the file
                
                data = None
                if quality == FilePreviewQualityEnum.SUPERFAST:
                    data = file.read(10000)
                    self.file_preview_quality = FilePreviewQualityEnum.SUPERFAST
                
                if quality == FilePreviewQualityEnum.MEDIUMQUALITY:
                    data = file.read(70000)
                    self.file_preview_quality = FilePreviewQualityEnum.MEDIUMQUALITY
                
                if quality == FilePreviewQualityEnum.FULLQUALITY:
                    data = file.read()
                    self.file_preview_quality = FilePreviewQualityEnum.FULLQUALITY
                
                if quality == FilePreviewQualityEnum.DISABLECOLOR:
                    data = file.read()
                    self.file_preview_quality = FilePreviewQualityEnum.DISABLECOLOR


                if filesize != None and len(data) < filesize:
                    print("File has not been fully read.")
                    self.has_loaded_full_file = False
                            
                # Check if the file has been fully loaded
                if filesize != None and len(data) == filesize:
                    print("Everything has been loaded.")
                    self.has_loaded_full_file = True

                # Try to decode the data using multiple encodings
                encodings_to_try = ['UTF-8', 'utf-32', 'utf-16', 'latin-1', 'ascii']
                for encoding in encodings_to_try:
                    try:
                        txt = data.decode(encoding)
                        # txt = txt.encode(detected_bom).decode('utf-8')
                        detected_bom = encoding
                        break
                    except UnicodeDecodeError:
                        pass
                
                # If I'm trying to open binary files, like zip and pdf, they allways fallback to latin-1, when i try to open them. So I use this catch all binary files, that is not utf32 
                if detected_bom == 'latin-1':
                    raise Exception("It looks like you are trying to open a binary file")
                # Check for BOM
                bom_patterns = {
                    b'\xef\xbb\xbf': 'UTF-8',
                    b'\xfe\xff': 'UTF-16 (BE)',
                    b'\xff\xfe\x00\x00': 'UTF-32 (LE)',
                    b'\x00\x00\xfe\xff': 'UTF-32 (BE)',
                    b'\xff\xfe': 'UTF-16 (LE)',
                }
                for bom, encoding in bom_patterns.items():
                    if data.startswith(bom):
                        detected_bom = encoding
                        break

        except Exception as e:
            self.set_code_view_content("Can't read file.")
            self.Ui.Statusbar.linecount_value.set('')
            self.Ui.Statusbar.encoding_value.set('')
            self.Ui.Statusbar.bom_value.set('')
            return

        # Convert the text to readable UTF-8 using the detected encoding or fallback to UTF-8
        # try:
        #     txt = txt.encode(detected_bom).decode('utf-8')
        # except (UnicodeEncodeError, UnicodeDecodeError):
        #     # If the conversion fails, it is likely already in UTF-8, or there is an issue with the text
        #     pass

        # Filesize in Statusbar
        self.Ui.Statusbar.set_filesize_value(file_size_bytes)
        
        if txt != "":
            # Detect Line Endings
            line_ending = self.detect_line_endings(txt)
        self.Ui.Statusbar.encoding_value.set(line_ending)
        
        
        # Detect BOM
        # bom = self.detect_byte_order_mark(txt)
        self.Ui.Statusbar.bom_value.set(detected_bom)
        
        # Statusbar Linecount
        char_count = len(txt)
        totalbytes = char_count*8
        plussign = ''
        line_count = txt.replace('\r\n', '\n').replace('\r', '\n').count('\n') + 1
        self.line_count = line_count
        if self.has_loaded_full_file == False and int(line_count) > 100 and totalbytes > 9991:
          plussign = '+'
        self.Ui.Statusbar.linecount_value.set(str(line_count) + plussign + ' Lines')
        
        # UTF-16 (BE) - Big Indian
        # https://en.wikipedia.org/wiki/Byte_order_mark 
        # Remove BOM (Byte Order Mark) character in beginning of file - Its only some files that has it.
        bom_regex = re.compile(r'^\ufeff', re.UNICODE)
        txt_without_bom = bom_regex.sub('', txt)
        txt = txt_without_bom
        
        self.file_content_length = len(txt)
        file_ext = self.get_file_extension(fullpath)
        if file_size_bytes != None and file_size_bytes >= 100000:
            self.set_code_view_content(txt, file_ext, FilePreviewQualityEnum.DISABLECOLOR)       
        else:
            self.set_code_view_content(txt, file_ext, quality)       

    def get_file_size(self, file_path):
        size_bytes = None
        try:
            return os.path.getsize(file_path)    
        except FileNotFoundError:
            return None
        return size_bytes
    
    # y0: Is where the scrollbar is, at the beginning of the Text editor. Example: '0.2165'
    # y1: Is where the scrollbar is, at the end of the Text editor. Example: '0.3167'
    def handle_scroll_code_view(self, y0, y1):
        print(y0, y1)
        self.Ui.code_panel.scrollbar_y.set(y0, y1)
        print('has loaded full file:', self.has_loaded_full_file)
        if float(y1) > 0.80 and self.file_preview_quality == FilePreviewQualityEnum.SUPERFAST:
            old_line_count = self.line_count
            old_y0 = y0
            self.set_code_view_content_preview(self.file_fullpath, FilePreviewQualityEnum.FULLQUALITY)
            if old_line_count > 149:
                scroll_to_y = str((old_line_count* float(old_y0) ) / self.line_count)
                self.Ui.code_panel.text.yview_moveto(scroll_to_y)
                self.Ui.code_panel.text_linenum.yview_moveto(scroll_to_y)
               
        self.Ui.code_panel.text_linenum.yview_moveto(y0)

    # Other UI Methods ----------------------------------------------------------------

    def on_shared_keyrelease(self, event):

        # Enter only
        if event.keysym == 'Return' and self.shift_pressed == False:
        #     self.on_listbox_doubleclick(event)
            self.menu_copy_text_to_clipboard("ignorethistexttotheparem")
            # Hide the window
            self.root.withdraw()

            # Show the window again
            # root.deiconify()        
            
            # It will popup a text in the top of the screen "Copied to Clipboard"
            UiPopupToastCopied().start_animation()

            time.sleep(0.5)
            self.exit_app()        
        
        # Shift+Enter
        if event.keysym == 'Shift_L':
            self.shift_pressed = True
        elif event.keysym == 'Return' and self.shift_pressed:
            self.menu_copy_and_paste_into_background_program("ignorethistexttotheparem")
        elif event.keysym == 'Return' and self.ctrl_pressed:
            self.menu_copy_file_like_filemanager("ignorethistexttotheparem")
            
        else:
            self.shift_pressed = False

        # Escape
        if event.keysym == 'Escape':
            self.exit_app()
        
    def is_image_file(self, image_fullpath):
        # Extract the file extension
        _, file_ext = os.path.splitext(image_fullpath)
        
        # Remove the dot from the extension
        file_ext = file_ext[1:].lower()
        
        # Check if the extension matches jpg, gif, or png using regular expressions
        if re.match(r"^(jpg|jpeg|gif|png|ico|tga|bmp|tiff|webp)$", file_ext):
            return True
        
        return False
    
    def is_markdown_file(self, image_fullpath):
        # Extract the file extension
        _, file_ext = os.path.splitext(image_fullpath)
        
        # Remove the dot from the extension
        file_ext = file_ext[1:].lower()
        
        # Check if the extension matches jpg, gif, or png using regular expressions
        if re.match(r"^(md)$", file_ext):
            return True
        
        return False
    
    
    def update_right_preview_panel(self, fullpath, quality=FilePreviewQualityEnum.NOTDEFINED):
        if self.is_image_file(fullpath):
            # Its an image, show the image element
            self.Ui.Statusbar.linecount_value.set('')
            self.Ui.Statusbar.encoding_value.set('')
            self.Ui.Statusbar.bom_value.set('')
            self.set_image(fullpath)
            self.Ui.code_panel.hide()
            
        else:
            # Its code, then show text
            self.root.image_frame.hide()
            
            self.set_code_view_content_preview(fullpath, quality)
    
    
    def set_image(self, full_image_path: str):
        if os.path.exists(full_image_path):
            filesize = self.get_file_size(full_image_path)
            if filesize != None:
                file_size_bytes = filesize
                self.Ui.Statusbar.set_filesize_value(file_size_bytes)
            self.root.image_frame.display_image(full_image_path)
        else:
            print(f"File '{full_image_path}' does not exist.")
    
    def set_statusbar(self, text):
        if os.name == "nt":  # Windows
            text = text.replace("/", "\\")
        self.Ui.Statusbar.set_value(text)
    # Methods ----------------------------------------------------------------
    
    def initialize_listbox(self):
        # self.root.unbind('<Visibility>')
        
        # list = getFileList("/home/m/Settings/FileGen/Templates")
        list = FileController().load_file_list()
        # list = getFileList("/usr")
        # A list, with FilePath classes, from FileList.py
        self.filePathList = list
        
        self.filter_list(list)
        
        
    
    def filter_list(self, list):
        value = self.root.entry.get()
        if value == "" :
           self.filteredFilePathList = self.filePathList
        if value != "" :
            sortable_objects = list
            search_string = value.lower()
            # filtered_objects = [obj for obj in sortable_objects if self.search_algo(search_string, obj.nicename.lower())]
            filtered_objects = []
            for obj in sortable_objects:
                obj_path_string = obj.nicename.lower()
                score = search_algo(search_string, obj_path_string)
                obj.score = score
                if obj.score > 0:
                    filtered_objects.append(obj)

            # Sort the list based on the 'age' property in descending order
            sorted_list = sorted(filtered_objects, key=lambda x: x.score, reverse=True)
            filtered_objects = sorted_list
            
            self.filteredFilePathList = []
            for obj in filtered_objects:
                self.filteredFilePathList.append(obj)
        
        self.outputList = []
        for _filepath in self.filteredFilePathList:
            self.outputList.append(" " + _filepath.nicename)
            # Display score in listbox
            # self.outputList.append(str(_filepath.score) + "  |  " +_filepath.nicename)

        self.reset_listbox()
        
        for line in self.outputList:
            self.root.listbox.insert("end", line)

    def reset_listbox(self):
        self.root.listbox.delete(0, "end")

    def read_file_as_string(self, filepath):
        try:
            with open(filepath, "rb") as file:
                binary_content = file.read()
                try:
                    content = binary_content.decode("utf-8")
                    self.file_content = content
                    
                    # UTF-16 (BE) - Big Indian
                    # https://en.wikipedia.org/wiki/Byte_order_mark
                    # Remove BOM (Byte Order Mark) character in beginning of file - Its only some files that has it.
                    bom_regex = re.compile(r'^\ufeff', re.UNICODE)
                    txt_without_bom = bom_regex.sub('', self.file_content)
                    self.file_content = txt_without_bom
                    
                    return content
                except UnicodeDecodeError:
                    return f"Error: File '{filepath}' is not a text file."
        except FileNotFoundError:
            return f"Error: File '{filepath}' not found."
        except Exception as e:
            return f"Error: {str(e)}"

        return ""
        self.file_content =""
    
    def detect_line_endings(self, text = ""):
        # Count the occurrences of different line endings
        newline_count = text.count('\n')
        crlf_count = text.count('\r\n')
        cr_count = text.count('\r')

        # Determine the type of line ending based on the counts
        if crlf_count > 0:
            return "Windows (CRLF)"
        elif cr_count > 0:
            return "macOS (CR)"
        elif newline_count > 0:
            # return "Unix/Linux (LF)"
            return "Linux (LF)"
        else:
            # return "Unknown line ending"
            return ""
        
    def detect_byte_order_mark(self, text):
        if not text:
            return 'Unknown'

        # Convert the text to bytes using various encodings
        text_bytes = text.encode('utf-8')
        bom_patterns = {
            b'\xef\xbb\xbf': 'UTF-8',
            b'\xff\xfe': 'UTF-16 (LE)',
            b'\xfe\xff': 'UTF-16 (BE)',
            b'\xff\xfe\x00\x00': 'UTF-32 (LE)',
            b'\x00\x00\xfe\xff': 'UTF-32 (BE)'
        }

        for bom, encoding in bom_patterns.items():
            if text_bytes.startswith(bom):
                # Remove the BOM from the text bytes
                text_bytes = text_bytes[len(bom):]
                try:
                    text_bytes.decode(encoding)
                    return encoding
                except UnicodeDecodeError:
                    return 'Unknown'

        # If no BOM is found, assume UTF-8 by default
        try:
            text_bytes.decode('utf-8')
            return 'UTF-8'
        except UnicodeDecodeError:
            return 'Unknown'
    
    def check_that_xclip_is_installed_on_linux(self):

        # If Xclip is not installed on linux, then show a message to user how to install
        if os.name == 'posix' and not self.is_xclip_installed():
            messagebox.showinfo("Required Program", 'A program called XClip is required. XClip is used to copy text to the clipboard.\n\nOpen terminal and write the following:\n\nsudo apt-get install xclip\n\nThen press Enter')
           
    def is_xclip_installed(self):
        try:
            subprocess.run(["xclip", "-version"])
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError:
            return False
    # MENU > FILE ------------------------------------------------------
            
    def menu_new_file(self, ignore_this_param = ""):
        if os.name == 'nt':
            try:
                subprocess.run(["notepad.exe"])
            except FileNotFoundError:
                print("Notepad was not found. Please check if it's installed or adjust the path accordingly.")
        else:
            newFileDialog = TextEditorApp()
            newFileDialog.run()

    def menu_file_save_file_as(self, ignore_this_param = ""):
        
        source_fullpath = self.file_fullpath
        if source_fullpath == "":
            messagebox.showinfo("No File Selected", "No File Is Selected")
            return 
        
        # Get seleted Filename
        source_filename = os.path.basename(source_fullpath)
        
        # Ask user to save filename
        
        default_name = source_filename
        destination_fullpath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("All Files", "*.*")],
                                                initialfile=default_name,
                                                title="Save File As..")
        if destination_fullpath:
            try:
                shutil.copyfile(source_fullpath, destination_fullpath)
                messagebox.showinfo("Succes - File Copied", f"File Copied Succesfully: '{destination_fullpath}'")
            except FileNotFoundError:
                messagebox.showinfo("Error","Error: Source file not found.")
            except PermissionError:
                messagebox.showinfo("Error", "Error: Permission denied. Make sure you have appropriate permissions.")
            except Exception as e:
                messagebox.showinfo("Error", f"An error occurred")

        # Promt user for Succes / Failure
        
    def menu_open_file(self, ignore_this_param = ""):
        # Prompt the user to select a file using a file dialog
        file_path = filedialog.askopenfilename()

        # Check if a file was selected
        if file_path:
            # Check if the file is not a binary file
            try:
                with open(file_path, 'rb') as file:
                    try:
                        file_contents = file.read().decode('utf-8')
                        newFileDialog = TextEditorApp()
                        newFileDialog.set_text(file_contents)
                        newFileDialog.run()
                        # messagebox.showinfo("File Contents", file_contents)
                    except UnicodeDecodeError:
                        messagebox.showerror("Error", "Selected file is a binary file.")
            except IOError:
                messagebox.showerror("Error", "Error opening the file.")
        else:
            messagebox.showinfo("Info", "No file selected.")
            

    def menu_open_selected_file(self, ignore_this_param = ""):
        # Prompt the user to select a file using a file dialog
        file_path = self.file_fullpath

        # Check if a file was selected
        if file_path:
            # Check if the file is not a binary file
            try:
                with open(file_path, 'rb') as file:
                    try:
                        file_contents = file.read().decode('utf-8')
                        newFileDialog = TextEditorApp()
                        newFileDialog.set_text(file_contents)
                        newFileDialog.run()
                        # messagebox.showinfo("File Contents", file_contents)
                    except UnicodeDecodeError:
                        messagebox.showerror("Error", "Selected file is a binary file.")
            except IOError:
                messagebox.showerror("Error", "Error opening the file.")
        else:
            messagebox.showinfo("Info", "No file selected.")

    def menu_open_selected_file_in_filemanager(self, ignore_this_param = ""):
        file_path = self.file_fullpath
        # Get the directory path
        dir = os.path.dirname(file_path)
        # Check if a file was selected
        if os.path.exists(dir) and os.path.isdir(dir):
            if os.name == "posix":  # Linux, macOS
                os.system(f"xdg-open '{dir}'")
            elif os.name == "nt":  # Windows
                file_path_backslash = file_path.replace("/", "\\")
                subprocess.Popen(f'explorer /select,"{file_path_backslash}"')
        else:
            messagebox.showinfo("Info", "No file selected.")

    def menu_open_selected_file_in_vscode(self, ignore_this_param = ""):
        file_path = self.file_fullpath
        # Get the directory path
        dir = os.path.dirname(file_path)
        # Check if a file was selected
        if os.path.exists(dir) and os.path.isdir(dir):
            if os.name == "posix":  # Linux, macOS
                try:
                    # It will open the DIRECTORY where the file is, in vscode. AFTER that, it will open the FILE in vscode. Then the explorer panel has opened the correct folder.
                    subprocess.run(['code', dir, file_path])
                except FileNotFoundError:
                    print("VSCode not found. Please ensure Visual Studio Code is installed and accessible in the system's PATH.")
            elif os.name == "nt":  # Windows
                file_path_backslash = file_path.replace("/", "\\")
                try:
                    # Get the user-specific path to the "code" executable
                    vscode_executable = os.path.expanduser(r"~\AppData\Local\Programs\Microsoft VS Code\Code.exe")

                    # It will open the DIRECTORY where the file is, in vscode. AFTER that, it will open the FILE in vscode. Then the explorer panel has opened the correct folder.
                    subprocess.run([vscode_executable, dir, file_path_backslash])
                except FileNotFoundError:
                    messagebox.showinfo("VSCode not found: c:\\Users\\Username\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        else:
            messagebox.showinfo("Info", "No file selected.")
    # MENU > COPY ------------------------------------------------------

    def menu_copy_text_to_clipboard(self, ignore_this_param = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return
        
        # If it is Text
        if not self.is_image_file(self.file_fullpath):
            content = self.read_file_as_string(self.file_fullpath)
            # pyperclip.copy(self.file_content)
            pyperclip.copy(content)
            self.set_statusbar("The File Content is copied to the clipboard")
            # It will popup a text in the top of the screen "Copied to Clipboard"
            # UiPopupToastCopied().start_animation()

        # If it is an Image
        else:
            if os.name == "posix":  # Linux, macOS
                CopyImageLinuxController().copy_image_to_clipboard_on_linux(self.file_fullpath)
                self.set_statusbar("The Image is copied to the clipboard")
                
            elif os.name == "nt":  # Windows
                file_path_backslash = self.file_fullpath.replace("/", "\\")            
                CopyImageWindowsController().copy_image_to_clipboard_on_windows(file_path_backslash)
                self.set_statusbar("The Image is copied to the clipboard")
      
    def menu_copy_and_paste_into_background_program(self, ignore = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return
    
        self.menu_copy_text_to_clipboard("ignorethistexttotheparam")
        # Hide the window
        self.root.withdraw()

        time.sleep(0.7)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.6)

        # Show the window again
        self.root.deiconify()        
        self.shift_pressed = False


    def menu_copy_HTML_as_formatted_text_to_clipboard(self, ignore_this_param = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return
        
        if os.name == "posix":  # Linux, macOS
            if not self.is_image_file(self.file_fullpath):
                copy_html_to_clipboard_linux(self.file_fullpath)
                self.set_statusbar("HTML formatted text copied to the clipboard")
            
        if os.name == "nt":  # Windows
            if not self.is_image_file(self.file_fullpath):
                try:
                    content = self.read_file_as_string(self.file_fullpath)
                    PutHtml(content)
                    self.set_statusbar("HTML formatted text copied to the clipboard")
                except Exception:
                    messagebox.showinfo("Info", "Failed: Can not copy the file content, to the clipboard as formatted HTML. Make sure you copy a *.html file.")


    def menu_copy_markdown_as_HTML_formatted_text_to_clipboard(self, ignore_this_param = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return
        if not self.is_markdown_file(self.file_fullpath):
            messagebox.showinfo("Info", "This feature only works with markdown files. Markdown is a fileformat used for simple text formatting. A markdowns filename allways ends with '.md' example: MyFile.md")
            return
        if os.name == "posix":  # Linux, macOS
            copy_markdown_as_HTML_clipboard_linux(self.file_fullpath)
            self.set_statusbar("Markdown text copied to the clipboard as formatted text (HTML)")
            
        if os.name == "nt":  # Windows
            try:
                content = self.read_file_as_string(self.file_fullpath)
                html = markdown.markdown(markdown_content, extensions=['tables', 'sane_lists'])
                PutHtml(html)
                self.set_statusbar("Markdown text copied to the clipboard as formatted text (HTML)")
            except Exception:
                messagebox.showinfo("Info", "Failed: Can not copy the file content, to the clipboard as formatted HTML. Make sure you copy a *.html file.")
          
            
    def menu_copy_fullpath_to_clipboard(self, ignore_this_param = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return
        
        
        if os.name == "posix":  # Linux, macOS
            pyperclip.copy(self.file_fullpath)
            self.set_statusbar("The Fullpath is copied to the clipboard")
            
        elif os.name == "nt":  # Windows
            fp = self.file_fullpath
            path = fp.replace("/", '\\')
            pyperclip.copy(path)
            self.set_statusbar("The Fullpath is copied to the clipboard")

    def menu_copy_filename_to_clipboard(self, ignore_this_param = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return
        
        
        if os.name == "posix":  # Linux, macOS
            filename = os.path.basename(self.file_fullpath)
            pyperclip.copy(filename)
            self.set_statusbar("The Filename is copied to the clipboard")
            
        elif os.name == "nt":  # Windows
            fp = self.file_fullpath
            path = fp.replace("/", '\\')
            filename = os.path.basename(path)
            pyperclip.copy(filename)
            self.set_statusbar("The Filename is copied to the clipboard")

    def menu_copy_folderpath_to_clipboard(self, ignore_this_param = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return
        
        if os.name == "posix":  # Linux, macOS
            dirpath = os.path.dirname(self.file_fullpath)
            pyperclip.copy(dirpath)
            self.set_statusbar("The Filename is copied to the clipboard")
            
        elif os.name == "nt":  # Windows
            fp = self.file_fullpath
            path = fp.replace("/", '\\')
            dirpath = os.path.dirname(path)
            pyperclip.copy(dirpath)
            self.set_statusbar("The Filename is copied to the clipboard")

    def menu_copy_file_like_filemanager(self, ignore = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return

        if os.name == "posix":  # Linux, macOS
            copy_file_linux_x11_gnome(self.file_fullpath)
            self.set_statusbar("The File is copied to the clipboard. In the Ubuntu program called 'Files' or Nautilus you can paste the file")
            
        elif os.name == "nt":  # Windows
            fp = self.file_fullpath
            path = fp.replace("/", '\\')
            copy_files_windows([path])
            self.set_statusbar("The File is copied to the clipboard")

    # Copy the file on Linux, under X11. The file can be pasted in Gmail, Dolphin and other programs.
    def menu_copy_file_linux_x11_other_programs(self, ignore = ""):
        if self.file_fullpath == '':
            messagebox.showinfo("Info", "No file selected. Go to Settings > Directory Settings. Add some Directorys")
            return

        if os.name == "posix":  # Linux, macOS
            copy_file_linux_x11_other_programs(self.file_fullpath)
            self.set_statusbar("The File is copied to the clipboard. You can paste the file in Gmail, Browsers, Dolphin and many other programs")
            
    # MENU > VIEW ------------------------------------------------------

    def menu_view_linenumbers(self):
        show_linenumber = self.AppSetting.menu_show_linenumber.get()
        self.Ui.code_panel.toggle_linenumbers_visibility(show_linenumber)
        
        self.AppSetting.save_settings()

    def menu_view_searchinsidefiles(self):
        show_searchinsidefiles = self.AppSetting.menu_show_searchinsidefiles.get()
        self.Ui.SearchInsideFiles.toggle_visibility(show_searchinsidefiles)
        
        self.AppSetting.save_settings()

    def menu_view_statusbar(self):
        show_statusbar = self.AppSetting.menu_show_statusbar.get()
        self.Ui.Statusbar.toggle_visibility(show_statusbar)
        self.AppSetting.save_settings()

    def menu_settings_exclude_files(self, ignore_this_param = ""):
        dialog = FilenameExcludeDialog(self)
        # dialog.set_predefined_list(["file1.txt",
        #                            "file2.txt", "file3.txt"])  # Set the predefined list
        dialog.run()
 
    # MENU > SETTINGS ------------------------------------------------------
    
    def menu_settings_open_filemanager(self, ignore_this_param = ""):
        config_path = FileController().open_directory_config_in_filemanager()
    
    def menu_settings_reload_directorys(self, ignore_this_param = ""):
        self.listbox_reload()
        
    def menu_settings_directory_settings(self, event):
        DirectorySettings(self)
    
    def get_file_extension(self, file_path):
        _, file_ext = os.path.splitext(file_path)
        return file_ext[1:] if file_ext else ''    
    
    # MENU > SETTINGS ------------------------------------------------------
 
    def menu_help_documentation(self, event):
        title = "Documentation"
        description_text = "See documentation here (You need a Github account):\n\nhttps://www.github.com"
        link_url = "https://www.github.com"
        link_window = UiBrowserLinkWindow(title, description_text, link_url).run()
 
    def menu_help_keyboard_shortcuts(self, event):
        title = "Keyboard Shortcuts"
        description_text = "See all Keyboard shortcuts here (You need a Github account):\n\nhttps://www.github.com"
        link_url = "https://www.github.com"
        link_window = UiBrowserLinkWindow(title, description_text, link_url).run()
 
    def menu_help_report_a_problem(self, event):
        title = "Report a Problem"
        description_text = "You can report a problem here (You need a Github account):\n\nhttps://www.github.com"
        link_url = "https://www.github.com"
        link_window = UiBrowserLinkWindow(title, description_text, link_url).run()
 
    def menu_help_suggest_a_feature(self, event):
        title = "Suggest a Feature"
        description_text = "You can suggest a feature here (You need a Github account):\n\nhttps://www.github.com"
        link_url = "https://www.github.com"
        link_window = UiBrowserLinkWindow(title, description_text, link_url).run()
 
    def menu_help_give_feedback(self, event):
        title = "Give Feedback"
        description_text = "You can give feedback here (You need a Github account):\n\nhttps://www.github.com"
        link_url = "https://www.github.com"
        link_window = UiBrowserLinkWindow(title, description_text, link_url).run()
 
    def menu_help_version(self, event):
        title = "Version"
        description_text = "Version: " + self.app_version + "\n\nYou can check for the latest version here (You need a Github account):\n\nhttps://www.github.com"
        link_url = "https://www.github.com"
        link_window = UiBrowserLinkWindow(title, description_text, link_url).run()
 

   
    
    # APP WINDOW ------------------------------------------------------

    def exit_app(self, event=None):
        # self.destroy()
        # TODO: https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
        sys.exit(0)
        os._exit(0) 