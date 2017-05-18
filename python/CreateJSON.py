import os
import subprocess
from datetime import datetime, timedelta

outputlist = ""
output = subprocess.check_output("cd /home/niels/Jsonfiles/ && ls", shell=True)
#print output
output = output.replace(".json", "")
#print output
max = max(output)
#print max
index = int(max) + 1
now = datetime.utcnow()
now = now.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
hourago = datetime.utcnow() - timedelta(hours=1)
hourago = hourago.strftime('%Y-%m-%dT%H:%M:%S.000000Z')
#print now
#print hourago
output = subprocess.check_output("sudo st2 execution list -tg '" + hourago +"' -tl '"+ now +"' -n 100", shell=True)
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
            file = open("/home/niels/Jsonfiles/" + str(index) + ".json", "w")
            file.write(output[0])
            file.close()
            os.system("curl -XPOST 'http://localhost:9200/pythontest/pythonjson/" + str(index) + "' -d " + "@/home/niels/Jsonfiles/" + str(index) + ".json")
            index = index +1



