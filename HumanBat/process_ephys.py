import matlab.engine
import io
import sys
import os
import pathlib

def extract(data_path):
	"""
	Python wrapper for extract_logger_data matlab script from LoggerDataProcessing written by Julie.

	Parameters
	----------
	data_path : string
		Path to logger data (directory should contain the data from logger SD card)
	"""
	assert os.path.exists(data_path), "{} does not exist!".format(data_path)

	folder_name = pathlib.PurePath(data_path).name
	assert folder_name[-2:].isdigit(), "{} must end in the logger number (e.g. *_13)".format(folder_name)

	assert os.path.exists(os.path.join(data_path, 'EVENTLOG.csv')), 'EVENTLOG.csv does not exist in {}, did you extract it using EVENT_FILE_READER.exe?'.format(data_path)

	# Start matlab engine
	eng = matlab.engine.start_matlab()

	# Add LoggerDataProcessing Path
	# Path is absolute
	LoggerDataProcessingPath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'LoggerDataProcessing')
	LoggerDataProcessingPath = eng.genpath(LoggerDataProcessingPath)

	matlab_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), data_path)

	eng.addpath(LoggerDataProcessingPath, nargout=0)

	print("Running extraction script... ")
	eng.extract_logger_data(matlab_path,'Diary',False,nargout=0)

	print("Extraction complete!")
