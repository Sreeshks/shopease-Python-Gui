import tkinter as tk
from .data import DataHandler
from .ui import ShopEaseUI

def main():
    root = tk.Tk()
    data_handler = DataHandler()
    app = ShopEaseUI(root, data_handler)
    root.mainloop()

if __name__ == "__main__":
    main()