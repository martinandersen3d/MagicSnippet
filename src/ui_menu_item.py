import tkinter as tk

# Create the root window
# root = tk.Tk()


# Create a menu bar
# menu_bar = tk.Menu(root)
# root.config(menu=menu_bar)

class MenuItem:
    def __init__(self, parent_menu_bar = None, title = ""):
        self.parent_menu_bar = parent_menu_bar
        self.title = title

        # Create the first menu
        self.menu = tk.Menu(self.parent_menu_bar, tearoff=False)

        # Add the first menu to the menu bar
        self.parent_menu_bar.add_cascade(label=self.title, menu=self.menu, underline=0)

        # Examples of how to add a submenu-item:
        # Parameters:
        # 1: Menu Label
        # 2: Method to call on click
        # 3: Paramters to send to the method on click
        # 4: Hotkey, example "Alt_L+o"
        # self.add_submenu_item("One", self.printer, "item 1")
        # self.add_submenu_item("Two", self.printer, "item 2")
        # self.add_seperator()
        # self.add_submenu_item("Redraw", self.redraw_menu, "redraw stuff")
        # self.add_submenu_item("Remove All", self.remove_all, "removes")

    # Define a function to add an item to the first menu
    def add_submenu_item(self, label_text, callback_function, function_param_content="", hotkey=""):
        self.menu.add_command(label=label_text, command=lambda: callback_function(function_param_content), accelerator=hotkey)

    # Define a function to remove the last item from the first menu
    def remove_submenu_item(self):
        self.menu.delete(len(menu_bar.get_menuitems())-1)

    def redraw_menu(self, param):
        print(self.menu.get_menuitems())
        self.menu.delete(2)
            
    def remove_all(self, param):
        last_index = self.menu.index('end')
        # Python range is a bit strange.. and yes it has to go to -1
        for i in range(last_index, -1, -1):
            self.menu.delete(i)
            
    def count_submenu_items(self):
        last_index = self.menu.index('end')
        item_count = last_index + 1
        return item_count

    def add_seperator(self):
        self.menu.add_separator()    


# xxx = MenuItem(menu_bar, "Directories")
# xxx.add_submenu_item("Hi", xxx.printer, "outside")
# MenuItem(menu_bar, "Open In")
# root.mainloop()
