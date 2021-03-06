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
import pipeline.rclone_tasks as rclone_tasks
from utils.utils import PyMatlab

class ConcatAudio(luigi.Task):
    """
    Concatenate audio
    """
    bat_id = luigi.Parameter()
    date = luigi.Parameter() # YYMMDD
    data_path = luigi.Parameter()


    #server_path = luigi.Parameter() # Path to server root directory containing data from each day
    #local_path = luigi.Parameter() # Path to local root directory containing data from each day

    def requires(self):
        return [rclone_tasks.PullServerData(self.bat_id, self.date, self.data_path)]

    def output(self):
        self.in_path = os.path.join(self.data_path, 'audio')
        out_path = self.in_path.replace('raw', 'processed')
        Path(out_path).mkdir(parents=True, exist_ok=True)
        self.out_path = os.path.join(out_path,'1920', 'audioCh_1.mat')

        return luigi.LocalTarget(self.out_path)

    def run(self):
        SniffBatPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        pyMatlab = PyMatlab(SniffBatPath)
        print(SniffBatPath)
        print("Concatenating audio... ")
        pyMatlab.eng.SniffBat_parConcatAudio(self.in_path, nargout=0)
