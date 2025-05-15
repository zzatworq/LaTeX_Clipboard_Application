import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
import logging
import subprocess
import os
import tempfile

def image_to_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()

def is_image_empty(image):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    img_array = np.array(image)
    return np.sum(img_array[:, :, 3] > 0) < 100

def render_latex_to_image(latex_string, text_color, font_size, dpi, mode="Matplotlib"):
    return render_latex_matplotlib(latex_string, text_color, font_size, dpi) if mode == "Matplotlib" else render_latex_standalone(latex_string, text_color, font_size, dpi)

def render_latex_matplotlib(latex_string, text_color, font_size, dpi):
    try:
        scaled_font_size = font_size * (dpi / 100)
        fig = plt.figure(figsize=(12, 3), dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_axis_off()
        ax.text(0.5, 0.5, f"${latex_string}$", fontsize=scaled_font_size, color=text_color, ha='center', va='center', transform=ax.transAxes)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=dpi, transparent=True, bbox_inches='tight', pad_inches=0.05)
        plt.close(fig)
        buffer.seek(0)
        img = Image.open(buffer).convert("RGBA")
        bbox = img.getbbox()
        if not bbox:
            return None
        left, top, right, bottom = bbox
        padding = max(5, dpi // 20)
        img = img.crop((max(0, left - padding), max(0, top - padding), min(img.width, right + padding), min(img.height, bottom + padding)))
        if img.width > 1800 or img.height > 600:
            aspect = img.width / img.height
            new_width = 1800 if img.width > 1800 else int(aspect * 600)
            new_height = 600 if img.height > 600 else int(1800 / aspect)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        return None if is_image_empty(img) else img
    except Exception as e:
        logging.error(f"Matplotlib render failed: {e}")
        return None

def render_latex_standalone(latex_string, text_color, font_size, dpi):
    tex_template = r"""
    \documentclass[preview]{standalone}
    \usepackage{amsmath}
    \usepackage{xcolor}
    \begin{document}
    \fontsize{%dpt}{%dpt}\selectfont
    \color{%s}
    $%s$
    \end{document}
    """
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_path = os.path.join(temp_dir, "temp.tex")
            dvi_path = os.path.join(temp_dir, "temp.dvi")
            png_path = os.path.join(temp_dir, "temp.png")
            scaled_font_size = int(font_size * (dpi / 100))
            with open(tex_path, 'w', encoding='utf-8') as f:
                f.write(tex_template % (scaled_font_size, int(scaled_font_size * 1.2), text_color, latex_string))
            subprocess.run(["latex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_path], check=True, capture_output=True, text=True)
            subprocess.run(["dvipng", "-D", str(dpi), "-T", "tight", "-bg", "Transparent", "-o", png_path, dvi_path], check=True, capture_output=True, text=True)
            img = Image.open(png_path).convert("RGBA")
            bbox = img.getbbox()
            if not bbox:
                return None
            left, top, right, bottom = bbox
            padding = max(5, dpi // 20)
            img = img.crop((max(0, left - padding), max(0, top - padding), min(img.width, right + padding), min(img.height, bottom + padding)))
            if img.width > 1800 or img.height > 600:
                aspect = img.width / img.height
                new_width = 1800 if img.width > 1800 else int(aspect * 600)
                new_height = 600 if img.height > 600 else int(1800 / aspect)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            return None if is_image_empty(img) else img
    except Exception as e:
        logging.error(f"Standalone render failed: {e}")
        return None