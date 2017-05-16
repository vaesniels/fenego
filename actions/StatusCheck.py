import os
import sys
import smtplib
from email.mime.text import MIMEText
import datetime
import subprocess
import time

from st2actions.runners.pythonrunner import Action


class ServiceStatus(Action):
    def run(self, host, company, stackstormpath, servicename, attempts=10, logfile):
        started = "No"
        with open(stackstormpath + "SSH/" + company + '_SSH') as ReadFile:  # Opens the SSH information file from the company.
            for line in ReadFile:  # Reads the file and loads the variables
                Credentials = line.split("; ")
                Credentials[0] = Credentials[0].strip("host:")
                Host = Credentials[0].strip("\'")
                if host == Host:  # If hostname is foud the script will put the info in local variables.
                    Credentials[1] = Credentials[1].strip("username:")
                    Username = Credentials[1].strip("\'")
                    Credentials[2] = Credentials[2].strip("pem-file:")
                    Credentials[2] = Credentials[2].strip("\n")
                    Pempath = Credentials[2].strip("\'")
                    # Creating an SSH connection with pem key and executing a command
		    try:
		            if servicename.lower() == "hybris" :
		                x = 0
		                now = datetime.datetime.now()
		                nu = now.strftime('%Y%m%d')
		                logfile = logfile + "console-" +str(nu) + ".log"
		                while x < int(attempts):
		                    x = x + 1
		                    time.sleep(30)
		                    output = subprocess.check_output("sudo ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host + " \'tail -200 " + logfile + " \'", shell=True)
		                    if "INFO: Server startup in" in output:
		                        x = attempts
		                        started = "Yes"
		                if started == "Yes" :
		                    return True
		                else:
				    print "Slack:Hybris did not start on Host : " + host + " of Company: " + company
		                    return (False, "Hybris did not start")

		            if servicename.lower() == "nginx":
		                now = datetime.datetime.now()
		                nu = now.strftime('[%d/%b/%Y')
		                time.sleep(60)
		                os.system("sudo ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host + " \'curl localhost\'")
		                output = subprocess.check_output("sudo ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host + " \'sudo -u root tail -2 " + logfile + " \'",shell=True)
		                output = output.split("\n")
		                for x in range(0,len(output)-1):
		                        if nu in output[x] and "curl" in output[x] and "127.0.0.1" in output[x]:
		                            x = len(output) - 1
		                            started = "Yes"
		                if started == "No" :
		                    print "Slack:Nginx did not start on Host : " + host + " of Company: " + company
		                    return (False, "nginx did not start")
		                else:
		                    return True
		    except:
			print "Slack:A error occurred while trying to preform a Status Check on Host: " + host + " of Company: " + company
            		return (False, "Error trying executing a service check")


