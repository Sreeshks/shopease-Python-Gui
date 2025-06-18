import re
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

def validate_username(username: str) -> bool:
    """Validate username format."""
    return bool(username and re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def validate_password(password: str) -> bool:
    """Validate password format."""
    return len(password) >= 6

def show_tooltip(widget, text):
    """Show tooltip on hover."""
    tooltip = None

    def enter(event):
        nonlocal tooltip
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def leave(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)