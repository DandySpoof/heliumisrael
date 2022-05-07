from datetime import datetime, timedelta
from dateutil import parser
import requests as rq
#
# time = datetime.now()
# last_7_days = time - timedelta(days=7)
# last_30_days = time - timedelta(days=30)
#
# print(last_7_days.isoformat())
# print(time.isoformat())

# date = "2020-08-29T00:00:00Z"
# yourdate = parser.parse(date)
# print(yourdate)
#
# time = datetime.now()
# last_7_days = time - timedelta(days=7)
# last_30_days = time - timedelta(days=30)
#
# url = f"https://api.helium.io/v1/hotspots/112PWaKaDxttMrxGem7Trt6Qs65ryCF9paeeoaQdNs2HTCiJsNNT/rewards/sum"
#
# headers = {
# 		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
# 	}
#
# parameters = {
#     "max_time": time.isoformat(),
#     "min_time": last_7_days.isoformat(),
# }
# response = rq.get(url, headers=headers, params=parameters)
# response.raise_for_status()
# data_7 = response.json()
# earining_7 = float(data_7["data"]['sum']) / 100000000
# print(earining_7)
#

# data = {
# #   "data": [
# #     {
# #       "lng": -122.51688114452725,
# #       "lat": 38.109947587584905,
# #       "timestamp_added": "2019-08-02T00:13:25.000000Z",
# #       "status": {
# #         "online": "online",
# #         "listen_addrs": ["/ip4/64.7.85.50/tcp/28762"],
# #         "height": 769399
# #       },
# #       "reward_scale": 1,
# #       "owner": "13fTdByCpUDRKuVh4VZcUWh7rdehrh4UfjMdFt17ew4h93nD86s",
# #       "nonce": 9,
# #       "name": "agreeable-walnut-weasel",
# #       "location": "8c2830ab51653ff",
# #       "last_poc_challenge": 750521,
# #       "last_change_block": 750521,
# #       "geocode": {
# #         "short_street": "Lockton Ln",
# #         "short_state": "CA",
# #         "short_country": "US",
# #         "short_city": "Novato",
# #         "long_street": "Lockton Lane",
# #         "long_state": "California",
# #         "long_country": "United States",
# #         "long_city": "Novato",
# #         "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
# #       },
# #       "block_added": 3805,
# #       "block": 771120,
# #       "address": "11tWRj2Qhnn177iVYm3KUmbPdMyhRfeqHqk9kCyiR7y57hdG9JA"
# #     },
# #     {
# #       "lng": -122.55193831997157,
# #       "lat": 38.1204024903364,
# #       "timestamp_added": "2019-08-01T15:44:31.000000Z",
# #       "status": {
# #         "online": "online",
# #         "listen_addrs": ["/ip4/76.102.181.228/tcp/44159"],
# #         "height": 771118
# #       },
# #       "reward_scale": 1,
# #       "owner": "13buBykFQf5VaQtv7mWj2PBY9Lq4i1DeXhg7C4Vbu3ppzqqNkTH",
# #       "nonce": 7,
# #       "name": "magic-rainbow-wasp",
# #       "location": "8c2830aa2a63dff",
# #       "last_poc_challenge": 771079,
# #       "last_change_block": 771079,
# #       "geocode": {
# #         "short_street": "Morning Star Ct",
# #         "short_state": "CA",
# #         "short_country": "US",
# #         "short_city": "Novato",
# #         "long_street": "Morning Star Court",
# #         "long_state": "California",
# #         "long_country": "United States",
# #         "long_city": "Novato",
# #         "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
# #       },
# #       "block_added": 3301,
# #       "block": 771120,
# #       "address": "112aeWRZdyz61Y7EQeMbXwqERNMPnciDvsxyFmhz1UfA9hte4R4W"
# #     },
# #     {
# #       "lng": -122.52885074963571,
# #       "lat": 38.12129445739087,
# #       "timestamp_added": "1970-01-01T00:00:00.000000Z",
# #       "status": {
# #         "online": "online",
# #         "listen_addrs": ["/ip4/76.102.181.228/tcp/44158"],
# #         "height": 771115
# #       },
# #       "reward_scale": 0.5,
# #       "owner": "13buBykFQf5VaQtv7mWj2PBY9Lq4i1DeXhg7C4Vbu3ppzqqNkTH",
# #       "nonce": 0,
# #       "name": "curly-berry-coyote",
# #       "location": "8c2830aa2529dff",
# #       "last_poc_challenge": 771113,
# #       "last_change_block": 771113,
# #       "geocode": {
# #         "short_street": "Andale Ave",
# #         "short_state": "CA",
# #         "short_country": "US",
# #         "short_city": "Novato",
# #         "long_street": "Andale Avenue",
# #         "long_state": "California",
# #         "long_country": "United States",
# #         "long_city": "Novato",
# #         "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
# #       },
# #       "block_added": 1,
# #       "block": 771120,
# #       "address": "112Z6fYnkQa8VAyMWHoaZJVzrxbWPoJV2NCfdZmaNoG1pYxWdGwD"
# #     },
# #     {
# #       "lng": -122.52885074963571,
# #       "lat": 38.12129445739087,
# #       "timestamp_added": "1970-01-01T00:00:00.000000Z",
# #       "status": {
# #         "online": "online",
# #         "listen_addrs": ["/ip4/76.102.181.228/tcp/44160"],
# #         "height": 768806
# #       },
# #       "reward_scale": 0.5,
# #       "owner": "13buBykFQf5VaQtv7mWj2PBY9Lq4i1DeXhg7C4Vbu3ppzqqNkTH",
# #       "nonce": 0,
# #       "name": "immense-eggplant-stallion",
# #       "location": "8c2830aa2529dff",
# #       "last_poc_challenge": 768733,
# #       "last_change_block": 771071,
# #       "geocode": {
# #         "short_street": "Andale Ave",
# #         "short_state": "CA",
# #         "short_country": "US",
# #         "short_city": "Novato",
# #         "long_street": "Andale Avenue",
# #         "long_state": "California",
# #         "long_country": "United States",
# #         "long_city": "Novato",
# #         "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
# #       },
# #       "block_added": 1,
# #       "block": 771120,
# #       "address": "11VKaN7fEvDm6NaGhcZtNSU1KAQQmTSwuuJsYYEqzh8mSWkoEUd"
# #     }
# #   ]
# # }


#Clear Redis quotes
# from redis import Redis
# from rq import Queue
#
# qfail = Queue(connection=Redis())
# print(qfail.count)
# qfail.empty()
# print(qfail.count)

# from twilio.rest import Client
# from twilio.base.exceptions import *
# import os
#
# account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
# auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
# service_sid = os.environ.get("TWILIO_VERIFY_SERVICE_ID")
#
# client = Client(account_sid, auth_token)
# verification = client.verify \
#                      .services(service_sid) \
#                      .verifications \
#                      .create(to='+9720507751298', channel='sms')
#
# code = str(input("Enter token: "))
#
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

