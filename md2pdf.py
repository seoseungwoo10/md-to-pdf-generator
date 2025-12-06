import multiprocessing
from src.cli import cli

if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    # Set FONTCONFIG_FILE for WeasyPrint/Fontconfig
    import os
    import sys
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
        os.environ['FONTCONFIG_FILE'] = os.path.join(base_path, 'fonts.conf')
        
    cli()
