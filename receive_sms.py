import os, constants, editdistance
from threading import Thread
from time import sleep
from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def isFullPrescription(body):
	#Calculate editdistance from body to accepted response
	editDistancePrescriptionFull = editdistance.eval(body, constants.PRESCRIPTION_FULL)						# Lipitor, 40 mg, 30 tablets
	editDistancePrescriptionFullLong = editdistance.eval(body, constants.PRESCRIPTION_FULL_LONG)			# Lipitor, 40 milligrams, 30 tablets
	return editDistancePrescriptionFull <= constants.LENIENT_EDIT_DISTANCE or editDistancePrescriptionFullLong <= constants.LENIENT_EDIT_DISTANCE

def isPrescriptionName(body):
	editDistancePrescriptionName = editdistance.eval(body, constants.PRESCRIPTION_NAME)						# Lipitor
	return editDistancePrescriptionName <= constants.STRICT_EDIT_DISTANCE

def isPrescriptionDosage(body):
	editDistancePrescriptionDosage = editdistance.eval(body, constants.PRESCRIPTION_DOSAGE)					# 40 mg
	editDistancePrescriptionDosageLong = editdistance.eval(body, constants.PRESCRIPTION_DOSAGE_LONG)		# 40 milligrams
	return editDistancePrescriptionDosage <= constants.STRICT_EDIT_DISTANCE or editDistancePrescriptionDosageLong <= constants.STRICT_EDIT_DISTANCE

def isPrescriptionQuantity(body):
	editDistancePrescriptionQuantity = editdistance.eval(body, constants.PRESCRIPTION_QUANTITY)				# 30 tabs
	editDistancePrescriptionQuantityLong = editdistance.eval(body, constants.PRESCRIPTION_QUANTITY_LONG)	# 30 tablets
	editDistancePrescriptionQuantityPills = editdistance.eval(body, constants.PRESCRIPTION_QUANTITY_PILLS)	# 30 pills
	return editDistancePrescriptionQuantity <= constants.STRICT_EDIT_DISTANCE or editDistancePrescriptionQuantityLong <= constants.STRICT_EDIT_DISTANCE or editDistancePrescriptionQuantityPills <= constants.STRICT_EDIT_DISTANCE

def send_price(phoneNumber):
	account_sid = os.environ["TWILIO_ACCOUNT_SID"]						#From Twilio, stored in OS for security
	auth_token = os.environ["TWILIO_AUTH_TOKEN"]			
	account_phoneNumber = os.environ["TWILIO_PHONE_NUMBER"]

	client = Client(account_sid, auth_token)

	client.messages.create(
		to=phoneNumber,
		from_=account_phoneNumber,							
		body=constants.PRICE_RESPONSE
	)

def send_follow_up(phoneNumber):
	account_sid = os.environ["TWILIO_ACCOUNT_SID"]						
	auth_token = os.environ["TWILIO_AUTH_TOKEN"]			
	account_phoneNumber = os.environ["TWILIO_PHONE_NUMBER"]

	client = Client(account_sid, auth_token)

	client.messages.create(
		to=phoneNumber,
		from_=account_phoneNumber,							
		body=constants.CARD_FOLLOW_UP,
	)

def send_card(phoneNumber):
	account_sid = os.environ["TWILIO_ACCOUNT_SID"]						
	auth_token = os.environ["TWILIO_AUTH_TOKEN"]			
	account_phoneNumber = os.environ["TWILIO_PHONE_NUMBER"]

	client = Client(account_sid, auth_token)

	client.messages.create(
		to=phoneNumber,
		from_=account_phoneNumber,							
		body=constants.CARD_RESPONSE,
		media_url="https://i.imgur.com/XcaxuQC.jpg"
	)

def delayed_response(phoneNumber):
	sleep(constants.DELAY_IN_SECONDS)									#Sleep for x seconds to simulate processing overhead
	send_price(phoneNumber)
	sleep(constants.RW_CARD_DELAY)
	send_follow_up(phoneNumber)

@app.route("/sms", methods=['GET', 'POST'])								#If a SMS message comes into our number, execute this function:
def sms_reply():
	from_phoneNumber = str(request.form['From'])						#Retreive phone number from user
	body = str(request.form['Body']).lower()							#Retreive body text sent from user
	resp=MessagingResponse()											#Construct response object

	if isPrescriptionName(body):
		resp.message(constants.DOSAGE_ASK)
	elif isPrescriptionDosage(body):
		resp.message(constants.QUANTITY_ASK)
	elif isFullPrescription(body) or isPrescriptionQuantity(body):
		resp.message(constants.THANK_YOU_RESPONSE)
		thread = Thread(target=delayed_response, args=(from_phoneNumber, ))	#Spin a separate thread to async send pricing info
		thread.start()
	elif body == "yes":
		resp.message(constants.QUESTION_RESPONSE)
	elif body == "blue":
		send_card(from_phoneNumber)
	else:
		resp.message(constants.UNRECOGNIZED_RESPONSE)

	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)