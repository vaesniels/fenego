from st2actions.runners.pythonrunner import Action

class ReturnFalse(Action):
    def run(self,message):
	return False

