import ffmpeg
import os
import logging
from datetime import datetime, timedelta
import threading
from threading import Thread, RLock



formatter       = logging.Formatter('%(asctime)s %(levelname)-5s %(message)s')
log_file = datetime.now().strftime('/home/nico/transcode_%Y%m%d_%H%M%S.log')
logger     = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler    = logging.FileHandler(log_file, 'a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

src_dir = '/mnt/logdepot/berl/hiq/13'
dst_dir = '/mnt/logdepot/tmp/'
dateformat = '%y%m%d%H%M'

startdate= datetime.strptime('1911010000',dateformat)
stopdate= datetime.strptime('2001310000',dateformat)

def transcode(file):
    prefix, suffix = os.path.splitext(file)
    prefix_date = datetime.strptime(prefix, dateformat)
    if '.wav' == suffix and startdate < prefix_date and stopdate > prefix_date:
        abspath_in = root + '/' + file
        dir_out = root.replace(src_dir, dst_dir)
        if not os.path.exists(dir_out):
            os.makedirs(dir_out)
        prefix_date_utc = prefix_date - timedelta(hours=1)
        prefix = prefix_date_utc.strftime(dateformat)
        #abspath_out = dir_out + '/' + prefix + '.ts'
        abspath_out = dir_out + '/' + prefix + '.aac'
        if os.path.isfile(abspath_out):
            logger.info(str(abspath_out) + " already exist")
        else:
            logger.info(str(abspath_in) + " to " + str(abspath_out) + " transcode started")
            try:
             audio = ffmpeg.input(abspath_in)
             #audio = ffmpeg.output(audio, abspath_out, format='mpegts', acodec='aac', streamid='0:482', mpegts_pmt_start_pid='0x1E0',**{'metadata:s:a:0': 'language=qaa'}, **{'fflags': '+genpts'}, audio_bitrate='64k')
             audio = ffmpeg.output(audio, abspath_out, format='adts', acodec='aac', audio_bitrate='64k')
             ffmpeg.run(audio, overwrite_output=True, capture_stdout=False, capture_stderr=True, input=None)
            except ffmpeg.Error as e:
             logger.info(str(abspath_out) + " transcode failed")
             logger.info(e.stderr.decode())



for root, dirs, files in os.walk(src_dir):
    threads=[]
    activeThreads = 0
    for file in files:
        a = threading.Thread(target=transcode, args=(file,))
        threads.append(a)
        activeThreads += 1
        if(activeThreads>30):
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            activeThreads = 0
            threads = []
    for t in threads:
        t.start()
    for t in threads:
        t.join()
