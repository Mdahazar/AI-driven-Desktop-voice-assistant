import tkinter as tk
from tkinter import ttk
import threading
from utils import get_greeting

class PopupManager:
    def __init__(self):
        self.root = None
        
    def show_greeting_popup(self, greeting):
        """Show the greeting popup in a separate thread"""
        popup_thread = threading.Thread(target=self._create_popup, args=(greeting,))
        popup_thread.daemon = True
        popup_thread.start()
    
    def _create_popup(self, greeting):
        """Create and display the popup window"""
        self.root = tk.Tk()
        self.root.title("Sara Assistant")
        
        # Set window properties
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.configure(bg='#2c3e50')
        
        # Make window always on top
        self.root.attributes('-topmost', True)
        
        # Center the window
        self._center_window(300, 200)
        
        # Create content
        self._create_widgets(greeting)
        
        # Auto-close after 10 seconds
        self.root.after(10000, self.root.destroy)
        
        # Start the GUI loop
        self.root.mainloop()
    
    def _center_window(self, width, height):
        """Center the window on screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_widgets(self, greeting):
        """Create popup widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Greeting label
        greeting_label = ttk.Label(
            main_frame, 
            text=greeting, 
            font=('Arial', 14, 'bold'),
            foreground='#3498db'
        )
        greeting_label.pack(pady=10)
        
        # Message label
        message_label = ttk.Label(
            main_frame,
            text="How can I help you?",
            font=('Arial', 11),
            foreground='#ecf0f1'
        )
        message_label.pack(pady=5)
        
        # Sara label
        sara_label = ttk.Label(
            main_frame,
            text="🤖 Sara AI Assistant",
            font=('Arial', 10, 'italic'),
            foreground='#bdc3c7'
        )
        sara_label.pack(pady=15)
        
        # Close button
        close_button = ttk.Button(
            main_frame,
            text="Close",
            command=self.root.destroy
        )
        close_button.pack(pady=10)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#2c3e50')
        style.configure('TLabel', background='#2c3e50')
        style.configure('TButton', background='#3498db')