import os
import yaml

class Config:
    def __init__(self):
        self.defaults = {
            'style': 'github',
            'font_size': 11,
            'page_size': 'A4',
            'toc': False,
            'recursive': False
        }

    def load(self, config_path=None):
        """Load configuration from file and merge with defaults"""
        config = self.defaults.copy()
        
        # Check for default config file if none provided
        if not config_path:
            default_config = os.path.join(os.getcwd(), '.md2pdf.yaml')
            if os.path.exists(default_config):
                config_path = default_config
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        config.update(file_config)
            except Exception as e:
                print(f"Warning: Failed to load config file: {e}")
                
        return config
