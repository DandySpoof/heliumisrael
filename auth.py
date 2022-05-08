from twilio.rest import Client, TwilioException
from twilio.base.exceptions import *
from flask import current_app
import os

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
service_sid = os.environ.get("TWILIO_VERIFY_SERVICE_ID")

# number = input("Enter number: ")


def _get_twilio_verify_client():
	return Client(account_sid, auth_token)


def request_verification_token(phone):
	client = _get_twilio_verify_client()
	try:
		client.verify \
			.services(service_sid) \
			.verifications \
			.create(to=phone, channel='sms')
	except TwilioException:
		client.verify \
			.services(service_sid) \
			.verifications \
			.create(to=phone, channel='call')


# request_verification_token(number)

# code = str(input("Enter token: "))


def check_verification_token(phone, token):
	client = _get_twilio_verify_client()
	# print(f"AUTH FUNCTION - {token}")
	# print(f"AUTH FUNCTION - {phone}")

	try:
		result = verification_check = client.verify \
			.services(service_sid) \
			.verification_checks \
			.create(to=phone, code=token)

	except TwilioRestException:
		# print("Wrong token")
		return False

	# print(result.status)
	return result.status == 'approved'


# check_verification_token(number, code)

# try:
# 	verification_check = client.verify\
# 		.services(service_sid)\
# 		.verification_checks\
# 		.create(to='+9720507751298', code=code)
# except TwilioRestException:
# 	print("Wrong token, pls try again")
# 	code = str(input("Enter token: "))
# 	verification_check = client.verify \
# 		.services(service_sid) \
# 		.verification_checks \
# 		.create(to='+9720507751298', code=code)
#
# print(verification_check.status)
