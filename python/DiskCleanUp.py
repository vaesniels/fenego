import os
import sys
import subprocess
import datetime as DT
import smtplib

today = DT.datetime.today()
Available = 0.0
diskavailable = 0.0
deletedate = today - DT.timedelta(days=int(2))
paths = sys.argv[1].split("$") #sys.args[2] are the paths on the system that can be cleaned up.

for i in range(0, len(paths)):
    output = subprocess.check_output("sudo find " + paths[i] + " -type f -size +1000M -exec ls -lh --time-style=long-iso {} \; 2> /dev/null"" | awk '{ print $NF \": \" $5 \": \" $6}'", shell=True) #This is going to generate a list of files that exceeds the predefined file size. The file size is defined in sys.argv[3].
    output = output.split("\n")

    for x in range(0, len(output) - 1): #with the paths that can be cleaned.
        values = output[x].split(": ")
        date = DT.datetime.strptime(values[2], "%Y-%m-%d")
        if date > deletedate: #script will check if the file is older then the defined date. When it is , it's allowed to be deleted.
            command = subprocess.check_output("df -h",shell=True)
            command = command.split("\n")

            for y in range(1, len(command) - 1):
                if command[y].startswith("/dev/"):
                    disk = command[y].split(" ")
                    while '' in disk:
                        disk.remove('')

                    if "M" in disk[3]:
                        diskavailable = disk[3].strip("M")
                        diskavailable = diskavailable.replace(",", ".")
                        diskavailable = float(diskavailable) / 1024
                    if "G" in disk[3]:
                        diskavailable = disk[3].strip("G")
                        diskavailable = diskavailable.replace(",", ".")
                    if "T" in disk[3]:
                        diskavailable = disk[3].strip("T")
                        diskavailable = diskavailable.replace(",", ".")
                        diskavailable = float(diskavailable) * 1024
                    Available += float(diskavailable)
            if "M" in values[1]:
                filesize = values[1].strip("M")
                filesize = filesize.replace(",", ".")
                SizeOfFile = float(filesize) / 1024
            if "G" in values[1]:
                filesize = values[1].strip("G")
                filesize = filesize.replace(",", ".")
                SizeOfFile = float(filesize)
            if "T" in values[1]:
                filesize = values[1].strip("T")
                filesize = filesize.replace(",", ".")
                SizeOfFile = float(filesize) * 1024
            if ((SizeOfFile/100) * 20) > Available:
		os.system("sudo echo '" + values[0] + "' >> /tmp/FileWasToBig")
            else:
                returncode = os.system("sudo gzip -f " + values[0])

