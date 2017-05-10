import os
import sys

from st2actions.runners.pythonrunner import Action

class ExecuteCommand(Action):
    def run(self,host,company,cmd,stackstormpath):
        
	hostname = "null"

	if company is not "null":
		try: #trying to make an SSH connection and run a command
			with open(stackstormpath +"SSH/"+ company + '_SSH') as ReadFile: #Opens the SSH information file from the company.
				for line in ReadFile:				  #Reads the file and loads the variables
					Credentials = line.split("; ")
					Credentials[0] = Credentials[0].strip("host:")
					Host = Credentials[0].strip("\'")
					if host == Host : #If hostname is foud the script will put the info in local variables.
					    hostname = " "
					    Credentials[1] = Credentials[1].strip("username:") 
					    Username = Credentials[1].strip("\'")
					    Credentials[2] = Credentials[2].strip("pem-file:")
					    Credentials[2] = Credentials[2].strip("\n")
					    Pempath = Credentials[2].strip("\'")
					    #Creating an SSH connection with pem key and executing a command
					    returnvalue = os.system("ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host + " \'"+ cmd +"\'")
					    if returnvalue != 0 :
						print "Slack:An error occured while trying to execute the command: " + cmd + ", on the Host " + host + " of Company: " + company
						return (False,"Error executing command on remote host")
		except:
			print "Slack:Couldn't make SSH connection to the Host:" + host + " of Company: " + company
			return (False,"Couldn't make ssh connection") 
	
		if hostname is "null":
			  return (False,"hostname wasn't found")   			 
	else:
		return (False,"Company wasn't found")
