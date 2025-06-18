import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Any

# Define color scheme
COLORS = {
    "primary": "#2c3e50",
    "secondary": "#34495e",
    "accent": "#3498db",
    "background": "#ecf0f1",
    "text": "#2c3e50",
    "button_hover": "#2980b9",
    "success": "#27ae60",
    "error": "#e74c3c"
}

class EmailHandler:
    def __init__(self, root: tk.Tk, main_menu_callback):
        self.root = root
        self.main_menu_callback = main_menu_callback
        self.current_button_index = 0
        self.buttons = []

    def create_button(self, parent, text, command, width=20):
        """Create a styled button with hover effect"""
        btn = ttk.Button(parent, text=text, command=command, width=width)
        btn.pack(fill="x", pady=10, padx=20)
        self.buttons.append(btn)
        return btn

    def create_entry(self, parent, show=None):
        """Create a styled entry field with Enter key binding"""
        entry = ttk.Entry(parent, font=("Helvetica", 12), show=show)
        entry.pack(pady=5, padx=20, fill="x")
        return entry

    def send_mail_window(self):
        """Create window for sending mail."""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reset button list
        self.buttons = []
        self.current_button_index = 0

        ttk.Label(self.root, text="Contact Developer", style="Subtitle.TLabel").pack(pady=20)

        ttk.Label(self.root, text="Recipient's Email:", style="Subtitle.TLabel").pack(pady=5)
        recipient_entry = self.create_entry(self.root)

        ttk.Label(self.root, text="Subject:", style="Subtitle.TLabel").pack(pady=5)
        subject_entry = self.create_entry(self.root)

        ttk.Label(self.root, text="Message:", style="Subtitle.TLabel").pack(pady=5)
        message_text = scrolledtext.ScrolledText(self.root, height=5, font=("Helvetica", 10))
        message_text.pack(pady=5)

        def send():
            recipient = recipient_entry.get().strip()
            subject = subject_entry.get().strip()
            message = message_text.get(1.0, tk.END).strip()

            if not all([recipient, subject, message]):
                messagebox.showerror("Error", "All fields are required.")
                return

            # Simulate sending mail
            messagebox.showinfo("Success", "Mail sent successfully!")
            self.main_menu_callback()

        # Create buttons
        send_btn = self.create_button(self.root, "Send", send)
        back_btn = self.create_button(self.root, "Back", self.main_menu_callback)

        # Set initial focus
        recipient_entry.focus_set()

        def on_arrow_key(event):
            if event.keysym == "Up":
                self.current_button_index = (self.current_button_index - 1) % len(self.buttons)
                self.buttons[self.current_button_index].focus_set()
            elif event.keysym == "Down":
                self.current_button_index = (self.current_button_index + 1) % len(self.buttons)
                self.buttons[self.current_button_index].focus_set()
            elif event.keysym == "Return":
                self.buttons[self.current_button_index].invoke()

        # Bind arrow keys to all widgets
        for widget in [recipient_entry, subject_entry, message_text, send_btn, back_btn]:
            widget.bind("<Up>", on_arrow_key)
            widget.bind("<Down>", on_arrow_key)
            widget.bind("<Return>", on_arrow_key)

        # Bind tab key for navigation
        def on_tab(event):
            if event.state & 0x1:  # Shift is pressed
                self.current_button_index = (self.current_button_index - 1) % len(self.buttons)
            else:
                self.current_button_index = (self.current_button_index + 1) % len(self.buttons)
            self.buttons[self.current_button_index].focus_set()
            return "break"  # Prevent default tab behavior

        for widget in [recipient_entry, subject_entry, message_text, send_btn, back_btn]:
            widget.bind("<Tab>", on_tab)
            widget.bind("<Shift-Tab>", on_tab) 