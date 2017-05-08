import os
import sys
import smtplib
from st2actions.runners.pythonrunner import Action

class mail(Action):
    def run(self,message):
        
	    MessageParts = message.split('\n')
	    for x in MessageParts :
		if MessageParts.startswith('Username:')
			username = MessageParts[x].strip('Username:')
		if MessageParts.startswith('Fromadd:')
			fromadd = MessageParts[x].strip('Fromadd:')
		if MessageParts.startswith('Toadd:')
			toadd = MessageParts[x].strip('Toadd:')
		if MessageParts.startswith('Passwd:')
			passwd = MessageParts[x].strip('Passwd:')
		if MessageParts.startswith('Message:')
			text = MessageParts[x].strip('Message:')
		if MessageParts.startswith('Subject:')
			subject = MessageParts[x].strip('Subject:')


	    #fromadd = 'tqwertyhgf@gmail.com'
	    #toadd = 't.qwertyhgf@gmail.com'

	    #username = 'tqwertyhgf@gmail.com'
	    #passwd = 'melon123dfgh10'

	    #text = "The procces '" + alert_query +  "' failed to manny times within the time limit on host: " + host + ", aditional action is needed."

	    try:
		    server = smtplib.SMTP('smtp.gmail.com:587')
		    server.ehlo()
		    server.starttls()
		    server.login(username, passwd)
		    msg = 'Subject: {}\n\n{}'.format(subject, text)
		    server.sendmail(fromadd, toadd, msg)
		    print("Mail Send Successfully")
		    server.quit()

	    except:
		    print("Error:unable to send mail")
