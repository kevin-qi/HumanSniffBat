import luigi
import os
from pathlib import Path
#import h5py
import json
import sys
import numpy as np
#import hdf5storage
import re
import gc
from distutils import dir_util
import getopt, sys
import luigi.tools.deps_tree as deps_tree
from HumanBat import process_motu, process_arduino, process_ephys, process_video, b151_tests

class B151ExtractMotuData(luigi.Task):
    data_path = luigi.Parameter()
    print(data_path)


    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def output(self):
        self.out_path = os.path.join(os.path.join(self.data_path, 'b151/motu')).replace('raw','processed')
        Path(self.out_path).mkdir(parents=True, exist_ok=True)
        self.in_path = os.path.join(os.path.join(self.data_path, 'b151/motu'))

        return luigi.LocalTarget(os.path.join(self.out_path,'motu.npy'))

    def run(self):
        raw_motu_data = process_motu.load_motu_data(self.in_path)
        print(raw_motu_data.shape)
        fs = self.config['b151']['motu']['fs']

        motu_data, ttl_indices = process_motu.slice_valid_motu_data(raw_motu_data, fs)
        mat_data = {'motu': {'data': motu_data, 'ttl_indices': ttl_indices, 'fs': fs}}
        #hdf5storage.savemat(self.output().path, mat_data, format='7.3')
        np.save(self.output().path, mat_data)

class B151ExtractArduinoData(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def output(self):
        self.out_path = os.path.join(os.path.join(self.data_path, 'b151/arduino')).replace('raw','processed')
        Path(self.out_path).mkdir(parents=True, exist_ok=True)
        self.in_path = os.path.join(os.path.join(self.data_path, 'b151'))
        return luigi.LocalTarget(os.path.join(self.out_path,'arduino.npy'))

    def run(self):
        session_name = Path(self.data_path).name
        arduino_data = process_arduino.parse_b151_arduino_logs(os.path.join(self.in_path, '{}_logs.txt'.format(session_name)))

        arduino_data = {'arduino': arduino_data}
        #hdf5storage.savemat(self.output().path, arduino_data, format='7.3')
        np.save(self.output().path, arduino_data)

class B151ExtractEphysData(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def output(self):
        # Get logger directory path
        self.in_path = os.path.join(os.path.join(self.data_path, 'b151/ephys'))
        dirs = os.listdir(self.in_path)
        r = re.compile("(.*_\d\d)")
        logger_dirs = list(filter(r.match, dirs))
        assert len(logger_dirs) == 1, "There should only be 1 logger folder! Found {}".format(logger_dirs)
        self.in_path = os.path.join(self.in_path, logger_dirs[0])

        # Create output path
        self.out_path = os.path.dirname(self.in_path.replace('raw','processed'))
        Path(self.out_path).mkdir(parents=True, exist_ok=True)

        return luigi.LocalTarget(os.path.join(self.out_path,'extracted_data'))

    def run(self):
        fs = self.config['b151']['ephys']['fs']

        # Extract logger data
        process_ephys.extract(self.in_path)

        # Copy extracted_data/ to processed folder
        if(os.path.isdir(os.path.join(self.out_path, 'extracted_data'))):
            print("Overwriting existing {}".format(os.path.join(self.out_path, 'extracted_data')))
        dir_util.copy_tree(os.path.join(self.in_path, 'extracted_data'),self.output().path)

class B151ExtractCameraData(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def output(self):
        # Get camera data path
        self.in_path = os.path.join(os.path.join(self.data_path, 'b151/cameras'))

        # Create output path
        self.out_path = self.in_path.replace('raw','processed')

        return luigi.LocalTarget(self.out_path)

    def run(self):
        # Extract camera data
        room_name = 'b151'
        session_name = Path(self.data_path).name
        process_video.preprocess_raw_video(room_name, session_name, self.config)

class B151EphysNoiseTest(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)
        print(config)
    def requires(self):
        return B151ExtractEphysData(self.data_path)

    def output(self):
        p = os.path.join(os.path.join(self.data_path, 'b151/ephys/'))
        p = self.data_path.replace('raw','processed')

        self.in_path = os.path.join(p,'b151/ephys')
        self.out_path = os.path.join(p,'b151/tests/ephys_noise_test.jpg')

        Path(os.path.dirname(self.out_path)).mkdir(parents=True, exist_ok=True)

        return luigi.LocalTarget(self.out_path)

    def run(self):
        # Extract camera data
        res = b151_tests.test_ephys_noise(self.in_path, self.out_path)
        assert res == True, 'Ephys test failed, see {} for test result'.format(self.out_path)

class B151VisualizeSynchronyTest(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def requires(self):
        return (B151ExtractEphysData(self.data_path),\
                B151ExtractCameraData(self.data_path),\
                B151ExtractArduinoData(self.data_path),\
                B151ExtractMotuData(self.data_path))

    def output(self):
        p = os.path.join(os.path.join(self.data_path, 'b151')).replace('raw','processed')

        self.ephys_path = os.path.join(p,'ephys')
        self.motu_path = os.path.join(p,'motu/motu.npy')
        self.arduino_path = os.path.join(p,'arduino/arduino.npy')
        self.camera_path = os.path.join(p,'cameras/')
        self.out_path = os.path.join(p,'tests/visualize_synchrony.mp4')

        Path(os.path.dirname(self.out_path)).mkdir(parents=True, exist_ok=True)

        return luigi.LocalTarget(self.out_path)

    def run(self):
        # Visualize Synchrony
        res = b151_tests.visualize_synchrony(self.motu_path,self.arduino_path,self.ephys_path,self.camera_path,self.out_path,self.config)
        assert res == True, 'Visualize Synchrony test failed, see {} for test result'.format(self.out_path)

if __name__ == '__main__':
    options, args = getopt.getopt(sys.argv[1:], "", ['local-scheduler', 'data-path=', 'skip-completed='])
    options = dict(options)

    data_path = options['--data-path']
    assert os.path.isdir(data_path), "{} is not a valid directory".format(data_path)

    skip_completed = bool(options['--skip-completed'])
    assert type(skip_completed) == type(True), "{} is not a bool".format(skip_completed)
    print(deps_tree.print_tree(B151EphysNoiseTest(data_path)))
    luigi.build([B151ExtractCameraData(data_path),\
                 B151ExtractEphysData(data_path),\
                 B151ExtractArduinoData(data_path),\
                 B151ExtractMotuData(data_path),\
                 B151EphysNoiseTest(data_path),\
                 B151VisualizeSynchronyTest(data_path)],
                 workers=4,
                 log_level='INFO')