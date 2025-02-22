import os

def create_config_file():
    """Create the necessary config file for pyresparser"""
    config_content = """[nlp]
lang = en_core_web_sm
disabled = []
    
[skills]
# Add custom skills if needed
SKILLS_DB = []

[education]
# Add custom education terms if needed
EDUCATION = []

[titles]
# Add custom titles if needed
TITLES = []
"""
    
    # Get the pyresparser installation directory
    try:
        import pyresparser
        parser_dir = os.path.dirname(pyresparser.__file__)
        config_path = os.path.join(parser_dir, 'config.cfg')
        
        # Create the config file if it doesn't exist
        if not os.path.exists(config_path):
            with open(config_path, 'w') as f:
                f.write(config_content)
            print(f"Created config file at: {config_path}")
        else:
            # Update existing config file
            with open(config_path, 'w') as f:
                f.write(config_content)
            print(f"Updated config file at: {config_path}")
        
        return True
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False 