import tkinter as tk
from PIL import Image, ImageTk
import os


class ImageDisplayFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.image_label = tk.Label(self)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        self.bind("<Configure>", self.on_frame_resize)

    def on_frame_resize(self, event):
        if hasattr(self, 'image_path'):
            self.display_image(self.image_path)

    def display_image(self, fullpath):
        try:
            # Check file size
            file_size = os.path.getsize(fullpath)
            if file_size > 10 * 1024 * 1024:  # 10 MB in bytes
                raise ValueError("Image file is too large")

            # Get the current size of the frame
            frame_width = self.winfo_width()
            frame_height = self.winfo_height()

            # Load and resize the image
            image = Image.open(fullpath)
            image.thumbnail((frame_width, frame_height))

            # Create a PhotoImage object
            tk_image = ImageTk.PhotoImage(image)

            # Display the image
            self.image_label.configure(image=tk_image)
            self.image_label.image = tk_image  # Save a reference to avoid garbage collection

            self.image_path = fullpath  # Save the image path for future reference
            self.show()
        except Exception as e:
            print(f"Error displaying image: {str(e)}")

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack(padx=2, pady=2, fill=tk.BOTH, expand=True)