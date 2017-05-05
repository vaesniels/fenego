from datetime import datetime , timedelta
import smtplib

from st2actions.runners.pythonrunner import Action

class selfheal(Action):
    def run(self, agg_key , alert_id , alert_metric, alert_query, alert_transition, alert_status, title,last_updated,date,event_type,body,user,link,priority,tags,host,snapshot,frequency , period , company,stackstormpath):
	limit = "no"
	times = 0
	OneHourAgo = datetime.now() - timedelta(hours=period)
	try:
		ReadFile = open(stackstormpath + "logs/" + company + "_logfile.log","r+")
		lines = ReadFile.readlines()
		ReadFile.seek(0)
		ReadFile.write(str(datetime.now()) + "; hostname:"+host + " , " + alert_query +"\n")
		for line in lines:
			values = line.split("; ")
			values[0] = datetime.strptime(values[0], "%Y-%m-%d %H:%M:%S.%f")
			if values[0] > OneHourAgo:
				ReadFile.write(line)
		ReadFile.truncate()
		ReadFile.close()
	except:
		return (False, "Error loading the log file")
	
	try:
		with open(stackstormpath + "logs/" + company + "_logfile.log") as ReadFile:
			for line in ReadFile:
				if host in line and alert_query in line:
					times = times + 1
	except:
		return (False, "Error reading the log file.")

	if times > frequency :
		            print "Procces failed to manny times within the time limit"
		            again = "yes"
		            fromadd = 'tqwertyhgf@gmail.com'
		            toadd = 't.qwertyhgf@gmail.com'

		            username = 'tqwertyhgf@gmail.com'
		            passwd = 'melon123dfgh10'

		            text = "The procces '" + alert_query +  "' failed to manny times within the time limit on host: " + host + ", aditional action is needed."

		            try:
		                    server = smtplib.SMTP('smtp.gmail.com:587')
		                    server.ehlo()
		                    server.starttls()
		                    server.login(username, passwd)
		                    msg = 'Subject: {}\n\n{}'.format("Proccess failed to manny times", text)
		                    server.sendmail(fromadd, toadd, msg)
		                    print("Mail Send Successfully")
		                    server.quit()

		            except:
		                    print("Error:unable to send mail")

	if limit == "no":
        	return True
	else:
        	return (False, "To manny restart attempts")
