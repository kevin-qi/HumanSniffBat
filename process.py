import luigi
import os
import getopt, sys
import luigi.tools.deps_tree as deps_tree
from process_b151 import *
from process_b149f import *

if __name__ == '__main__':
    options, args = getopt.getopt(sys.argv[1:], "", ['local-scheduler', 'data-path=', 'skip-completed='])
    options = dict(options)

    data_path = options['--data-path']
    assert os.path.isdir(data_path), "{} is not a valid directory".format(data_path)

    skip_completed = bool(options['--skip-completed'])
    assert type(skip_completed) == type(True), "{} is not a bool".format(skip_completed)
    print(deps_tree.print_tree(B151EphysNoiseTest(data_path)))
    #luigi.build([B151BottomCameraDLC(data_path)])
    """
    luigi.build([B149fExtractEphysData(data_path),  # B149f
                 B149fDownsampleEphysData(data_path),
                 B149fExtractCortexData(data_path),
                 B151ExtractEphysData(data_path),
                 B151ExtractMotuData(data_path),
                 B151DownsampleEphysData(data_path),
                 B149fExtractCiholasData(data_path)],
                 workers=4,
                 log_level='INFO')
    """
    luigi.build([B151CheckDataIntegrity(data_path),\ # B151
                 B151ExtractCameraData(data_path),\
                 B151ExtractEphysData(data_path),\
                 B151DownsampleEphysData(data_path),\
                 B151ExtractArduinoData(data_path),\
                 B151ExtractMotuData(data_path),\
                 B151EphysNoiseTest(data_path),\
                 B151VisualizeSynchronyTest(data_path),\
                 B151BottomCameraDLC(data_path),\
                 B149fExtractEphysData(data_path),\  # B149f
                 B149fDownsampleEphysData(data_path),\
                 B149fExtractCiholasData(data_path),\
                 B149fExtractCortexData(data_path)],
                 workers=4,
                 log_level='INFO')
