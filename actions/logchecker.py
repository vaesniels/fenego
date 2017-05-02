from datetime import datetime , timedelta
import smtplib

from st2actions.runners.pythonrunner import Action

class selfheal(Action):
    def run(self, agg_key , alert_id , alert_metric, alert_query, alert_transition, alert_status, title,last_updated,date,event_type,body,user,link,priority,tags,host,snapshot):
	again = "no"
	times = 0
	OneHourAgo = datetime.now() - timedelta(hours=1)

	ReadFile = open("/opt/stackstorm/packs/fenego/" + "logfile.log","r+")
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
	with open("/opt/stackstorm/packs/global/" + "logfile.log") as ReadFile:
		for line in ReadFile:
		        if host in line and alert_query in line:
				times = times + 1
	if times > 1 :
		            print "Procces failed to manny times within the time limit"
		            again = "yes"
		            fromadd = 'tqwertyhgf@gmail.com'
		            toadd = 't.qwertyhgf@gmail.com'

		            username = 'tqwertyhgf@gmail.com'
		            passwd = 'melon123dfgh10'

		            text = "The procces '" + serv +  "' failed to manny times within the time limit on host: " + host + ", aditional action is needed."

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

	if again == "no":
        	return True
	else:
        	return (False, "To manny restart attempts")
