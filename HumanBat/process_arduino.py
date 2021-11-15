import os
import numpy as np
import re
from pathlib import Path

def parse_b151_arduino_logs(log_file_path):
    arduino_ttl = []
    arduino_state = []
    arduino_state_enter_ms = []
    arduino_state_exit_ms = []
    with open(log_file_path, 'r') as f:
        for line in f.readlines():
            ttl_ts_matches= re.findall('(\d*)!', line) # Match ttl timestamps
            if(not ttl_ts_matches == []):
                arduino_ttl += ttl_ts_matches

            state_enter_matches=re.search('(\w+)_ENTER:(\d+)|', line)
            if(state_enter_matches.group(1) != None):
                arduino_state.append(state_enter_matches.group(1))
                arduino_state_enter_ms.append(state_enter_matches.group(2))

            state_exit_matches=re.search('.*(\w+)_EXIT:(\d+)|', line)
            if(state_exit_matches.group(1) != None):
                arduino_state_exit_ms.append(state_exit_matches.group(2))
    arduino_ttl = np.array(arduino_ttl, dtype=np.uint64)
    arduino_state_enter_ms = np.array(arduino_state_enter_ms, dtype=np.int64) - arduino_ttl[0]
    arduino_state_exit_ms = np.array(arduino_state_exit_ms, dtype=np.int64) - arduino_ttl[0]
    arduino_ttl_ms = arduino_ttl - arduino_ttl[0]
    return {'ttl_ms':arduino_ttl_ms, 'state':arduino_state, 'state_enter_ms':arduino_state_enter_ms, 'state_exit_ms':arduino_state_exit_ms}
