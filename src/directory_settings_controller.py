import os
import json
import sys
from file_controller import *

class DirectorySettingsController:
    def __init__(self, items=[]):
        self.items = items
    
    def save_config(self):
        FileController().save_directory_config(self.items)

    def load_config(self):
        return FileController().load_directory_config()

# ------------------------------------------------------------------------------------------------

        
# settings=[
#     {"active": True, "path": "/some/path1"},
#     {"active": False, "path": "/some/path2"}
# ]
# ds = DirectorySettingsController(settings)
# ds.save_config()
# ds.load_config()

# for item in ds.items:
#     print(item.active, item.path)