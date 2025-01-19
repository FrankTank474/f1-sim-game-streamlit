import os

def get_css():
    # Get the directory where styles.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level and into the styles directory
    css_path = os.path.join(current_dir, '..', 'styles', 'main.css')
    
    try:
        with open(css_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: CSS file not found at {css_path}")
        return ""