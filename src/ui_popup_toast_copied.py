import os
import sys
import tkinter as tk

class UiPopupToastCopied:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Set window dimensions
        self.window_width = 300
        self.window_height = 80
        
        # Calculate initial position (top middle of the screen)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.x_position = (screen_width - self.window_width) // 2
        self.y_position = 0
        
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")
        
        # Set window background
        self.root.configure(bg="#262626")
        
        # Create a frame with a solid gray border
        self.frame = tk.Frame(self.root, bg="#262626", highlightbackground="gray", highlightthickness=2)
        self.frame.pack(fill='both', expand=True)
        
        label2 = tk.Label(self.frame, text="Copied To Clipboard", font=("Helvetica", 14), fg="white", bg="#262626", anchor="center")
        label2.pack(fill='both', pady=(26, 0))  # Use pady to control bottom margin
        
    def animate_fly_out(self):
        if self.y_position < -self.window_height:
            try:
                self.root.after_cancel(self.animation_id)
            except:
                pass
            self.close_window()
            return
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x_position}+{self.y_position}")
        self.y_position -= 10  # Change this value to control animation speed
        self.animation_id = self.root.after(10, self.animate_fly_out)
        
    def close_window(self):
        self.root.destroy()
        sys.exit(0)
        os._exit(0) 
        
    def start_animation(self):
        self.root.after(1400, self.animate_fly_out)
        self.root.mainloop()


# flying_window = UiPopupToastCopied()
# flying_window.start_animation()
