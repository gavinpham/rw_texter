import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(account_sid, auth_token)

client.messages.create(
	to=os.environ["MY_PHONE_NUMBER"],
	from_="+12142144367",	##From Twilio
	body="Test"
)