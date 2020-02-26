import subprocess
import time
import logging
import os
import shutil
from os import path


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
RUN_PATH = path.dirname(path.abspath(__file__)) + "/"


def process(chunk):
    file_name = "chunk" + str(chunk) + ".flac"
    shutil.move(RUN_PATH + "raw/" + file_name, RUN_PATH + "processed/" + file_name)


logging.info("Starting audio capture.")
subprocess.call(RUN_PATH + "start_capture.sh")


index = 0
for i in range(15):
    
    files_cnt = len(os.listdir(RUN_PATH + "raw"))
    
    if files_cnt > 0:
        process(index)
        index += 1
    time.sleep(.5)

subprocess.call(RUN_PATH + 'stop_capture.sh')
