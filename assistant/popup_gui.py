import tkinter as tk
from datetime import datetime

class SaraPopup:
    def __init__(self):
        self.root = None
        self.is_open = False
        self.response_label = None
        self.base_height = 200
        self.max_height = 800
    
    def show_popup(self):
        """Show auto-resizing popup interface"""
        self.close_popup()
        
        self.root = tk.Tk()
        self.root.title("Sara AI")
        self.root.attributes('-topmost', True)
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(True, True)  # Allow resizing
        
        # Initial window size - wider to accommodate text better
        window_width = 500
        window_height = self.base_height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 3
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Main frame
        frame = tk.Frame(self.root, bg='#1a1a1a')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            frame,
            text="🤖 Sara AI Assistant",
            font=('Arial', 14, 'bold'),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        title_label.pack(pady=(0, 15))
        
        # Response label - auto-wrapping
        self.response_label = tk.Label(
            frame,
            text="Hello! How can I help you?",
            font=('Arial', 11),
            fg='#ffffff',
            bg='#1a1a1a',
            wraplength=460,  # Auto-wrap text
            justify=tk.LEFT,
            anchor='nw'
        )
        self.response_label.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        status_frame = tk.Frame(frame, bg='#1a1a1a')
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        status_label = tk.Label(
            status_frame,
            text="● Listening",
            font=('Arial', 9),
            fg='#00ff88',
            bg='#1a1a1a'
        )
        status_label.pack(side='left')
        
        resize_label = tk.Label(
            status_frame,
            text="↕ Drag corner to resize",
            font=('Arial', 8),
            fg='#666666',
            bg='#1a1a1a'
        )
        resize_label.pack(side='right')
        
        self.is_open = True
        print("🪟 Auto-resizing popup opened")
        
        self.root.mainloop()
    
    def update_response(self, response_text):
        """Update the popup with response and auto-resize"""
        if self.root and self.response_label:
            try:
                self.response_label.config(text=response_text)
                
                # Auto-adjust window height based on content
                self._auto_resize_window(response_text)
                
                self.root.update()
            except Exception as e:
                print(f"⚠️ Error updating popup: {e}")
    
    def _auto_resize_window(self, text):
        """Automatically resize window based on text content"""
        try:
            # Calculate lines and approximate height needed
            lines = text.count('\n') + 1
            base_line_height = 20  # pixels per line
            min_height = self.base_height
            max_height = self.max_height
            
            # Calculate required height
            required_height = min_height + (lines * base_line_height)
            
            # Add extra height for long lines that wrap
            words_per_line = 15  # Average words per line before wrapping
            total_words = len(text.split())
            wrapped_lines = max(0, (total_words // words_per_line) - lines)
            required_height += wrapped_lines * base_line_height
            
            # Limit height to maximum
            new_height = min(max(required_height, min_height), max_height)
            
            # Get current width and position
            current_width = self.root.winfo_width()
            current_x = self.root.winfo_x()
            current_y = self.root.winfo_y()
            
            # Update window geometry
            self.root.geometry(f"{current_width}x{new_height}+{current_x}+{current_y}")
            
        except Exception as e:
            print(f"⚠️ Error auto-resizing: {e}")
    
    def minimize_popup(self):
        """Minimize the popup window"""
        if self.root and self.is_open:
            try:
                self.root.iconify()  # Minimize to taskbar
                print("🪟 Popup minimized")
            except Exception as e:
                print(f"⚠️ Error minimizing popup: {e}")
    
    def close_popup(self):
        """Close popup"""
        if self.root:
            try:
                self.root.destroy()
                self.is_open = False
                print("🪟 Popup closed")
            except:
                pass
            self.root = None