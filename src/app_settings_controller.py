import os
import sys
import tkinter as tk
# from tkcode import CodeBlock
from tkinter import ttk

from file_controller import FileController

class AppSettingsController:
    def __init__(self, controller):

        self.controller = controller
        
        # Default: 0
        self.menu_show_linenumber = tk.IntVar()
        self.menu_show_searchinsidefiles = tk.IntVar()
        self.menu_show_statusbar = tk.IntVar()
        
        self.load_settings()

    def save_settings(self):
        config = self.to_json()
        FileController().save_app_settings(config)

    def load_settings(self):
        config = self.to_json()
        from_config = FileController().load_app_settings(config)
        self.from_json(from_config)

    def to_json(self):
        return {
            "menu_show_linenumber": self.menu_show_linenumber.get(),
            "menu_show_searchinsidefiles": self.menu_show_searchinsidefiles.get(),
            "menu_show_statusbar": self.menu_show_statusbar.get()
        }

    def from_json(self, config):
        self.menu_show_linenumber.set(config.get("menu_show_linenumber", 0))
        self.menu_show_searchinsidefiles.set(config.get("menu_show_searchinsidefiles", 0))
        self.menu_show_statusbar.set(config.get("menu_show_statusbar", 0))