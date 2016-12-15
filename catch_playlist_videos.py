import os
import sys
import json
from subprocess import Popen, PIPE

if len(sys.argv) != 3:
    sys.stderr.write('Wrong number of inputs')
    sys.exit(-1)

playlist=sys.argv[1]
outFile=sys.argv[2]

per = Popen('python3.5 /usr/local/bin/youtube-dl -j --flat-playlist ' + '"'+playlist+'"',shell=True, stdout=PIPE, stderr=PIPE)
out, err = per.communicate()
vlj = (out.decode("utf-8")).split('\n')
lout=[]
for i in vlj:
    if i:
        lout.append(json.loads(i)['url'])
prefix='https://www.youtube.com/watch?v='
with open(outFile,'w') as fp:
    for i in lout:
        fp.write('%s\n' % (prefix + i))
