import os
import subprocess
import datetime

SERVER_PATH = '/run/user/1000/gvfs/afp-volume:host=Server2.local,user=KevinQi,volume=server_home/'
SERVER_PATH = os.path.join(SERVER_PATH, 'users/KevinQi/HumanBat/14592')

SOURCE_PATH = '/home/batlab/Desktop/HumanBat/data/14592'

currentDT = datetime.datetime.now()
log_time = currentDT.strftime("%y%m%d_%H_%M_%S")
print (log_time)
LOG_DIR = '/home/batlab/Desktop/HumanBat/rclone_logs'
LOG_PATH_CHECK = os.path.join(LOG_DIR, 'CHECK_{}.log'.format(log_time))
LOG_PATH_COPY = os.path.join(LOG_DIR, 'COPY_{}.log'.format(log_time))

RCLONE_CHECK_CMD_EXAMPLE = 'rclone check . /run/user/1000/gvfs/afp-volume:host=Server2.local,user=KevinQi,volume=server_home/users/KevinQi/HumanBat/14592 --one-way --size-only'
RCLONE_COPY_CMD_EXAMPLE = 'rclone copy . /run/user/1000/gvfs/afp-volume:host=Server2.local,user=KevinQi,volume=server_home/users/KevinQi/HumanBat/14592 --size-only'


def rclone_check():
    res = subprocess.run(['rclone', 'check', SOURCE_PATH, SERVER_PATH, '--size-only', '--one-way', '--log-file={}'.format(LOG_PATH_CHECK)])
    print(res)
    if(res.returncode):
        print("rclone CHECK command SUCCESS!")
        return 1
    else:
        print("rclone CHECK command FAILED!")
        print(res)
        return 0

def rclone_copy():
    res = subprocess.run(['rclone', 'copy', SOURCE_PATH, SERVER_PATH,'--size-only', '--transfers=16', '--checkers=4'])
    print(res)
    if(res.returncode):
        print("rclone COPY command SUCCESS!")
        return 1
    else:
        print("rclone COPY command FAILED!")
        print(res)
        return 0

#rclone_check()
rclone_copy()
