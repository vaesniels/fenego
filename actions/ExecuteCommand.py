import os
import sys

from st2actions.runners.pythonrunner import Action

class selfheal(Action):
    def run(self,host,company,cmd,stackstormpath):
        
	if company is not "null":
		try:
			with open(stackstormpath +"SSH/"+ company + '_SSH') as ReadFile: 
				for line in ReadFile:				  #Reads the file and loads the variables
					if "host:\'" + host in line:
					    hostname = " "
					    Credentials = line.split("; ")
					    Credentials[0] = Credentials[0].strip("host:")
					    Host = Credentials[0].strip("\'")
					    Credentials[1] = Credentials[1].strip("username:")
					    Username = Credentials[1].strip("\'")
					    Credentials[2] = Credentials[2].strip("pem-file:")
					    Credentials[2] = Credentials[2].strip("\n")
					    Pempath = Credentials[2].strip("\'")
					    #Creating an SSH connection with pem key and running an python script on the remote host
					    print "trying to execute cmd " + cmd
					    returnvalue = os.system("ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host + " \'"+ cmd +"\'")
					    if returnvalue != 0 :
						return (False,"Error executing command on remote host")
		except:
			return (False,"Couldn't make ssh connection") 
	
		if hostname is "null":
			  return (False,"hostname wasn't found")   			 
	else:
		return (False,"Company wasn't found")
