import os
import tkinter as tk

class Statusbar:
    def __init__(self, root, controller):
        self.root = root
        self.labels_frame = tk.Frame(self.root)
        
        self.text_value = tk.StringVar()
        self.linecount_value = tk.StringVar()
        self.filesize_value = tk.StringVar()
        self.encoding_value = tk.StringVar()
        self.bom_value = tk.StringVar()


        self.status_label = tk.Label(self.labels_frame, textvariable=self.text_value, bd=1, relief=tk.SUNKEN, anchor=tk.W, padx=10, pady=9)
        self.linecount_label = tk.Label(self.labels_frame, textvariable=self.linecount_value, bd=1, relief=tk.SUNKEN, anchor=tk.E, padx=10, pady=9, width=10)
        self.filesize_label = tk.Label(self.labels_frame, textvariable=self.filesize_value, bd=1, relief=tk.SUNKEN, anchor=tk.E, padx=10, pady=9, width=8)
        self.encoding_label = tk.Label(self.labels_frame, textvariable=self.encoding_value, bd=1, relief=tk.SUNKEN, anchor=tk.E, padx=10, pady=9, width=15)
        self.bom_label = tk.Label(self.labels_frame, textvariable=self.bom_value, bd=1, relief=tk.SUNKEN, anchor=tk.E, padx=10, pady=9, width=12)
        
    def get_value(self):
        return self.root.text_value.get()
        
    def set_value(self, text):
        if os.name == "nt":  # Windows
            text = text.replace("/", "\\")
        self.text_value.set(text)
            
    def set_filesize_value(self, size_bytes=0):
        # Define the units and their respective suffixes
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        # Get the index of the appropriate unit to use for conversion
        index = 0
        while size_bytes >= 1024 and index < len(units) - 1:
            size_bytes /= 1024
            index += 1

        # Format the size with up to two decimal places
        value = f"{size_bytes:.2f} {units[index]}"
        self.filesize_value.set(value)
        
        
    def show(self):
        # pass
        self.labels_frame.columnconfigure(1, weight=1)
        self.labels_frame.pack(side=tk.BOTTOM, fill=tk.X)
        # self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_label.grid(row=0, column=0, columnspan=4, sticky="we")
        self.linecount_label.grid(row=0, column=1, sticky="e")
        self.filesize_label.grid(row=0, column=2, sticky="e")
        self.encoding_label.grid(row=0, column=3, sticky="e")
        self.bom_label.grid(row=0, column=4, sticky="e")
        
    def hide(self):
        self.labels_frame.pack_forget()
        
    def toggle_visibility(self, int_value):
        if int_value == 0:
            self.hide()
        else:
            self.show()        
        