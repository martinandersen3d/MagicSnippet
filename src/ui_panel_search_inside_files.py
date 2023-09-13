import os
import tkinter as tk

class SearchInsideFiles:
    def __init__(self, parent_frame, root, controller):
        self.root = root
        self.controller = controller
        
        self.label_frame = tk.LabelFrame(parent_frame, text="Search Inside Files Content")
        # root.label_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)

        # Search Entry
        self.search_entry = tk.Entry(self.label_frame, borderwidth=8, relief=tk.FLAT)
        self.search_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search Button
        self.search_button = tk.Button(self.label_frame, text="     Search     ", command=self.controller.on_search_inside_files)
        self.search_button.pack(padx=10, pady=10, side=tk.LEFT)
        
        if self.controller.AppSetting.menu_show_searchinsidefiles.get() == 0:
            pass
        
    def show(self):
            self.label_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=16)
            self.controller.show_search_in_files_panel = True
        
    def hide(self):
            self.label_frame.pack_forget()
            self.controller.show_search_in_files_panel = False
        
    def toggle_visibility(self, int_value):
        if int_value == 0:
            self.hide()
        else:
            self.show()        
        
        
        

        # if self.root.label_frame.winfo_ismapped():
        #     self.root.label_frame.pack_forget()
        #     self.show_search_in_files_panel = False
        # else:
        #     self.root.label_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=10)
        #     self.show_search_in_files_panel = True