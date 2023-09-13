#!/usr/bin/env python3 

import os
import sys
import tkinter as tk
from controller import *

app_version = "0.9"

if __name__ == "__main__":
    
    ui = tk.Tk()
    # ui.bind('<Visibility>', app.initialize_listbox())
    app = Controller(ui, app_version)
    # ui.after_idle(app.initialize_listbox())
    
    # ui.protocol("WM_DELETE_WINDOW", app.initialize_listbox())    
    app.root.mainloop()


