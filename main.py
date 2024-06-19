import tkinter as tk
from tkinter import messagebox
from login import *

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()