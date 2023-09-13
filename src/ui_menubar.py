import os
import tkinter as tk
from ui_menu_item import MenuItem

class Menubar:
    def __init__(self, root, controller):
        
        self.root = root
        self.controller = controller
        
        # Create variables to store the checkbox states
        self.menu_show_linenumber = self.controller.AppSetting.menu_show_linenumber
        self.menu_show_searchinsidefiles = self.controller.AppSetting.menu_show_searchinsidefiles
        self.menu_show_statusbar = self.controller.AppSetting.menu_show_statusbar

        
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # FILE MENU
        self.menu_file = MenuItem(menu_bar, "File")
        self.menu_file.add_submenu_item("New File..            ", self.controller.menu_new_file, None, hotkey="Ctrl+N")
        self.menu_file.add_submenu_item("Save File As..            ", self.controller.menu_file_save_file_as, None, hotkey="Ctrl+S")
        self.menu_file.add_submenu_item("Open A File in Text Editor..            ", self.controller.menu_open_file, None, hotkey="Ctrl+O")
        self.menu_file.add_seperator()
        self.menu_file.add_submenu_item("Open In Text Editor            ", self.controller.menu_open_selected_file, None, hotkey="Ctrl+K")
        self.menu_file.add_submenu_item("Open In File Manager            ", self.controller.menu_open_selected_file_in_filemanager, None, hotkey="Ctrl+E")
        self.menu_file.add_submenu_item("Open In VsCode            ", self.controller.menu_open_selected_file_in_vscode, None, hotkey="Ctrl+D")
        self.menu_file.add_seperator()
        self.menu_file.add_submenu_item("Exit            ", self.controller.exit_app, None, hotkey="ESC")
        
        # COPY MENU
        self.menu_copy = MenuItem(menu_bar, "Copy")
        self.menu_copy.add_submenu_item("Copy Content            ", self.controller.menu_copy_text_to_clipboard, None, hotkey="Enter")
        # Todo: On linux/Wayland, i dont know how to simulate a Ctrl+V press, I need more time for this feature
        if self.controller.linux_session_type != "wayland":
            self.menu_copy.add_submenu_item("Copy Content And Paste Into Background Program", self.controller.menu_copy_and_paste_into_background_program, None, hotkey="Shift+Enter")
        self.menu_copy.add_submenu_item("Copy HTML as Formatted Text", self.controller.menu_copy_HTML_as_formatted_text_to_clipboard, None, hotkey="Ctrl+H")
        self.menu_copy.add_submenu_item("Copy Markdown as Formatted Text", self.controller.menu_copy_markdown_as_HTML_formatted_text_to_clipboard, None, hotkey="Ctrl+M")
        self.menu_copy.add_seperator()
        self.menu_copy.add_submenu_item("Copy Fullpath", self.controller.menu_copy_fullpath_to_clipboard, None, hotkey="F1")
        self.menu_copy.add_submenu_item("Copy Filename", self.controller.menu_copy_filename_to_clipboard, None, hotkey="F2")
        self.menu_copy.add_submenu_item("Copy Folder Path", self.controller.menu_copy_folderpath_to_clipboard, None, hotkey="F3")
        self.menu_copy.add_seperator()

        if os.name == 'posix':
            self.menu_copy.add_submenu_item("Copy File to Clipboard. And Paste in Nautilus..", self.controller.menu_copy_file_like_filemanager, None, hotkey="F4")
            self.menu_copy.add_submenu_item("Copy File to Clipboard. And Paste in Applications.. ", self.controller.menu_copy_file_linux_x11_other_programs, None, hotkey="F5")
        if os.name == 'nt':
            self.menu_copy.add_submenu_item("Copy File to Clipboard, like Windows Explorer", self.controller.menu_copy_file_like_filemanager, None, hotkey="F4")

        # VIEW MENU
        view_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="View", menu=view_menu, underline=0)
        view_menu.add_checkbutton(label="Line Numbers", variable=self.menu_show_linenumber, onvalue=1, offvalue=0, command=self.controller.menu_view_linenumbers)
        view_menu.add_checkbutton(label="Search Inside Files", variable=self.menu_show_searchinsidefiles, onvalue=1, offvalue=0, command=self.controller.menu_view_searchinsidefiles)
        view_menu.add_checkbutton(label="Statusbar", variable=self.menu_show_statusbar, onvalue=1, offvalue=0, command=self.controller.menu_view_statusbar)
        
        # SETTINGS MENU
        self.menu_settings = MenuItem(menu_bar, "Settings")
        self.menu_settings.add_submenu_item("Directory Settings", self.controller.menu_settings_directory_settings, None)
        self.menu_settings.add_submenu_item("Exclude Filepath Settings", self.controller.menu_settings_exclude_files, None)
        self.menu_settings.add_submenu_item("Open Config Directory in Filemanager", self.controller.menu_settings_open_filemanager, None)
        self.menu_settings.add_submenu_item("Reload Directorys", self.controller.menu_settings_reload_directorys, None)

        # HELP MENU
        self.menu_help = MenuItem(menu_bar, "Help")
        self.menu_help.add_submenu_item("Documentation", self.controller.menu_help_documentation, None)
        self.menu_help.add_submenu_item("Keyboard Shortcuts", self.controller.menu_help_keyboard_shortcuts, None)
        self.menu_help.add_seperator()
        self.menu_help.add_submenu_item("Report a Problem", self.controller.menu_help_report_a_problem, None)
        self.menu_help.add_submenu_item("Suggest a Feature", self.controller.menu_help_suggest_a_feature, None)
        self.menu_help.add_submenu_item("Give Feedback", self.controller.menu_help_give_feedback, None)
        self.menu_help.add_seperator()
        self.menu_help.add_submenu_item("Version", self.controller.menu_help_version, None)