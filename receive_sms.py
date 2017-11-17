import os, constants, editdistance
from threading import Thread
from time import sleep
from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def send_price(phoneNumber):
	sleep(constants.DELAY_IN_SECONDS)						##Automate a delayed response
	account_sid = os.environ["TWILIO_ACCOUNT_SID"]			##From Twilio, stored in OS for security
	auth_token = os.environ["TWILIO_AUTH_TOKEN"]			##From Twilio, stored in OS for security
	account_phoneNumber = os.environ["TWILIO_PHONE_NUMBER"]	##From Twilio, stored in OS for security

	client = Client(account_sid, auth_token)

	client.messages.create(
		to=phoneNumber,
		from_=account_phoneNumber,							
		body=constants.PRICE_RESPONSE
	)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	#Retreive body text sent from user
	body = str(request.form['Body']).lower()
	from_phoneNumber = str(request.form['From'])

	print body
	print from_phoneNumber
	editDistanceLipitor = editdistance.eval(body, constants.LIPITOR_EXAMPLE)
	print editDistanceLipitor

	resp=MessagingResponse()

	
	if editDistanceLipitor <= 6:
		resp.message(constants.RESPONSE_1)								#Hardcoded response to 'Lipitor, 40 mg, 30 tablets'
		thread = Thread(target=send_price, args=(from_phoneNumber, ))	#Spin a separate thread to async send pricing info
		thread.start()
	elif body == "yes":
		resp.message(constants.RESPONSE_2)								#Hardcoded response to 'YES'
																		#Any other input is disregarded

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)