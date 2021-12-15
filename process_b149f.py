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
import pickle
from distutils import dir_util
import getopt, sys
import luigi.tools.deps_tree as deps_tree
from HumanBat import process_motu, process_arduino, process_ephys, process_video# b_tests

class B149fCheckDataIntegrity(luigi.Task):
    data_path = luigi.Parameter()
    task_complete = False

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def output(self):
        return None

    def complete(self):
        return True#self.task_complete

    def run(self):
        ephys_path = os.path.join(self.data_path, 'b149f/ephys')
        logger_dirs = os.listdir(ephys_path)

        assert len(logger_dirs) == 1, "Data Integrity Error: Multiple logger folders found in {}".ephys_path

        # EVENTLOG.CSV exists (extracted by EVENT_FILE_READER.EXE from NEURALYNX)
        assert os.path.exists(os.path.join(ephys_path, logger_dirs[0], 'EVENTLOG.CSV')), "Data Integrity Error: EVENTLOG.CSV not found. Did you remember to extract it?"

        # TODO: Check number of NEUR____.DAT files match expected number in EVENTLOG.CSV

        # Check arduino logs exist
        session_name = Path(self.data_path).name
        assert os.path.exists(os.path.join(self.data_path, 'b149f/{}_logs.txt'.format(session_name)))

        self.task_complete = True

class B149fExtractArduinoData(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def requires(self):
        return B149fCheckDataIntegrity(self.data_path)

    def output(self):
        self.out_path = os.path.join(os.path.join(self.data_path, 'b149f/arduino')).replace('raw','processed')
        Path(self.out_path).mkdir(parents=True, exist_ok=True)
        self.in_path = os.path.join(os.path.join(self.data_path, 'b149f'))
        return luigi.LocalTarget(os.path.join(self.out_path,'arduino.npy'))

    def run(self):
        session_name = Path(self.data_path).name
        arduino_data = process_arduino.parse_b149f_arduino_logs(os.path.join(self.in_path, '{}_logs.txt'.format(session_name)))

        arduino_data = {'arduino': arduino_data}
        #hdf5storage.savemat(self.output().path, arduino_data, format='7.3')
        np.save(self.output().path, arduino_data)

class B149fExtractEphysData(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    #def requires(self):
    #    return B149fCheckDataIntegrity(self.data_path)

    def output(self):
        # Get logger directory path
        self.in_path = os.path.join(os.path.join(self.data_path, 'b149f/ephys'))
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
        fs = self.config['b149f']['ephys']['fs']

        # Extract logger data
        process_ephys.extract(self.in_path)

        # Copy extracted_data/ to processed folder
        if(os.path.isdir(os.path.join(self.out_path, 'extracted_data'))):
            print("Overwriting existing {}".format(os.path.join(self.out_path, 'extracted_data')))
        dir_util.copy_tree(os.path.join(self.in_path, 'extracted_data'),self.output().path)

class B149fDownsampleEphysData(luigi.Task):
    data_path = luigi.Parameter()

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    def requires(self):
        return (B149fCheckDataIntegrity(self.data_path), B149fExtractEphysData(self.data_path))

    def output(self):
        # Get logger directory path
        self.in_path = os.path.join(os.path.join(self.data_path, 'b149f/ephys'))
        dirs = os.listdir(self.in_path)
        r = re.compile("(.*_\d\d)")
        logger_dirs = list(filter(r.match, dirs))
        assert len(logger_dirs) == 1, "There should only be 1 logger folder! Found {}".format(logger_dirs)
        self.in_path = os.path.join(self.in_path, logger_dirs[0])

        # Create output path
        self.out_path = os.path.dirname(self.in_path.replace('raw','processed'))
        Path(self.out_path).mkdir(parents=True, exist_ok=True)

        return luigi.LocalTarget(os.path.join(self.out_path,'ephys_ds.npy'))

    def run(self):
        fs = self.config['b149f']['ephys']['fs']

        # Extract logger data
        ephys_ds = process_ephys.load_extracted_data(os.path.join(self.out_path,'extracted_data'), fs, 10)
        np.save(self.output().path, ephys_ds, allow_pickle = True)


if __name__ == '__main__':
    options, args = getopt.getopt(sys.argv[1:], "", ['local-scheduler', 'data-path=', 'skip-completed='])
    options = dict(options)

    data_path = options['--data-path']
    assert os.path.isdir(data_path), "{} is not a valid directory".format(data_path)

    with open('./config/config.json', 'r') as f:
        config = json.load(f)

    #data_path = os.path.join(config['project_root'], data_path)

    skip_completed = bool(options['--skip-completed'])
    assert type(skip_completed) == type(True), "{} is not a bool".format(skip_completed)
    #print(deps_tree.print_tree(B149fEphysNoiseTest(data_path)))
    luigi.build([B149fExtractEphysData(data_path)],
                 workers=4,
                 log_level='WARNING')
