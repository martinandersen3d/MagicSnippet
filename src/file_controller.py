import glob
import os.path 
from pathlib import Path
import os
import json
import sys
from tkinter import messagebox


# FILEPATH --------------------------------------------------------------
class FilePath:
    def __init__(self, fullpath: str, startPath: str):
        self.fullpath = fullpath
        self.baseName = os.path.basename(fullpath)
        self.shortpath = fullpath.replace(startPath, "")
        self.nicename = self.shortpath.replace("%20", " ")
        self.score = 0
        if self.nicename[0] == "/" or self.nicename[0] == "\\":
            # remove first slash in path
           self.nicename = self.nicename[1:]

    # Print the class
    def __repr__(self):
        return f"basename:{self.baseName} | fullpath: {self.fullpath} | shortpath: {self.shortpath} | nicename: {self.nicename}\n"

    # Sort the class based on alphabetical order and case-insensitive
    def __lt__(self, other):
        return self.shortpath.lower() < other.shortpath.lower()

# TREEITEM --------------------------------------------------------------
class TreeItem:
    def __init__(self, active=True, path=""):    
        self.active = active
        self.path = path
        
    def to_dict(self):
        return {'active': self.active, 'path': self.path}

# FILECONTROLLER --------------------------------------------------------------

class FileController:
    def __init__(self):
        self.items = []
        pass

    # INIT GET FILE LIST ---------------------------------------------------------------
    # Get all the snippet files when the program starts up
    def load_file_list(self):
        # Load Directory Config
        directory_config = self.load_directory_config()
        
        # Load Exlude Config
        exclude_config = self.load_exludefiles_config()

        # Find all snippet files
        treeItems = []
        
        for treeItem in directory_config:
            if treeItem.active == True:
                snippet_dir = treeItem.path
                for r, d, f in os.walk(snippet_dir):
                    for file in f:
                        fullpath=os.path.join(r, file)
                        treeItems.append(FilePath(fullpath, snippet_dir))
         
        # Exclude Files
            
        # Run through the full list and remove filepaths that is excluded
        excludelist =  exclude_config
        newTreeItemList = []
        for treeItem in treeItems:
            if self.is_whitelisted(treeItem, excludelist):
                newTreeItemList.append(treeItem)
        
        newTreeItemList.sort()
        
        # Return file list
        return newTreeItemList

    def is_whitelisted(self, filepath, excludelist):
        for exludepath in excludelist:
            expath = exludepath.lower().replace('\\', '/').replace('\\\\', '/')
            fullpath = filepath.fullpath.lower().replace('\\', '/').replace('\\\\', '/')
            if expath in fullpath:
                return False
        return True
        
    
    

    # APP SETTINGS ---------------------------------------------------------------
    
    def load_app_settings(self, appsettings):
        config_path = self.get_appsettings_path()
        if not os.path.exists(config_path):
            self.save_app_settings(appsettings)
        with open(config_path, "r") as f:
            config = json.load(f)
        appsettings = config.get("appsettings", {})
        return appsettings
        
    def save_app_settings(self, appsettings):
        config = {"appsettings": appsettings}
        with open(self.get_appsettings_path(), "w") as f:
            json.dump(config, f)
    
    def get_appsettings_path(self):
        home_dir = os.path.expanduser("~")
        if os.name == "posix":  # Linux, macOS
            self.create_directory_config_dir()
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.AppSettings.Linux.json")
        elif os.name == "nt":  # Windows
            self.create_exlude_config_dir()
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.AppSettings.Windows.json")



    # DIRECTORY ---------------------------------------------------------------

    def load_directory_config(self):
        config_path = self.get_directory_config_path()
        if os.path.exists(config_path):
            # self.path_listbox.delete(0, tk.END)  # clear the listbox
            with open(config_path, "r") as f:
                self.items = []
                config = json.load(f)
                config_items = config.get("config", [])
                for item in config_items:
                    newItem = TreeItem(item['active'], item['path'])
                    self.items.append(newItem)
        return self.items

    def save_directory_config(self, items):
        dicts = []
        for item in items:
            dicts.append(item.to_dict())
        config = {"config": dicts}
        with open(self.get_directory_config_path(), "w") as f:
            json.dump(config, f)
    
    def get_directory_config_path(self):
        home_dir = os.path.expanduser("~")
        if os.name == "posix":  # Linux, macOS
            self.create_directory_config_dir()
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.DirectorySettings.Linux.json")
        elif os.name == "nt":  # Windows
            self.create_exlude_config_dir()
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.DirectorySettings.Windows.json")

    def open_directory_config_in_filemanager(self):
        config_dir = os.path.dirname(self.get_directory_config_path())
        if os.name == "posix":  # Linux, macOS
            os.system(f"xdg-open '{config_dir}'")
        elif os.name == "nt":  # Windows
            os.startfile(config_dir)

    def create_directory_config_dir(self):
        try:
            user_dir = os.path.expanduser("~")
            if os.name == "posix":  # Windows
                # config_dir = os.path.join(user_dir, "AppData", "Roaming", "MagicSnippet")        
                config_dir = os.path.join(user_dir, ".MagicSnippet")        
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir)
            if os.name == "nt":  # Windows
                # config_dir = os.path.join(user_dir, "AppData", "Roaming", "MagicSnippet")        
                config_dir = os.path.join(user_dir, ".MagicSnippet")        
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir)

        except:
            print("Unexpected error:", sys.exc_info()[0])
            messagebox.showinfo("Path Error", sys.exc_info()[0])
            raise


    # EXCLUDE FILES---------------------------------------------------------------
    
    def load_exludefiles_config(self):
        filepath = self.get_exlude_config_path()
        
        # If the config file does not exist then create it
        if not os.path.exists(filepath):
            self.set_default_exlude_list()
        
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, "r") as file:
                    self.filepaths = file.read().splitlines()
                return self.filepaths
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def save_exludefiles_config(self, exclude_files_list):
        filepath = self.get_exlude_config_path()
        if filepath:
            try:
                with open(filepath, "w") as file:
                    for item in exclude_files_list:
                        file.write(item + "\n")
                messagebox.showinfo("Save", "List Saved to:\n" + filepath )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    # To get the list of exclude files
    # def get_exlude_paths_list(self):


            
    def get_exlude_config_path(self): 
        home_dir = os.path.expanduser("~")
        if os.name == "posix":  # Linux, macOS
            self.create_exlude_config_dir()
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.FilepathExcludeSettings.Linux.txt")
        elif os.name == "nt":  # Windows
            self.create_exlude_config_dir()
            return os.path.join(home_dir, ".MagicSnippet", "MagicSnippet.FilepathExcludeSettings.Windows.txt")

    def create_exlude_config_dir(self):
        try:
        
            user_dir = os.path.expanduser("~")
            if os.name == "posix":  # Windows
                # config_dir = os.path.join(user_dir, "AppData", "Roaming", "MagicSnippet")        
                config_dir = os.path.join(user_dir, ".MagicSnippet")        
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir)
            if os.name == "nt":  # Windows
                # config_dir = os.path.join(user_dir, "AppData", "Roaming", "MagicSnippet")        
                config_dir = os.path.join(user_dir, ".MagicSnippet")        
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir)

        except:
            # print("Unexpected error:", sys.exc_info()[0])
            # messagebox.showinfo("Path Error", sys.exc_info()[0])
            pass

    # To get the list of exclude files
    def get_exlude_paths_list(self):
        filepath = self.get_exlude_config_path()
        
        # If the config file does not exist then create it
        if not os.path.exists(filepath):
            self.set_default_exlude_list()
        
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, "r") as file:
                    filepaths = file.read().splitlines()
                return filepaths
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")


    # If it cant find a config file list it will save these defaults
    def set_default_exlude_list(self):
        exclude_files = [
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

        # CSS/JS
        '.min.', #Minified files
        
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
        exclude_files.sort()
        self.save_exludefiles_config(exclude_files)
        

