import os

import requests


class TelegramBot:

	def __init__(self):

		self.bot_token = os.getenv("BOT_TOKEN")
		self.bot_chatID = os.getenv("BOT_CHAT_ID")


	# Function to send telegram message
	def send_message(self, message):

	    self.text = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}'.format(self.bot_token, self.bot_chatID, message)
	    
	    self.response = requests.get(self.text)

	    return self.response.json()


	# Function to create a new telegram message
	def create_message(self, type, class_details=None):
		if type == "success" and class_details:
			self.message = """
				SIGNED UP!
				You've successfully signed up for the following lesson:

				Nummer: {}
				Sportart: {}
				Datum/Zeit: {}
				Anlage: {}
				Raum: {}
				Trainingsleitende: {}
				""".format(class_details["Nummer"], 
					class_details["Sportart"], 
					class_details["Datum/Zeit"],
					class_details["Anlage"],
					class_details["Raum"],
					class_details["Trainingsleitende"])

		elif type == "no_sign_up_button":
			self.message = "Couldn't sign up because Sign Up button could not be found :("

		else:
			self.message = "An invalid argument was passed to TelegramBot.create_msg()"

		return self.message