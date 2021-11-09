import os
from pathlib import Path
import json


def main():
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

if __name__ == '__main__':
	main()