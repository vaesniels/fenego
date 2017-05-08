import os
import sys
import subprocess

from st2actions.runners.pythonrunner import Action

class selfheal(Action):
    def run(self, agg_key , alert_id , alert_metric, alert_query, alert_transition, alert_status, title,last_updated,date,event_type,body,user,link,priority,tags,host,snapshot,size,day,path,company,stackstormpath):
        
	hostname = "null"
	DiskSpaceToClean = 0.0
	TotalDiskSpaceUsed= 0.0
	DiskSpaceAfterClean = 0.0

	with open(stackstormpath +"SSH/"+ company + '_SSH') as ReadFile: 
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
				output = subprocess.check_output("sudo ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host + " \'df -h\'", shell=True)
				output = output.split("\n")
				for x in range(1, len(output) - 1):
					if output[x].startswith("/dev/"):
						disk = output[x].split(" ")
						if "G" in disk[9] :
						    diskused = disk[9].strip("G")
						    diskused = diskused.replace(",", ".")
						if "T" in disk[9] :
						    diskused = disk[9].strip("T")
						    diskused = diskused.replace(",", ".")
						    diskused = float(diskused) * 1024
						SpaceToClean = (float(diskused) / 100 ) * 10
						TotalDiskSpaceUsed += float(diskused)
						DiskSpaceToClean = DiskSpaceToClean + SpaceToClean

				returnvalue = os.system("ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host  + " python -u - "+ alert_id + " " + path +" " + size + " " + day + " < " + stackstormpath + "python/DiskCleanUp.py")
#passing some variables to the pythonscript 
#alert_id will be sys.argv[1]
#path will be sys.argv[2]
#size will be sys.argv[3]
#day will be sys.argv[4]
				if returnvalue != 0 :
					return (False,"Error executing pythonfile on remote host")
				output = subprocess.check_output("sudo ssh -o StrictHostKeyChecking=No -i " + Pempath + " " + Username + "@" + Host + " \'df -h\'", shell=True)
				output = output.split("\n")
				for x in range(1, len(output) - 1):
				    if output[x].startswith("/dev/"):
					disk = output[x].split(" ")
					if "G" in disk[9] :
					    diskused = disk[9].strip("G")
					    diskused = diskused.replace(",", ".")
					if "T" in disk[9] :
					    diskused = disk[9].strip("T")
					    diskused = diskused.replace(",", ".")
					    diskused = float(diskused) * 1024
					DiskSpaceAfterClean += float(diskused)
				if DiskSpaceAfterClean <= (TotalDiskSpaceUsed - DiskSpaceToClean) :
					print "genoeg schoongemaakt"
				else :
					print "nie genoeg schoongemaakt"
				   			
				returnvalue = os.system("ssh -i " + Pempath + " " + Username + "@" + Host + " \'sudo rm /tmp/"+alert_id+"\'")
				if returnvalue != 0 :
					return (False,"Error deleteing temp log file")
	if hostname is "null":
		return (False,"hostname was not found")   			 
