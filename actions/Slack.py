import os
import sys

from st2actions.runners.pythonrunner import Action

class Slack(Action):
    def run(self,message):
	y = 0
	msg = ""
	MessageParts = message.split('\n')
	print MessageParts
	for x in MessageParts :
		if MessageParts[y].startswith('Slack:') :
		    msg = MessageParts[y].replace('Slack:', '')
		y = y + 1
	msg = msg.replace("'", "")
	msg = msg.replace('"', '')
	msg = msg.replace("$newline", "\n")
	os.system('curl -X POST --data-urlencode \'payload={"channel": "#general", "username": "StackStorm", "text" :" ' + msg + '"}\' https://hooks.slack.com/services/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')

