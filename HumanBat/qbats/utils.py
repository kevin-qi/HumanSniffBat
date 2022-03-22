import numpy
import h5py
import hdf5storage
import matlab.engine


def savemat73(mat_data, fname):
    print(fname)
    hdf5storage.write(mat_data, filename=fname, store_python_metadata=False, matlab_compatible=True)

class PyMatlab():
    def __init__(self, path_to_add):
        # Start matlab engine
        self.eng = matlab.engine.start_matlab()

        # Add LoggerDataProcessing Path
        # Path is absolute
        print("Adding to matlab path:", path_to_add)
        generated_path = self.eng.genpath(path_to_add)
        self.eng.addpath(generated_path, nargout=0)
