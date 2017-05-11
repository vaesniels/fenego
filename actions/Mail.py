import os
import sys
import smtplib
from email.mime.text import MIMEText

from st2actions.runners.pythonrunner import Action

class mail(Action):
    def run(self,message):
            y = 0
	    toadd = ""
	    MessageParts = message.split('\n')
	    print MessageParts
	    for x in MessageParts :
		if MessageParts[y].startswith('Toadd:') :
		    toadd = MessageParts[y].replace('Toadd:', '')
		    print toadd
		if MessageParts[y].startswith('Message:') :
		    text = MessageParts[y].replace('Message:', '')
		    text = text.replace('$newline', '\n')
		    print text
		if MessageParts[y].startswith('Subject:') :
		    subject = MessageParts[y].replace('Subject:', '')
		    print subject
		y = y + 1
	    if toadd != "" :
		    try:
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.ehlo()
			server.starttls()
			server.login('StackstormTool@gmail.com', 'fenego101')
			msg = MIMEText(text)
			sender = 'stackstormtool@gmail.com'
			recipients = toadd
			msg['Subject'] = subject
			msg['From'] = sender
			msg['To'] = recipients
			server.sendmail(sender, recipients.split(','), msg.as_string())
			print("Mail Send Successfully")
			server.quit()

		    except:
			print("Error:unable to send mail")
