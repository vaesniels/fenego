#!/usr/bin/env python

import os
import subprocess
from datetime import datetime, timedelta

SomeTimeAgo  = datetime.utcnow() - timedelta(minutes=15)
SomeTimeAgo = SomeTimeAgo.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
LongerAgo = datetime.utcnow() - timedelta(minutes=16)
LongerAgo = LongerAgo.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
#print now
#print hourago
output = subprocess.check_output("sudo st2 execution list -tg '" + LongerAgo +"' -tl '"+ SomeTimeAgo +"' -n 100", shell=True)
#print output
outputlist = output
outputlist = outputlist.split("\n")
for x in range(3, len(outputlist)-2):
    line = outputlist[x]
    #print line
    if "packs." not in line:
        line = line.split("|")
        ExecutionID = line[1].replace(" ", "")
        if ExecutionID != "":
            if "+" in ExecutionID:
                ExecutionID = ExecutionID.replace("+","")
            #print test
            output = subprocess.check_output("sudo st2 execution get " + ExecutionID + " -j", shell=True)
            output = output.split("[\n")
            #print output
            os.system("curl -XPOST 'http://localhost:9200/stackstorm/actions/' -d \'" + output[0] + "\'")
