import ffmpeg
import os
import logging
from datetime import datetime, timedelta
import threading
from threading import Thread, RLock



formatter       = logging.Formatter('%(asctime)s %(levelname)-5s %(message)s')
log_file = datetime.now().strftime('transcode_%Y%m%d_%H%M%S.log')
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

src_dir = '/mnt/logdepot/tmp'
dst_dir = '/mnt/logdepot/tmp/mux'
dateformat = '%y%m%d%H%M'
arrdateformat = '%y%m%d'
startdate= datetime.strptime('1911010000',dateformat)
stopdate= datetime.strptime('2001310000',dateformat)
daysArr = {}
foundFiles = []

def findFiles():
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            prefix, suffix = os.path.splitext(file)
            prefix_date = datetime.strptime(prefix, dateformat)
            if '.aac' == suffix:
                abspath_in = root + '/' + file
                dir_out = root.replace(src_dir, dst_dir)
                if not os.path.exists(dir_out):
                    os.makedirs(dir_out)
                prefix_date_utc = prefix_date - timedelta(hours=1)
                prefix = prefix_date_utc.strftime(dateformat)
                foundFiles.append(prefix)
    for file in sorted(foundFiles):
        day = file[:-4]
        if(day not in daysArr.keys()):
            daysArr[day] = []
        #daysArr[day].append(str(file + '.aac'))
        daysArr[day].append(str(dir_out + '/' + file + '.aac'))
    concatFiles(daysArr)

def concatFiles(filesArr):
    for day in filesArr:
        print("===== %s =====" % (day))
        listDay = '|'.join(filesArr[day])
        try:
             print("try")
             print(listDay)
             # audio = ffmpeg.input(abspath_in)
             # audio = ffmpeg.output(audio, abspath_out, format='mpegts', acodec='aac', streamid='0:482', mpegts_pmt_start_pid='0x1E0',**{'metadata:s:a:0': 'language=qaa'}, **{'fflags': '+genpts'}, audio_bitrate='64k')
             # audio = ffmpeg.output(audio, abspath_out, format='adts', acodec='aac', audio_bitrate='64k')
             # ffmpeg.run(audio, overwrite_output=True, capture_stdout=False, capture_stderr=True, input=None)
        except ffmpeg.Error as e:
             logger.info(str(abspath_out) + " transcode failed")
             logger.info(e.stderr.decode())
findFiles()
