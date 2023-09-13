import tkinter as tk

# Debounce: Debounce in a text field refers to delaying the execution of a function until the user stops typing for a specified period, preventing rapid or unnecessary updates.

class DebouncedEntry:
    def __init__(self, master=None, *args, **kwargs):
        self.entry = tk.Entry(master, *args, **kwargs)
        self.entry.bind("<KeyPress>", self._on_key_press)
        self.entry.bind("<KeyRelease>", self._on_key_release)
        self.debounce_times = {1: 600, 2: 600, 3: 300, 4: 200}
        self.current_value = self.entry.get()
        self.alt_pressed = False
        self.shift_pressed = False
        self.ctrl_pressed = False
        self.fn_on_keypress = None
        self.event_on_key_press = None
        
        self.entry.bind("<Button-3>", self.on_entry_show_context_menu)
        self.entry.bind("<Control-v>", self.on_entry_paste_from_clipboard)
        self.entry.bind("<Control-a>", self.on_entry_select_all)
        self.entry.bind("<Control-x>", self.on_entry_cut_text)
        self.entry.bind("<Control-c>", self.on_entry_copy_text)

    def _on_key_press(self, event):
        self.event_on_key_press = event
        if event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift_pressed = True
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl_pressed = True
        if event.keysym == "Alt_L":
            self.alt_pressed = True
        # Do nothing with these arrows
        if event.keysym in ["Left", "Right", "Up"]:
            return
        
        self.current_value = self.entry.get()
        debounce_time = self.debounce_times.get(len(self.current_value), 150)

        # If backspace is used, then increase the debounce
        if event.keysym == 'BackSpace':
            debounce_time = 450

        if hasattr(self, '_timer_id'):
            self.entry.after_cancel(self._timer_id)

        self._timer_id = self.entry.after(debounce_time, self._execute_callback)

    def _on_key_release(self, event):
        if event.keysym == "Shift_L" or event.keysym == "Shift_R":
            self.shift_pressed = False
        if event.keysym == "Control_L" or event.keysym == "Control_R":
            self.ctrl_pressed = False
        if event.keysym == "Alt_L":
            self.alt_pressed = False
        
    def _execute_callback(self):
        value = self.entry.get()
        print("Debounced Value:", value)  # Replace this line with your desired action

        # if self.shift_pressed and value.lower() == "enter":
        #     self.on_entry_shift_enter()

        # if value.lower() == "alt+backspace":
        #     self.on_entry_alt_backspace()
        if self.fn_on_keypress != None:
           self.fn_on_keypress(self.event_on_key_press)

    def on_entry_alt_backspace(self):
        print('Alt Backspace')
        self.reset_entry()

    def on_entry_shift_enter(self):
        print('Shift Enter')
        self.reset_entry()

    def setup_on_keypress(self, callback_function):
        self.fn_on_keypress = callback_function
    
    # -----------------------------------------

    def get(self):
        return self.entry.get()

    def insert(self, start_index, content):
        self.entry.insert( start_index, content)

    def focus_set(self):
        self.entry.focus_set()

    def focus(self):
        self.entry.focus()

    def delete(self, start, end):
        self.entry.delete(start, end)

    def configure(self):
        self.entry.configure(background="white")

    def pack(self):
        self.entry.pack(fill="both", expand=True)

    def reset_entry(self):
        self.entry.delete(0, 'end')
        self.entry.focus_set()

    def bind(self, key_string, callback_fn):
        self.entry.bind( key_string, callback_fn)

    def selection_present(self):
        self.entry.selection_present()

    def select_range(self, start, end):
        self.entry.select_range(start, end)

    def icursor(self, end):
        self.entry.icursor(end)  # Moves the cursor to the end of the selected text

    def event_generate(self, event_string):
        self.entry.event_generate(event_string)

    # Context Menu ---------------------------------------------------
    def on_entry_show_context_menu(self, event):
        context_menu = tk.Menu(self.entry, tearoff=0)
        context_menu.add_command(label="Cut", command=self.on_entry_cut_text)
        context_menu.add_command(label="Copy", command=self.on_entry_copy_text)
        context_menu.add_command(label="Paste", command=self.on_entry_paste_from_clipboard)
        context_menu.add_command(label="Select All", command=self.on_entry_select_all)
        context_menu.tk_popup(event.x_root, event.y_root)

    def on_entry_cut_text(self, event=None):
        try:
            self.entry.event_generate("<<Cut>>")
            return "break"
        except:
            pass

    def on_entry_copy_text(self, event=None):
        try:
            self.entry.event_generate("<<Copy>>")
            return "break"
        except:
            pass
        
    def on_entry_paste_from_clipboard(self, event=None):
        try:
            has_selected_text = self.entry.selection_present()
            if has_selected_text:
                self.entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
            # content = self.root.clipboard_get()
            # self.root.entry.insert(tk.INSERT, content)
            self.entry.event_generate("<<Paste>>")
            print('paste')
        except:
        #     print('no paste')
            pass

    def on_entry_select_all(self, event=None):
        try:
            # self.root.entry.tag_add(tk.SEL, "1.0", tk.END)
            # self.root.entry.mark_set(tk.INSERT, "1.0")
            # self.root.entry.see(tk.INSERT)
            
            self.entry.select_range(0, tk.END)  # Selects all text in the Entry widget
            self.entry.icursor(tk.END)  # Moves the cursor to the end of the selected text

            return "break"
        except:
            pass
            

if __name__ == "__main__":
    # Example usage:
    root = tk.Tk()
    root.title("Debounced Entry")

    entry1 = DebouncedEntry(root)
    entry1.entry.pack(padx=10, pady=10)

    entry2 = DebouncedEntry(root)
    entry2.entry.pack(padx=10, pady=10)

    root.mainloop()
