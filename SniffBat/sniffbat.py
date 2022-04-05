import luigi
import os
import getopt, sys
#import luigi.tools.deps_tree as deps_tree
from pipeline.rclone_tasks import *
from pipeline.audio_tasks import *

if __name__ == '__main__':

    options, args = getopt.getopt(sys.argv[1:], "", ['local-scheduler', 'bat-id=', 'date='])
    options = dict(options)

    bat_id = options['--bat-id']
    date = options['--date']

    #data_path = options['--data-path']
    #assert os.path.isdir(data_path), "{} is not a valid directory".format(data_path)

    #skip_completed = bool(options['--skip-completed'])
    #assert type(skip_completed) == type(True), "{} is not a bool".format(skip_completed)

    local_path = './data/{}/raw/{}'.format(bat_id, date)
    server_path = ''

    #luigi.build([B149fDownsampleEphysData(data_path),B149fKilosortEphysData(data_path)])
    data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'data/{}/raw/{}'.format(bat_id, date))

    luigi.build([PullServerData(bat_id, date, data_path),
                 ConcatAudio(bat_id, date, data_path),
                 PushServerData(bat_id, date, data_path)],
                  workers=8,
                  log_level='INFO')

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
