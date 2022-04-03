import os
from pathlib import Path
import json
from setuptools import setup, find_packages

def input_dir(msg):
    is_good = False
    while(not is_good):
        try:
            local_src = input(msg)

            print("\nProvided local_src contains the following directories:\n", os.listdir(local_src))
            reply = input('\nDoes this local path look correct?(y/n): ').lower().strip()
            print(reply)
            if(reply == ''):
                is_good = False
            elif reply == 'y':
                is_good = True
            elif reply == 'n':
                is_good = False

        except FileNotFoundError:
            print("{} is not a valid directory".format(local_src))
            is_good = False

    return local_src

#setup(name='humanbat', version='1.0', py_modules=['utils/extract_logger_data.py', 'utils/preprocess_video.py'])
"""
# Configure SniffBat Luigi
print("\n----------------------")
print("SniffBat Configuration")
print("----------------------")

default_luigi_config = {'local_data_path':'','remote_data_path':''}

local_SniffBat_src = input_dir('Enter LOCAL absolute path to data/ folder for SniffBat:\n')
remote_SniffBat_src = input_dir('Enter SERVER absolute path to data/ folder for SniffBat:\n')
# Read configuration file
with open('SniffBat/pipeline/config.json', 'w+') as f:
    config = default_luigi_config
    config['local_data_path'] = local_SniffBat_src
    config['remote_data_path'] = remote_SniffBat_src
    json.dump(default_luigi_config, f)

print('')
print("\n----------------------")
print("HumanBat Configuration")
print("----------------------")

local_HumanBat_src = input_dir('Enter LOCAL absolute path to data/ folder for HumanBat:\n')
remote_HumanBat_src = input_dir('Enter SERVER absolute path to data/ folder for HumanBat:\n')
# Read configuration file
with open('HumanBat/pipeline/config.json', 'w+') as f:
    config = default_luigi_config
    config['local_data_path'] = local_HumanBat_src
    config['remote_data_path'] = remote_HumanBat_src
    json.dump(default_luigi_config, f)
"""

setup(name='HumanSniffBat', version='1.0', packages=find_packages())




"""
# Get project root
project_root = str(Path(__file__).parent.resolve())

# Read configuration file
with open('config/config.json', 'r') as f:
    config = json.load(f)

# Configure project root
config['project_root'] = project_root
print("Configured project root: {}".format(project_root))

# Save to configuration file
with open('config/config.json', 'w') as f:
    config = json.dump(config, f)"""

print("Project setup successful!")
