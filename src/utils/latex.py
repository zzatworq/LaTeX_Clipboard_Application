import re
import logging
import subprocess
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def check_latex():
    try:
        plt.figure()
        plt.text(0.5, 0.5, r'$\alpha$', fontsize=12, ha='center', va='center')
        plt.axis('off')
        plt.savefig('test_latex.png', format='png', dpi=100, bbox_inches='tight')
        plt.close()
        if os.path.exists('test_latex.png'):
            os.remove('test_latex.png')
        else:
            return False
        subprocess.run(["latex", "--version"], check=True, capture_output=True, text=True)
        subprocess.run(["dvipng", "--version"], check=True, capture_output=True, text=True)
        return True
    except Exception as e:
        logging.error(f"LaTeX check failed: {e}")
        return False

def find_latex_equations(text):
    if not text:
        return {'equations': [], 'matches': []}
    patterns = [
        (r'\\\[(.*?)\\\]', True),
        (r'\\\((.*?)\\\)', False),
        (r'\$\$(.*?)\$\$', True),
        (r'\$(.*?)\$', False),
        (r'\\begin\{equation\}(.*?)\\end\{equation\}', True)
    ]
    equations = []
    matches = []
    for pattern, is_display in patterns:
        for match in re.finditer(pattern, text, re.DOTALL):
            equation = match.group(1).strip()
            if equation:
                cleaned = equation.replace('\n', ' ').strip()
                equations.append(cleaned)
                matches.append({
                    'start': match.start(),
                    'end': match.end(),
                    'equation': cleaned,
                    'is_display': is_display,
                    'raw_match': match.group(0)
                })
    matches.sort(key=lambda x: x['start'])
    return {'equations': [m['equation'] for m in matches], 'matches': matches}