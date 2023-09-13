import tkinter as tk
import webbrowser

class UiBrowserLinkWindow:
    def __init__(self, title, description, link):
        self.root = tk.Tk()
        self.root.title(title)

        self.description_label = tk.Label(self.root, text=description, justify="left")
        self.description_label.pack(padx=10, pady=10, anchor='w')

        self.link = link

        self.open_button = tk.Button(self.root, text="Open Link In Browser", command=self.open_link)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.root.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Center the window on the screen
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"+{x}+{y}")

    def open_link(self):
        webbrowser.open(self.link)
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    title = "Give some"
    description_text = "Click the 'Open Link' button to visit a website. \n\nwww.something"
    link_url = "https://www.example.com"

    link_window = UiBrowserLinkWindow(title, description_text, link_url)
    link_window.run()
