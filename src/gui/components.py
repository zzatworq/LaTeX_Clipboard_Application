import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

def create_settings_frame(parent, defaults, logger_enabled, validate_inputs):
    class SettingsFrame:
        def __init__(self):
            self.frame = ttk.LabelFrame(parent, text="Configuration", padding="5")
            self.frame.grid(row=0, column=0, sticky="ew", pady=5)
            self.frame.columnconfigure(1, weight=1)

            menu_font = tkfont.Font(family="Arial", size=12)
            self.mode_var = tk.StringVar(value=defaults["mode"])
            self.color_var = tk.StringVar(value=defaults["text_color"])
            self.font_size_var = tk.StringVar(value=defaults["font_size"])
            self.dpi_var = tk.StringVar(value=defaults["dpi"])
            self.only_images_var = tk.BooleanVar(value=defaults["only_images"])

            ttk.Label(self.frame, text="Render Mode:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
            self.mode_menu = ttk.OptionMenu(self.frame, self.mode_var, defaults["mode"], "Matplotlib", "Standalone")
            self.mode_menu["menu"].configure(font=menu_font)
            self.mode_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            ttk.Label(self.frame, text="Text Color:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
            self.color_menu = ttk.OptionMenu(self.frame, self.color_var, defaults["text_color"], "white", "black", "red", "blue", "green")
            self.color_menu["menu"].configure(font=menu_font)
            self.color_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

            ttk.Label(self.frame, text="Font Size:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
            self.font_size_spin = ttk.Spinbox(self.frame, from_=10, to=50, width=10, textvariable=self.font_size_var)
            self.font_size_spin.grid(row=2, column=1, padx=5, pady=5, sticky="w")

            ttk.Label(self.frame, text="DPI:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
            self.dpi_spin = ttk.Spinbox(self.frame, from_=100, to=600, width=10, textvariable=self.dpi_var)
            self.dpi_spin.grid(row=3, column=1, padx=5, pady=5, sticky="w")

            self.only_images_check = ttk.Checkbutton(self.frame, text="Only Images", variable=self.only_images_var)
            self.only_images_check.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

            self.logger_check = ttk.Checkbutton(self.frame, text="Enable Logging", variable=logger_enabled)
            self.logger_check.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    return SettingsFrame()

def create_actions_frame(parent, toggle_monitoring, test_render, save_as_docx, open_defaults_dialog):
    class ActionsFrame:
        def __init__(self):
            self.frame = ttk.LabelFrame(parent, text="Actions", padding="5")
            self.frame.grid(row=1, column=0, sticky="ew", pady=5)

            self.toggle_button = ttk.Button(self.frame, text="Start Monitoring", command=toggle_monitoring)
            self.toggle_button.grid(row=0, column=0, padx=5, pady=5)

            self.test_button = ttk.Button(self.frame, text="Test Render", command=test_render)
            self.test_button.grid(row=0, column=1, padx=5, pady=5)

            self.save_button = ttk.Button(self.frame, text="Save as DOCX", command=save_as_docx)
            self.save_button.grid(row=0, column=2, padx=5, pady=5)

            self.defaults_button = ttk.Button(self.frame, text="Defaults", command=open_defaults_dialog)
            self.defaults_button.grid(row=0, column=3, padx=5, pady=5)

    return ActionsFrame()

def create_io_frame(parent, render_input_text):
    class IOFrame:
        def __init__(self):
            self.frame = ttk.LabelFrame(parent, text="Input & Output", padding="5")
            self.frame.grid(row=2, column=0, sticky="nsew", pady=5)
            self.frame.columnconfigure(0, weight=1)
            self.frame.rowconfigure(1, weight=1)

            ttk.Label(self.frame, text="Input Text:").grid(row=0, column=0, padx=5, pady=5, sticky="nw")
            self.text_input = tk.Text(self.frame, height=5, width=50, font=("Arial", 12))
            self.text_input.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

            self.render_button = ttk.Button(self.frame, text="Render Input", command=render_input_text)
            self.render_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

            ttk.Label(self.frame, text="Note: White text may be invisible on white backgrounds.", foreground="red").grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.status_var = tk.StringVar(value="Stopped")
            ttk.Label(self.frame, textvariable=self.status_var, foreground="red").grid(row=4, column=0, padx=5, pady=5, sticky="w")

    io = IOFrame()
    return io.frame, io.text_input, io.status_var