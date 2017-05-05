import os
import sys
import subprocess
import datetime as DT
import smtplib

today = DT.datetime.today()
deletedate = today - DT.timedelta(days=int(sys.argv[4]))
paths = sys.argv[2].split("$") #sys.args[2] are the paths on the system that can be cleaned up.

os.system('sudo touch /tmp/' + sys.argv[1])	#Create a temp file to store output and send this content as a mail.
os.system('sudo chmod 777 /tmp/' + sys.argv[1]) #sys.args[1] is a unique eventID. this eventID is used to make sure the filename doens't already exists

output = subprocess.check_output('df -h', shell=True)
output = output.split("\n")
os.system("echo " + output[0] + " >> /tmp/" + sys.argv[1])  #This is going to put some info in the temp file.
for x in range(1, len(output) - 1):
    if output[x].startswith("/dev/"):
        os.system("echo " + output[x] + " >> /tmp/" + sys.argv[1])

for i in range(0, len(paths)):
	output = subprocess.check_output("sudo find " + paths[i]+ " -type f -size +"+sys.argv[3]+"M -exec ls -lh --time-style=long-iso {} \; 2> /dev/null"" | awk '{ print $NF \": \" $5 \": \" $6}'", shell=True) #This is going to generate a list of files that exceeds the predefined file size. The file size is defined in sys.argv[3].
	ouput = output.split("\n")
	for x in range(0, len(output) - 1): #with the paths that can be cleaned.
		values = output[x].split(": ")
		date = DT.datetime.strptime(values[2], "%Y-%m-%d")
		if date > deletedate: #script will check if the file is older then the defined date. When it is , it's allowed to be deleted.
		        os.system("echo " + values[0] + " >> /tmp/" + sys.argv[1])
		        returncode = os.system("sudo zip -j " + values[0] + ".zip " + values[0])
		        if returncode == 0: #Only when zipping the file is successfull the original file will be deleted.
		            os.system("echo File : " + values[0] + " has been zipped >> /tmp/" + sys.argv[1])
		            os.system("sudo rm " + values[0])
		        else:
		            os.system("echo Error while zipping : " + values[0] + " >> /tmp/" + sys.argv[1])



output = subprocess.check_output('df -h', shell=True)
output = output.split("\n")
os.system("echo ' ' >> /tmp/" + sys.argv[1])
os.system("echo " + output[0] + " >> /tmp/" + sys.argv[1])#Again putting some info in the temp file.
for x in range(1, len(output) - 1):
    if output[x].startswith("/dev/"):
        os.system("echo " + output[x] + " >> /tmp/" + sys.argv[1])

fromadd = 'tqwertyhgf@gmail.com'
toadd = 't.qwertyhgf@gmail.com'

text = subprocess.check_output("sudo cat /tmp/" + sys.argv[1], shell=True)

username = 'tqwertyhgf@gmail.com'
passwd = 'melon123dfgh10'

try: #trying to mail the info from the temp file.
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, passwd)
    msg = 'Subject: {}\n\n{}'.format("diskclean has run", text)
    server.sendmail(fromadd, toadd, msg)
    print("Mail Send Successfully")
    server.quit()

except:
    print("Error:unable to send mail")
