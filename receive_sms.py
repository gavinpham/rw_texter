import os, constants, editdistance
from threading import Thread
from time import sleep
from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def send_price(phoneNumber):
	print "Waiting"
	sleep(10)
	print "Sending price"
	account_sid = os.environ["TWILIO_ACCOUNT_SID"]
	auth_token = os.environ["TWILIO_AUTH_TOKEN"]

	client = Client(account_sid, auth_token)

	client.messages.create(
		to=phoneNumber,
		from_="+12142144367",	##From Twilio
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
		resp.message(constants.RESPONSE_1)	#Hardcoded response to 'Lipitor, 40 mg, 30 tablets'
		thread = Thread(target=send_price, args=(from_phoneNumber, ))	#Spin a separate thread to async send pricing info
		thread.start()
	elif body == "yes":
		resp.message(constants.RESPONSE_2)	#Hardcoded response to 'YES'
	#Any other input is disregarded

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)