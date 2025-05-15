import ctypes
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
import tkinter as tk
from src.config.settings import LOGGING_CONFIG, RC_PARAMS
from src.gui.app_gui import LatexClipboardApp

rcParams.update(RC_PARAMS)

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

if __name__ == "__main__":
    root = tk.Tk()
    app = LatexClipboardApp(root)
    root.mainloop()