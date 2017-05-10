from datetime import datetime , timedelta
import smtplib

from st2actions.runners.pythonrunner import Action

class logchecker(Action):
    def run(self, agg_key , alert_id , alert_metric, alert_query, alert_transition, alert_status, title,last_updated,date,event_type,body,user,link,priority,tags,host,snapshot,frequency , period , company,stackstormpath,email):

	times = 0
	SomeHoursAgo = datetime.now() - timedelta(hours=period) #Calculating a date 
	try: #Opens the log file and deletes all log entrys older then "SomeHoursAgo"
		ReadFile = open(stackstormpath + "logs/" + company + "_logfile.log","r+")
		lines = ReadFile.readlines()
		ReadFile.seek(0)
		ReadFile.write(str(datetime.now()) + "; hostname:"+host + " , " + alert_query +"\n") #Puts the alert that triggered this script into the logfile.
		for line in lines:
			values = line.split("; ")
			values[0] = datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S.%f") #Gets the timestamp out of the logfile for each entry.
			if values[0] > SomeHoursAgo: #Compairs the timestamp with SomeHoursAgo when timestamp is newer than SomeHoursAgo it will rewrite the line 
				ReadFile.write(line) #When the timestamp it older then SomeHoursAgo it will delete the entry
		ReadFile.truncate()
		ReadFile.close()
	except:
		return (False, "Error loading the log file")
	
	try:
		with open(stackstormpath + "logs/" + company + "_logfile.log") as ReadFile: #Reading the logfile and checking how manny times the error came from the same host.
			for line in ReadFile:
				if host in line and alert_query in line:
					times = times + 1
	except:
		return (False, "Error reading the log file.")
#When the numbers of errors extends the predefined allowed frequency. The script will send an e-mail telling you that the service failed to manny times.
	if times > frequency :
		            print "Toadd:" + email
		            print "Message:The procces '" + alert_query +  "' failed to manny times within the time limit on host: " + host + ", aditional action is needed."
			    print "Subject:Procces failed to manny times"
			    print "Slack:The procces '" + alert_query +  "' failed to manny times within the time limit on host: " + host + ", aditional action is needed."
			    return (False, "To manny restart attempts")

	else:
        	return True #when the numbers of errors didn't exceeds the limit the script will return "true" letting stackstorm know everything is ok.

