import tkinter as tk
from tkinter import filedialog, messagebox

class TextEditorApp:
    def __init__(self, width=1600, height=900):
        self.window = tk.Tk()
        self.window.title("Text Editor - New File..")
        self.window.geometry(f"{width}x{height}")

        self.create_text_field()
        self.create_save_button()

    def create_text_field(self):
        frame = tk.Frame(self.window, padx=8, pady=8)
        scrollbar = tk.Scrollbar(frame, width=14, borderwidth=0, highlightthickness=0, troughcolor='#ededed', activebackground='#3daee9', bg='#c4c4c4', highlightcolor='blue')
        self.text_field = tk.Text(frame, height=20, width=80)
        self.text_field.bind("<Button-3>", self.show_context_menu)
        self.text_field.bind("<Control-v>", self.paste_from_clipboard)
        self.text_field.bind("<Control-a>", self.select_all)
        self.text_field.bind("<Control-x>", self.cut_text)
        self.text_field.bind("<Control-c>", self.copy_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_field.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_field.yview)
        self.text_field.config(yscrollcommand=scrollbar.set)
        frame.pack(fill=tk.BOTH, expand=True)

    def create_save_button(self):
        button_save = tk.Button(self.window, text="Save..", command=self.save_text)
        button_save.pack(fill=tk.X, padx=8, pady=(0, 8))

    def show_context_menu(self, event):
        context_menu = tk.Menu(self.text_field, tearoff=0)
        context_menu.add_command(label="Cut", command=self.cut_text)
        context_menu.add_command(label="Copy", command=self.copy_text)
        context_menu.add_command(label="Paste", command=self.paste_from_clipboard)
        context_menu.add_command(label="Select All", command=self.select_all)
        context_menu.tk_popup(event.x_root, event.y_root)

    def cut_text(self, event=None):
        try:
            self.text_field.event_generate("<<Cut>>")
            return "break"
        except:
            pass

    def copy_text(self, event=None):
        try:
            self.text_field.event_generate("<<Copy>>")
            return "break"
        except:
            pass
        
    def paste_from_clipboard(self, event=None):
        try:
            has_selected_text = self.text_field.tag_ranges(tk.SEL)
            if has_selected_text:
                self.text_field.delete(tk.SEL_FIRST, tk.SEL_LAST)
            # content = self.window.clipboard_get()
            # self.text_field.insert(tk.INSERT, content)
            self.text_field.event_generate("<<Paste>>")

        except:
            pass

        # try:
        #     has_selected_text = self.root.entry.selection_present()
        #     if has_selected_text:
        #         self.root.entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
        #     # content = self.root.clipboard_get()
        #     # self.root.entry.insert(tk.INSERT, content)
        #     self.root.entry.event_generate("<<Paste>>")
        #     print('paste')
        # except:
        # #     print('no paste')
        #     pass


    def select_all(self, event=None):
        try:
            self.text_field.tag_add(tk.SEL, "1.0", tk.END)
            self.text_field.mark_set(tk.INSERT, "1.0")
            self.text_field.see(tk.INSERT)
            return "break"
        except:
            pass
        
    def save_text(self):
        text = self.text_field.get("1.0", tk.END)
        path = filedialog.asksaveasfilename()
        if path:
            try:
                with open(path, "w") as file:
                    file.write(text)
                messagebox.showinfo("Success", "Text saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def set_text(self, text):
        self.text_field.delete("1.0", tk.END)
        self.text_field.insert(tk.INSERT, text)

    def run(self):
        self.window.mainloop()


# Usage example
# if __name__ == "__main__":
#     app = TextEditorApp()
#       # Example of starting it up with some specific text
#     app.set_text("This is a sample text.")
#     app.run()