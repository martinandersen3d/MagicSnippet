import os
import json
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont

# TODO: add Program Nice name to self.paths

class ProgramItem:
    def __init__(self, displayName, path):
        self.displayName = displayName
        self.path = path
    def __json__(self):
        return {"a":"d"}

class OpenInProgramSettings:
    def __init__(self):
        self.paths = []
        self.window = tk.Tk()
        self.window.geometry("1000x800")
        self.window.title("Open File in Program.. - Settings")

        # Path label
        path_label = tk.Label(self.window, text="Open file with the following programs:")
        path_label.pack(padx=8, pady=10, anchor='w')

        # Path listbox
        self.listbox = tk.Listbox(self.window)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=8, padx=8)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        # Add path button
        add_button = tk.Button(self.window, text="Add Program To List", command=self.add_listbox_item, width=20, height=2, padx=8)
        add_button.pack(fill=tk.X, pady=4, padx=8)

        # Remove path button
        remove_button = tk.Button(self.window, text="Remove Program From List", command=self.remove_selected_listbox_item, width=20, height=2, padx=8)
        remove_button.pack(fill=tk.X, padx=8, pady=8)

        # Save paths button
        # save_button = tk.Button(self.window, text="Save Paths", command=self.save_settings, width=20, height=2, padx=8, pady=8)
        # save_button.pack(fill=tk.X, pady=10)

        # # Load paths button
        # load_button = tk.Button(self.window, text="Load Paths", command=self.startup, width=20, height=2, padx=8, pady=8)
        # load_button.pack(fill=tk.X, pady=10)

        # Create a frame to hold the elements
        frame = tk.LabelFrame(self.window, text="Program Configuration")
        frame.pack(fill=tk.X, padx=8, pady=8)
        
        # Create the label for the program name
        name_label = tk.Label(frame, text="Program name - In the UI:")
        name_label.pack(side=tk.TOP, padx=8, pady=(16, 0), anchor='w')

        # Create a font object with a specific size
        font = tkFont.Font(size=12)

        # Create the text field for the program name
        self.name_field = tk.Entry(frame, font=font)
        self.name_field.pack(fill=tk.X, side=tk.TOP, padx=8, pady=8, ipady=8, ipadx=8)
        self.name_field.bind("<KeyRelease>", self.on_field_change)   
        self.name_field.bind("<FocusOut>", self.on_field_loose_focus)   

        # Create the label for the program path
        path_label = tk.Label(frame, text="Program path:")
        path_label.pack(side=tk.TOP, padx=8, pady=(16, 0), anchor='w')

        # Create the text field for the program path
        self.path_field = tk.Entry(frame, font=font)
        self.path_field.pack(fill=tk.X, side=tk.TOP, padx=8, pady=8, ipady=8, ipadx=8)
        self.path_field.bind("<KeyRelease>", self.on_field_change)      
        self.path_field.bind("<FocusOut>", self.on_field_loose_focus)   


        picker = tk.Button(frame, text="Select program...", command=self.on_filepicker_click)
        picker.pack(side=tk.RIGHT, anchor='ne')


        # Create the label for the program parameters
        # param_label = tk.Label(frame, text="Program parameters:")
        # param_label.pack(side=tk.TOP, padx=8, pady=(16, 0), anchor='w')

        # Create the text field for the program parameters
        # param_field = tk.Entry(frame)
        # param_field.pack(fill=tk.X, side=tk.TOP, padx=8, pady=8, ipady=8, ipadx=8)

        label1 = tk.Label(frame, text="f%: File fullpath - Will insert the fullpath to the selected file")
        label1.pack(side=tk.TOP, padx=8, pady=(0, 0), anchor='w')
        label2 = tk.Label(frame, text="d%: Directory Basepath - Will insert the fullpath to the directory, where the selected file is")
        label2.pack(side=tk.TOP, padx=8, pady=(8, 0), anchor='w')
        label3 = tk.Label(frame, text="u%: Username - Will insert your username")
        label3.pack(side=tk.TOP, padx=8, pady=(8, 16), anchor='w')
        # Load paths from config file

        # Config file path label
        config_path_label = tk.Label(self.window, text=f"Config file: {self.get_config_path()}")
        config_path_label.pack(pady=20, anchor='w')

        # Open config file directory button
        open_button = tk.Button(self.window, text="Open Config Folder", command=self.open_config_path, height=2, padx=8, pady=8)
        open_button.pack(fill=tk.X, padx=8, pady=8)

        self.startup()
        self.window.mainloop()

    def on_listbox_select(self,event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected = self.paths[index]
             # Unfreeze the Entry widget
            self.name_field.delete(0, tk.END)
            self.path_field.delete(0, tk.END)
            self.name_field.insert(0, selected.displayName) 
            self.path_field.insert(0, selected.path) 
        else:
            self.name_field.delete(0, tk.END)
            self.path_field.delete(0, tk.END)

            
   
    def on_field_change(self,event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            selected = self.paths[index]
            selected.displayName = self.name_field.get()   
            selected.path = self.path_field.get()
            self.paths[index] = selected
            self.save_settings() 
            
   
    def on_field_loose_focus(self,event):
        selection = self.listbox.curselection()
        if selection:
            self.save_settings()
            index = selection[0]
            self.refresh_listbox()

    def set_field_freeze_state(self):
        if self.listbox.size()> 0:
            self.name_field.config(state="normal")
            self.path_field.config(state="normal")
        else:
            self.name_field.delete(0, tk.END)
            self.path_field.delete(0, tk.END)
            self.name_field.insert(0, "") 
            self.path_field.insert(0, "") 
            self.name_field.config(state="disabled")
            self.path_field.config(state="disabled")

    def on_filepicker_click(self):
        # Show a file picker dialog
        filename = filedialog.askopenfilename()
        self.path_field.delete(0, tk.END)
        self.path_field.insert(0, filename + ' "%f"') 
        self.on_field_change(None)
        self.on_field_loose_focus(None)


    # ------------------------------------------------------------------------------
    def listbox_has_selection(self):
        selection = self.listbox.curselection()
        if selection:
            return True
        return False
    
    def listbox_get_selected_index(self):
        selection = self.listbox.curselection()
        if selection:
            return selection[0]
        return None
    
    def refresh_listbox(self):
        index = None
        self.paths = []
        if self.listbox_has_selection():
            index = self.listbox_get_selected_index()
        
        
        config_path = self.get_config_path()
        if os.path.exists(config_path):
            self.listbox.delete(0, tk.END)  # clear the listbox
            with open(config_path, "r") as f:
                config = json.load(f)
                data = config.get("paths", [])

                for item in data:
                    self.paths.append(ProgramItem(item['displayName'], item['path']))

                for item in self.paths:
                    self.listbox.insert(tk.END, item.displayName)
            if index != None and index < self.listbox.size():
                self.listbox.selection_set(index, index)
                
        
    # ------------------------------------------------------------------------------
    
     
    def add_listbox_item(self):
        newProgram = ProgramItem('app','notepad "%f"')
        
        self.paths.append(newProgram)
        self.listbox.insert(tk.END, newProgram.displayName)
        self.set_field_freeze_state()
        self.save_settings()
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(tk.END)
        self.on_listbox_select(None)

    def remove_selected_listbox_item(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.paths.pop(index)
            self.listbox.delete(index)
            self.set_field_freeze_state()
            self.save_settings()
            if index < self.listbox.size():
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(index,index)  
                self.on_listbox_select(None)
            elif index> 0:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(index-1,index-1)  
                self.on_listbox_select(None)

    def save_settings(self):
        # Convert array of Person classes to JSON
        programs = [p.__dict__ for p in self.paths]
        config = {"paths": programs}
        with open(self.get_config_path(), "w") as f:
            json.dump(config, f)


    def startup(self):
        config_path = self.get_config_path()
        if os.path.exists(config_path):
           self.refresh_listbox()
           self.set_field_freeze_state()
        else:
            if os.name == "posix":  # Linux, macOS
                self.paths.append(ProgramItem('Explorer', 'explorer /select,"%f"'))
                
            elif os.name == "nt":  # Windows
                self.paths.append(ProgramItem('Vs Code', 'code  --new-window "%f" "%d"'))
                self.paths.append(ProgramItem('Explorer', 'explorer /select,"%f"'))
                self.paths.append(ProgramItem('Notepad', 'notepad "%f"'))
            self.save_settings()
            self.refresh_listbox()
            

    def get_config_path(self):
        home_dir = os.path.expanduser("~")
        if os.name == "posix":  # Linux, macOS
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.OpenInProgram.Linux.config.json")
        elif os.name == "nt":  # Windows
            self.create_config_dir()
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.OpenInProgram.Windows.config.json")

    def open_config_path(self):

        config_dir = os.path.dirname(self.get_config_path())
        if os.name == "posix":  # Linux, macOS
            os.system(f"xdg-open '{config_dir}'")
        elif os.name == "nt":  # Windows
            os.startfile(config_dir)

    def create_config_dir(self):
        try:
        
            user_dir = os.path.expanduser("~")
            if os.name == "nt":  # Windows
                # config_dir = os.path.join(user_dir, "AppData", "Roaming", "MagicSnippet")        
                config_dir = os.path.join(user_dir, ".MagicSnippet")        
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            messagebox.showinfo("Path Error", sys.exc_info()[0])
            raise

if __name__ == "__main__":
    OpenInProgramSettings()


# 1. if no config file
#   2. create one and seed, depending on what os it is
# 3. if config file > load it 