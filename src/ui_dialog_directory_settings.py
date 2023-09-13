import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from directory_settings_controller import *
from file_controller import *

                
class DirectorySettings:
    def __init__(self, controller):
        
        self.DirectorySetting = DirectorySettingsController()
        self.items = []
        self.window = tk.Tk()
        self.window.geometry("1000x500")
        self.window.title("Folder Settings")
        self.controller = controller
        self.selectedIndex = None


        # Add the "Add", "Remove", and "Toggle Active" buttons above the Treeview
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(side="top", fill="x", padx=16, pady=16)
        add_button = tk.Button(self.button_frame, text="Add Folder", command=self.add_folder)
        add_button.pack(side="left", padx=5)
        remove_button = tk.Button(self.button_frame, text="Remove From List", command=self.remove_item)
        remove_button.pack(side="left", padx=5)
        toggle_active_button = tk.Button(self.button_frame, text="Toggle Active", command=self.toggle_active)
        toggle_active_button.pack(side="left", padx=5)

        # Create a Treeview with two columns: "active" and "path"
        self.treeview = ttk.Treeview(self.window, columns=("active", "path"), show="headings")
        self.treeview.heading("active", text="Active",anchor="w")
        self.treeview.heading("path", text="Path",anchor="w")
        
        self.treeview.column("active", width=130, stretch=False)
        self.treeview.column("path", stretch=True)
        
        self.treeview.pack(side="left", fill="both", expand=True, padx=(16, 16), pady=(8, 16))

        self.treeview.bind("<<TreeviewSelect>>", self.on_click)
        # Doubleclick
        self.treeview.bind("<Double-1>", self.on_double_click)
        self.treeview.bind('<KeyPress>', self.on_keypress)
        # Populate the Treeview with sample data
        # self.treeview.insert("", "end", values=(True, "/path/to/folder1"))
        # self.treeview.insert("", "end", values=(False, "/path/to/folder2"))
        self.redraw()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set focus on the first item if it exists
        # Select the first item if it exists
        children = self.treeview.get_children()
        if children:
            first_item = children[0]
            self.treeview.selection_set(first_item)
            self.treeview.focus(first_item)
            print("YES")
        
        self.window.mainloop()


    def add_folder(self):
        # Open a file dialog to select a folder
        folder = filedialog.askdirectory()
        doesAllreadyExist=False
        if folder:
            for item in self.items:
                if item.path == folder:
                    doesAllreadyExist = True
                    break
            if doesAllreadyExist == False:
                self.items.append( TreeItem(True, folder) )
                self.DirectorySetting.items = self.items
                self.DirectorySetting.save_config()
                
        self.redraw()
        self.window.lift()  # Push the window to the front


    def remove_item(self):
        # Remove the selected item from the Treeview
        index = self.get_selected_index()
        if index != None:
            index = self.get_selected_index()-1
            del self.items[index]
            self.save()
            self.redraw()
        
    def toggle_active(self):
        # Toggle the active status of the selected item in the Treeview
        index = self.get_selected_index()
        try:
            item = self.items[self.get_selected_index()-1]
            print(item.active)
            if item.active == True:
               item.active = False
            else:
                item.active = True
        except:
            pass
        self.save()
        self.redraw()
    
        if index != None:
            self.selectedIndex = index-1
            self.set_selected_index()
            self.treeview.focus_set()        
        
    def save(self):
        self.DirectorySetting.items = self.items
        self.DirectorySetting.save_config()
        

    def redraw(self):
        self.items = self.DirectorySetting.load_config()
        # self.treeview.delete("all")
        self.treeview.delete(*self.treeview.get_children())

        for item in self.items:
            self.treeview.insert("", "end", values=(item.active, item.path))

        # self.set_selected_index()
        # if self.selectedIndex != None and len(self.items) <= self.selectedIndex :
        #    self.treeview.selection_set(self.selectedIndex)
        
    def get_selected_index(self):
        
        index = None
        
        all_items = self.treeview.get_children()
        count = len(all_items)
        selected = self.treeview.focus()
        counter=0
        if selected != "":
            for item in all_items:
                counter+=1
                if selected == item:
                    break
        if count > 0:
            index = counter
        
        if index:
            # Return the index of the first selected item as an integer
            self.selectedIndex = index
            return index
        else:
            # No item is selected
            self.selectedIndex = None
            return None

    def set_selected_index(self):

        index = self.selectedIndex  # set the focus to the third item in the tree (index 2)
        item_id = self.treeview.get_children()[index]
        self.treeview.selection_set(item_id)
        
        # index = None
        
        # all_items = self.treeview.get_children()
        # count = len(all_items)
        # counter=0
        # for item in all_items:
        #     if counter == self.get_selected_index():
        #         # item_id = self.treeview.get_children()[index]
        #         self.treeview.selection_set(item_id)
        #     counter+=1
            
        
        # if count > 0:
        #     index = counter
        
        # if index:
        #     # Return the index of the first selected item as an integer
        #     self.selectedIndex = index
        #     return index
        # else:
        #     # No item is selected
        #     self.selectedIndex = None
        #     return None


    def on_click(self,event):
        self.get_selected_index()

    def on_double_click(self, event):
        self.toggle_active()
        
    def on_keypress(self,event):
        if  event.keysym == 'space':
            self.toggle_active()
    
    def open_folder(self, dir):
        if os.name == "posix":  # Linux, macOS
            os.system(f"xdg-open '{dir}'")
        elif os.name == "nt":  # Windows
            os.startfile(f"'{dir}'")

    def on_closing(self):
        try:
            self.controller.listbox_reload()
        except:
          pass
        self.window.destroy()
        
            
# root = tk.Tk()
# app = TreeviewExample(root)
# root.mainloop()
