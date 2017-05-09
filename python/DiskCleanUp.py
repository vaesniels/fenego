import os
import sys
import subprocess
import datetime as DT
import smtplib

today = DT.datetime.today()
deletedate = today - DT.timedelta(days=int(sys.argv[3]))
paths = sys.argv[1].split("$") #sys.args[2] are the paths on the system that can be cleaned up.

for i in range(0, len(paths)):
    output = subprocess.check_output("sudo find " + paths[i]+ " -type f -size +"+sys.argv[2]+"M -exec ls -lh --time-style=long-iso {} \; 2> /dev/null"" | awk '{ print $NF \": \" $5 \": \" $6}'", shell=True) #This is going to generate a list of files that exceeds the predefined file size. The file size is defined in sys.argv[3].
    output = output.split("\n")
    
    for x in range(0, len(output) - 1): #with the paths that can be cleaned.
        values = output[x].split(": ")
        date = DT.datetime.strptime(values[2], "%Y-%m-%d")
        if date > deletedate: #script will check if the file is older then the defined date. When it is , it's allowed to be deleted.
            returncode = os.system("sudo zip -j " + values[0] + ".zip " + values[0])
            if returncode == 0: #Only when zipping the file is successfull the original file will be deleted.
                os.system("sudo rm " + values[0])

