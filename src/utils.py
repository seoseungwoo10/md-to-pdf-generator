import os
import sys

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), relative_path)

def get_default_output_path(input_path):
    """Generate default output path based on input filename"""
    base, _ = os.path.splitext(input_path)
    return f"{base}.pdf"
