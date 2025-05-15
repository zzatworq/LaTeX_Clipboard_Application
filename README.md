LaTeX Clipboard Monitor
A Python app that monitors the clipboard for LaTeX equations, renders them as images (using Matplotlib or standalone LaTeX), and copies them as HTML. It supports saving to .docx files and offers a Tkinter GUI for customization.
Features

Monitors clipboard for LaTeX equations.
Renders via Matplotlib or standalone LaTeX (requires MiKTeX).
Customizes font size (10–50), DPI (100–600), text color, and image-only output.
Toggles logging to cache-and-logs/latex_clipboard.log.
Saves rendered equations as .docx.
Tests rendering with a predefined string.
Saves default settings to configs/defaults.json.

Prerequisites

Python 3.8+
MiKTeX (with latex and dvipng in PATH)
Dependencies: matplotlib, Pillow, pywin32, python-docx

Installation

Clone the repo:git clone <repository-url>
cd latex-clipboard-monitor


Set up virtual environment:python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Run:python main.py



Usage

Launch: Run run.bat or python main.py.
Configure: Set render mode, color, font size, DPI, and logging in the GUI.
Monitor: Click "Start Monitoring" to render clipboard LaTeX equations.
Manual Input: Enter LaTeX in the text box and click "Render Input".
Test: Click "Test Render" for a sample string.
Save: Click "Save as DOCX" to export.
Defaults: Set defaults in the "Defaults" dialog.

Project Structure
project_root/
├── main.py
├── requirements.txt
├── run.bat
├── src/
│   ├── gui/
│   │   ├── app_gui.py
│   │   └── components.py
│   ├── utils/
│   │   ├── clipboard.py
│   │   ├── image.py
│   │   └── latex.py
│   ├── config/
│   │   └── settings.py
│   └── templates/
│       └── test_string.py
└── cache-and-logs/
    └── latex_clipboard.log

Troubleshooting

LaTeX Not Found: Ensure MiKTeX is installed and latex/dvipng are in PATH.
Dependencies: Run pip install -r requirements.txt.
Rendering: Verify LaTeX syntax or switch render modes.

License
MIT License (see LICENSE if included).
