import os
import sys
import smtplib
from st2actions.runners.pythonrunner import Action

class mail(Action):
    def run(self,message):
            y = 0
	    MessageParts = message.split('\n')
	    print MessageParts
	    for x in MessageParts :
		if MessageParts[y].startswith('Toadd:') :
		    toadd = MessageParts[y].replace('Toadd:', '')
		    print toadd
		if MessageParts[y].startswith('Message:') :
		    text = MessageParts[y].replace('Message:', '')
		    print text
		if MessageParts[y].startswith('Subject:') :
		    subject = MessageParts[y].replace('Subject:', '')
		    print subject
		y = y + 1

	    try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login('StackstormTool@gmail.com', 'fenego101')
		msg = 'Subject: {}\n\n{}'.format(subject, text)
		server.sendmail('StackstormTool@gmail.com', toadd, msg)
		print("Mail Send Successfully")
		server.quit()

	    except:
		print("Error:unable to send mail")
