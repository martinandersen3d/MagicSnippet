import os
import sys
import tkinter as tk
from tkinter import ttk
from ui_menubar import Menubar
from ui_panel_search_file import DebouncedEntry
from ui_panel_search_inside_files import SearchInsideFiles
from ui_statusbar import Statusbar
from ui_panel_codeviewer import TextDisplayFrame

from ui_panel_imageviewer import *
from ui_menu_item import MenuItem

class Ui():
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        # WINDOW ------------------------------
        
        # app = tk.Tk()
        # set window width and height
        mywidth = 1900
        myheight = 1060

        # get screen height and width
        scrwdth = int( root.winfo_screenwidth() )
        scrhgt = int(root.winfo_screenheight())

        maxwidth=2500
        maxheight=1600
        
        # optimize the Width and Height of the program, depending on screen size
        if scrwdth > maxwidth:
            mywidth = round(maxwidth *0.75)
        else:
            mywidth = round(scrwdth *0.75)
        myheight = round(scrhgt *0.85)         
        
        # write formula for center screen
        xLeft = int( (scrwdth/2) - (mywidth/2))
        yTop = int((scrhgt/2) - (myheight/2)-50)

        # set geometry 
        root.geometry(str(mywidth) + "x" + str(myheight) + "+" + str(xLeft) + "+" + str(yTop))
        root.title("Magic Snippets - Version " + self.controller.app_version)
        
        bg="white"
        # textcolor="#8ca0aa"
        # background-color: #282C33;
        # border-color: #2e343f;
        # text-color: #8ca0aa;
        
        # MENU BAR ------------------------------
        self.MenuBar = Menubar(self.root, self.controller)
        
        
        # self.configure(background=bg)
        self.folderTupleList = ()

        # LAYOUT ---------------------------------

        paned_window = tk.PanedWindow(root, orient="horizontal")
        paned_window.pack(fill="both", expand=True)

        # Left Side
        # left_frame = tk.Frame(paned_window, bg="red", width=500, height=200)
        left_frame = tk.Frame(paned_window, width=500, height=200)
        paned_window.add(left_frame)

        # Top left frame
        left_frame_100 = tk.Frame(left_frame, width=100, height=100)
        left_frame_100.pack(side="top", fill="x", pady=10, padx=10)

        # left-middle to left bottom frame
        left_frame_body = tk.Frame(left_frame, width=100, height=100)
        left_frame_body.pack( fill="both", expand=True, pady=10, padx=10)

        # Right Side
        right_frame = tk.Frame(paned_window, width=100, height=200)
        paned_window.add(right_frame)        # Top right frame
        # right_frame_100 = tk.Frame(right_frame, bg="green", width=100, height=100)
        # right_frame_100.pack(side="top", fill="x")        

        # right-middle to right bottom frame
        right_frame_body = tk.Frame(right_frame, width=100, height=100)
        right_frame_body.pack( fill="both", expand=True)
        
        # here I set the width of the left windows
        paned_window.paneconfigure(left_frame, minsize=300, width=950)
        paned_window.paneconfigure(right_frame, minsize=300)
        
        # TEXTFIELD ---------------------------------
        root.entry = DebouncedEntry(left_frame_100, borderwidth=8, relief=tk.FLAT, width=100)
        root.entry.configure()
        root.entry.pack()
        root.entry.focus()
        
        # SEARCH INSIDE FILES ---------------------------------

        self.SearchInsideFiles = SearchInsideFiles(left_frame_100, self.root, self.controller)
        show_searchinsidefiles = self.controller.AppSetting.menu_show_searchinsidefiles.get()
        self.SearchInsideFiles.toggle_visibility(show_searchinsidefiles)
        
        # LISTBOX --------------------------------
        root.listbox = tk.Listbox(left_frame_body)
        root.listbox.bind("<Button-3>", self.on_listbox_show_context_menu)
        root.listbox.pack(side="left", fill="both", expand=True)

        # Scrollbar widget and associate it with the Listbox
        # root.scrollbar = tk.Scrollbar(left_frame_body, orient="vertical", command=root.listbox.yview,  width=12, borderwidth=0, highlightthickness=0, troughcolor='#faf4f4', activebackground='#3daee9', bg='#8b8888', highlightcolor='blue')
        root.scrollbar = tk.Scrollbar(left_frame_body, orient="vertical", command=root.listbox.yview,  width=14, borderwidth=0, highlightthickness=0, troughcolor='#ededed', activebackground='#3daee9', bg='#c4c4c4', highlightcolor='blue')
        root.scrollbar.pack(side="right", fill="y")
        root.listbox.configure(yscrollcommand=root.scrollbar.set)

        # Add listbox elements
        root.listbox.insert('end', 'Loading...')

        # # Add some sample data to the Listbox
        # for i in range(100):
        #     root.listbox.insert("end", "Item {}".format(i))
        
                
        # CODE PANEL --------------------------------
        self.code_panel = TextDisplayFrame(right_frame_body, self.controller)
        show_linenumber = self.controller.AppSetting.menu_show_linenumber.get()
        self.code_panel.toggle_linenumbers_visibility(show_linenumber)
        
        # IMAGE PANEL --------------------------------
        root.image_frame = ImageDisplayFrame(right_frame_body)
        # root.image_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # STATUSBAR --------------------------------
        self.Statusbar = Statusbar(self.root, self.controller)
        show_statusbar = self.controller.AppSetting.menu_show_statusbar.get()
        self.Statusbar.toggle_visibility(show_statusbar)

    def on_listbox_show_context_menu(self, event):
        context_menu = tk.Menu(self.root.listbox, tearoff=0)
        context_menu.add_command(label="Copy Content", command=self.controller.menu_copy_text_to_clipboard)
        context_menu.add_command(label="Copy Content And Paste Into Background Program", command=self.controller.menu_copy_and_paste_into_background_program)
        context_menu.add_command(label="Copy File - Just like Windows Explorer", command=self.controller.menu_copy_file_like_filemanager)
        context_menu.add_command(label="Copy HTML as Formatted Text", command=self.controller.menu_copy_HTML_as_formatted_text_to_clipboard)
        context_menu.add_separator() 
        context_menu.add_command(label="Copy Fullpath", command=self.controller.menu_copy_fullpath_to_clipboard)
        context_menu.add_command(label="Copy Filename", command=self.controller.menu_copy_filename_to_clipboard)
        context_menu.add_command(label="Copy Folder Path", command=self.controller.menu_copy_folderpath_to_clipboard)
        context_menu.tk_popup(event.x_root, event.y_root)
