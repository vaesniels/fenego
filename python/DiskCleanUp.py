import os
import sys
import subprocess
import datetime as DT
import smtplib

today = DT.datetime.today()
deletedate = today - DT.timedelta(days=int(sys.argv[4]))
paths = sys.argv[2].split("$")

os.system('sudo touch /tmp/' + sys.argv[1])
os.system('sudo chmod 777 /tmp/' + sys.argv[1])

output = subprocess.check_output('df -h', shell=True)
output = output.split("\n")
os.system("echo " + output[0] + " >> /tmp/" + sys.argv[1])
for x in range(1, len(output) - 1):
    if output[x].startswith("/dev/"):
        os.system("echo " + output[x] + " >> /tmp/" + sys.argv[1])

output = subprocess.check_output(
    "sudo find / -type f -size +"+sys.argv[3]+"M -exec ls -lh --time-style=long-iso {} \; 2> /dev/null"" | awk '{ print $NF \": \" $5 \": \" $6}'",
    shell=True)

os.system("echo '\nFiles bigger than "+sys.argv[3] + " MB :' >> /tmp/" + sys.argv[1])
os.system("echo '" + output + "' >> /tmp/" + sys.argv[1])
os.system("echo 'selected files :' >> /tmp/" + sys.argv[1])

output = output.split("\n")
for x in range(0, len(output) - 1):
    values = output[x].split(": ")
    date = DT.datetime.strptime(values[2], "%Y-%m-%d")
    for y in range(0, len(paths)):
        if paths[y] in values[0]:
            if date > deletedate:
                os.system("echo " + values[0] + " >> /tmp/" + sys.argv[1])
                returncode = os.system("sudo zip -j " + values[0] + ".zip " + values[0])
                if returncode == 0:
                    os.system("echo File : " + values[0] + " has been zipped >> /tmp/" + sys.argv[1])
                    os.system("sudo rm " + values[0])
                else:
                    os.system("echo Error while zipping : " + values[0] + " >> /tmp/" + sys.argv[1])

output = subprocess.check_output('df -h', shell=True)
output = output.split("\n")
os.system("echo ' ' >> /tmp/" + sys.argv[1])
os.system("echo " + output[0] + " >> /tmp/" + sys.argv[1])
for x in range(1, len(output) - 1):
    if output[x].startswith("/dev/"):
        os.system("echo " + output[x] + " >> /tmp/" + sys.argv[1])

fromadd = 'tqwertyhgf@gmail.com'
toadd = 't.qwertyhgf@gmail.com'

text = subprocess.check_output("sudo cat /tmp/" + sys.argv[1], shell=True)

username = 'tqwertyhgf@gmail.com'
passwd = 'melon123dfgh10'

try:
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
