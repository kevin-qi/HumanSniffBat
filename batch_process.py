import luigi
import os
import getopt, sys
import luigi.tools.deps_tree as deps_tree
from process_b151 import *
from process_b149f import *

if __name__ == '__main__':
    options, args = getopt.getopt(sys.argv[1:], "", ['local-scheduler', 'data-path='])
    options = dict(options)

    data_path = options['--data-path']
    assert os.path.isdir(data_path), "{} is not a valid directory".format(data_path)

    sessions = os.listdir(data_path);
    session_paths = [os.path.join(data_path, sess) for sess in sessions]
    print(session_paths)

    tasks = [[B151CheckDataIntegrity(sess), # B151
      B151ExtractCameraData(sess),
      B151ExtractEphysData(sess),
      B151DownsampleEphysData(sess),
      B151ExtractArduinoData(sess),
      B151ExtractMotuData(sess),
      B151EphysPowerSpectrum(sess),
      B151BottomCameraDLC(sess),
      B151KilosortEphysData(sess),
      B149fEphysPowerSpectrum(sess),
      B149fExtractEphysData(sess),  # B149f
      B149fDownsampleEphysData(sess),
      B149fExtractCiholasData(sess),
      B149fExtractCortexData(sess),
      B149fKilosortEphysData(sess)] for sess in session_paths]

    tasks = sum(tasks, [])


    print(tasks)
    print("Executing",len(tasks),"tasks across",len(sessions),'days of data')

    luigi.build(tasks, workers=8,log_level='INFO')

    #luigi.build([B149fDownsampleEphysData(data_path),B149fKilosortEphysData(data_path)])

    """
    luigi.build([B149fExtractEphysData(data_path),  # B149f
                 B149fDownsampleEphysData(data_path),
                 B149fExtractCortexData(data_path),
                 B151ExtractEphysData(data_path),
                 B151ExtractMotuData(data_path),
                 B151DownsampleEphysData(data_path),
                 B149fExtractCiholasData(data_path)],
                 workers=4,
                 log_level='INFO'))

    luigi.build([B151CheckDataIntegrity(data_path), # B151
                  B151ExtractCameraData(data_path),
                  B151ExtractEphysData(data_path),
                  B151DownsampleEphysData(data_path),
                  B151ExtractArduinoData(data_path),
                  B151ExtractMotuData(data_path),
                  B151EphysPowerSpectrum(data_path),
                  B151BottomCameraDLC(data_path),
                  B151KilosortEphysData(data_path),
                  B149fEphysPowerSpectrum(data_path),
                  B149fExtractEphysData(data_path),  # B149f
                  B149fDownsampleEphysData(data_path),
                  B149fExtractCiholasData(data_path),
                  B149fExtractCortexData(data_path),
                  B149fKilosortEphysData(data_path)],
                  workers=8,
                  log_level='INFO')"""
