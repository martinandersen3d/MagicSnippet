import os
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from file_controller import *

        
class FilenameExcludeDialog:
    def __init__(self, controller):
        self.root = tk.Tk()
        self.root.title("Filename Exclude Dialog")
        self.root.geometry("600x900")
        self.root.resizable(True, True)
        self.root.configure(padx=8, pady=8)
        self.controller = controller

        self.filepaths = []

        # LIST OF PATHS
        self.label_frame_filepath = tk.LabelFrame(self.root, text="    List of Excluded Filepaths:    ", padx=12, pady=16)
        self.label_frame_filepath.pack(fill=tk.BOTH, expand=True)
        # Add margin to the top
        self.label_frame_filepath.pack(pady=(16, 0))        
        
        self.listbox_frame = tk.Frame(self.label_frame_filepath)
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.listbox_frame, height=15, selectmode=tk.MULTIPLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.remove_button = tk.Button(self.label_frame_filepath, text="    Remove    ", command=self.remove_selected)
        self.remove_button.pack(side=tk.LEFT, pady=8)

        # ADD PATHS 
        self.label_frame = tk.LabelFrame(self.root, text="    Add Filepaths - Write filepaths to Exlude:    ", padx=12, pady=16)
        self.label_frame.pack(fill=tk.BOTH, expand=True)
        # Add 50px margin to the top
        self.label_frame.pack(pady=(16, 0))
        
        self.textbox = ScrolledText(self.label_frame, height=20, width=40, wrap=tk.WORD)
        self.textbox.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.label_frame)
        self.button_frame.pack(fill=tk.X, pady=8)

        self.exclude_button = tk.Button(self.button_frame, text="    Exclude Paths    ", command=self.exclude_paths)
        self.exclude_button.pack(side=tk.LEFT, padx=(0, 8))

        self.textbox.bind("<Button-3>", self.show_popup_menu)

        self.load_list_from_file()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_popup_menu(self, event):
        popup_menu = tk.Menu(self.root, tearoff=0)
        popup_menu.add_command(label="Cut", accelerator="Ctrl+X")
        popup_menu.add_command(label="Copy", accelerator="Ctrl+C")
        popup_menu.add_command(label="Paste", accelerator="Ctrl+V")
        popup_menu.add_command(label="Delete", accelerator="Del")
        popup_menu.add_separator()
        popup_menu.add_command(label="Select All", accelerator="Ctrl+A")
        popup_menu.post(event.x_root, event.y_root)

    def exclude_paths(self):
        paths = self.textbox.get("1.0", tk.END).strip().replace('*', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace(',','\n').replace(' ', '\n').split("\n")
        # Remove duplicates
        my_list = list(set(paths))

        # Remove empty strings and spaces
        my_list = [item for item in my_list if item.strip()]
        self.filepaths.extend(my_list)
        
        # Retain the current selection
        selections = self.listbox.curselection()

        self.update_listbox()

        # Restore the selection
        for index in selections:
            self.listbox.select_set(index)
        self.save_listbox_to_file()
        self.root.lift()  # Push the window to the front

    def remove_selected(self):
        selections = self.listbox.curselection()
        for index in reversed(selections):
            self.listbox.delete(index)
        self.filepaths = self.listbox.get(0, tk.END)
        self.save_listbox_to_file()
        self.root.lift()  # Push the window to the front

    def update_listbox(self):
        self.filepaths.sort()
        self.listbox.delete(0, tk.END)
        for filepath in self.filepaths:
            self.listbox.insert(tk.END, filepath)

    def set_predefined_list(self, predefined_list):
        self.filepaths = predefined_list
        self.update_listbox()

    # On Dialog startin up
    def load_list_from_file(self):
        self.get_exlude_paths_list()
        self.update_listbox()

    # To get the list of exclude files
    def get_exlude_paths_list(self):
        filepaths = FileController().get_exlude_paths_list()
        self.filepaths = filepaths
        return filepaths


    def save_listbox_to_file(self):
        FileController().save_exludefiles_config(self.filepaths)
        

    def run(self):
        self.root.mainloop()


    # If it cant find a config file list it will save these defaults
    def set_default_exlude_list(self):
        self.filepaths = [
        # General
        '.cache',
        '.coverage',
        '.DS_Store',
        '.git',
        '.idea/',
        '.ipynb_checkpoints/',
        '.mypy_cache/',
        '.pytest_cache/',
        '.tox/',
        '.venv/',
        '.vs/',
        '.vscode/',
        
        # Windows
        'Thumbs.db',
        'desktop.ini',

        # Linux
        '/etc/',

        # C#
        'bin/',
        'obj/',
        '.dll',
        '.exe',

        # .NET
        'packages/',

        # TypeScript
        'node_modules/',
        '.js.map',
        '.d.ts',

        # Vue.js
        'dist/',
        'build/',
        '.css.map',

        # React.js

        # Angular

        # Python
        '__pycache__/',
        '.pyc',
        '.pyo',
        '.pyd',
        '.egg-info/',
        '.egg',
        '.egg-info',
        '.so',

        # Node.js
        ]
        self.filepaths.sort()
        self.save_listbox_to_file()

    def on_closing(self):
        try:
            self.controller.listbox_reload()
        except:
          pass
        self.root.destroy()
        
# dialog = FilenameExcludeDialog()
# # dialog.set_predefined_list(["file1.txt",
# #                            "file2.txt", "file3.txt"])  # Set the predefined list

# dialog.run()
