import time
import datetime
import subprocess
import sys
import os

def timeH():
    return float(datetime.datetime.now().strftime('%H')) + float(datetime.datetime.now().strftime('%M'))/100.

path_download='/Users/krikitos/Desktop/tmp_download/youtube'

if len(sys.argv) != 6:
    sys.stderr.wrtie('Wrong number of arguments')
    sys.exit(-1)

listArgs=sys.argv
startTime=int(listArgs[1]) + int(listArgs[2])/100.
endTime=int(listArgs[3]) + int(listArgs[4])/100.
pathList=listArgs[5]

while True:
    timeNow=timeH()
    if (timeNow >= startTime) and (timeNow < endTime):
        # time to start download
        with open(pathList,'r') as fp:
            for name in fp.readlines():
#                p = subprocess.Popen('python3.5 /usr/local/bin/youtube-dl --format 249 --extract-audio --audio-format mp3 ' + name.strip(), shell=True)
                p = subprocess.Popen('python3.5 /usr/local/bin/youtube-dl --format 171 ' + name.strip(), shell=True)            
                while p.poll() is None: 
                    if timeH() >= endTime:
                        p.terminate()
                        p.kill()
                        sys.exit(1)
                    time.sleep(0.5)
        sys.exit(0)
    time.sleep(1)
