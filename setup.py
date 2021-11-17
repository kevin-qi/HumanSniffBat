import os
from pathlib import Path
import json
from setuptools import setup, find_packages

setup(name='HumanBat', version='1.0', packages=find_packages())

#setup(name='humanbat', version='1.0', py_modules=['utils/extract_logger_data.py', 'utils/preprocess_video.py'])

# Get project root
project_root = str(Path(__file__).parent.resolve())

# Read configuration file
with open('config/config.json', 'r') as f:
    config = json.load(f)

# Configure project root
config['project_root'] = project_root
print("Configured project root")

# Save to configuration file
with open('config.json', 'w') as f:
    config = json.dump(config, f)

print("Project setup successful!")
