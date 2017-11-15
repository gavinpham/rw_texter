import os, constants
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	#Retreive body text sent from user
	body = str(request.form['Body']).lower()


	resp=MessagingResponse()

	
	if body == "lipitor, 40 mg, 30 tablets":
		resp.message(constants.RESPONSE_1)	#Hardcoded response to 'Lipitor, 40 mg, 30 tablets'
	elif body == "yes":
		resp.message(constants.RESPONSE_2)	#Hardcoded response to 'YES'

	#Any other input is disregarded
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)