import os
import sys

from st2actions.runners.pythonrunner import Action

class selfheal(Action):
    def run(self, agg_key , alert_id , alert_metric, alert_query, alert_transition, alert_status, title,last_updated,date,event_type,body,user,link,priority,tags,host,snapshot,size,day,path,company):
        
	StackstormPath = "/opt/stackstorm/packs/fenego/"
	hostname = "null"

	with open(StackstormPath +"SSH/"+ company + '_SSH') as ReadFile: 
		for line in ReadFile:				  #Reads the file and loads the variables
			Credentials = line.split("; ")
			Credentials[0] = Credentials[0].strip("host:")
			Host = Credentials[0].strip("\'")
			if host == Host :
				hostname = " "
				Credentials[1] = Credentials[1].strip("username:")
				Username = Credentials[1].strip("\'")
				Credentials[2] = Credentials[2].strip("pem-file:")
				Credentials[2] = Credentials[2].strip("\n")
				Pempath = Credentials[2].strip("\'")
					    #Creating an SSH connection with pem key and running an python script on the remote host
				returnvalue = os.system("ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host  + " python -u - "+ alert_id + " " + path +" " + size + " " + day + " < " + StackstormPath + "python/DiskCleanUp.py")
				if returnvalue != 0 :
					return (False,"Error executing pythonfile on remote host")
				   			
				returnvalue = os.system("ssh -i " + Pempath + " " + Username + "@" + Host + " \'sudo rm /tmp/"+alert_id+"\'")
				if returnvalue != 0 :
					return (False,"Error deleteing temp log file")
	if hostname is "null":
		return (False,"hostname was not found")   			 
