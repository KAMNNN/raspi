import subprocess
import time
import logging
import os
from os import path

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

RUN_PATH = path.dirname(path.abspath(__file__)) + "/"

logging.info("Starting audio capture.")

start = time.time()
subprocess.call(RUN_PATH + 'start_capture.sh')

for i in range(60):
    files_cnt = len(os.listdir(RUN_PATH + "raw"))
    logging.debug("Check " + str(i) + " " + str(files_cnt))
    time.sleep(1)

subprocess.call(RUN_PATH + 'stop_capture.sh')
end = time.time()
logging.info("Finished audio capture. Duration: " + str(end - start))
