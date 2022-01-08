import deeplabcut

project_config_path = 'dlc_projects/B151_211116_IMPLANT_BOTTOM-Madeleine-2021-11-22/config.yaml'

deeplabcut.analyze_videos(project_config_path, 'dlc_projects/B151_211116_IMPLANT_BOTTOM-Madeleine-2021-11-22/test/211116_IMPLANT_BOTTOM_000.mp4', videotype='.mp4')
