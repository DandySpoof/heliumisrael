from datetime import datetime, timedelta
from main import Prices, db
from dateutil import parser
from time import sleep
import requests as rq
import csv
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


# Clear Redis quotes
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

# from datetime import datetime,date, time
#
# print(datetime.now())

#     # data = {"data": [{"timestamp": "2022-05-08T12:00:16.000000Z", "price": 1401670000, "block": 1346030},
#     #                  {"timestamp": "2022-05-08T11:30:29.000000Z", "price": 1399800000, "block": 1346000},
#     #                  {"timestamp": "2022-05-08T11:20:39.000000Z", "price": 1395000000, "block": 1345990},
#     #                  {"timestamp": "2022-05-08T11:10:49.000000Z", "price": 1392792500, "block": 1345980},
#     #                  {"timestamp": "2022-05-08T10:40:54.000000Z", "price": 1393000000, "block": 1345950},
#     #                  {"timestamp": "2022-05-08T10:30:21.000000Z", "price": 1392191000, "block": 1345940},
#     #                  {"timestamp": "2022-05-08T10:20:29.000000Z", "price": 1394105000, "block": 1345930},
#     #                  {"timestamp": "2022-05-08T10:10:36.000000Z", "price": 1394640000, "block": 1345920},
#     #                  {"timestamp": "2022-05-08T09:49:22.000000Z", "price": 1388000000, "block": 1345900},
#     #                  {"timestamp": "2022-05-08T09:39:32.000000Z", "price": 1387200000, "block": 1345890},
#     #                  {"timestamp": "2022-05-08T09:20:08.000000Z", "price": 1389000000, "block": 1345870},
#     #                  {"timestamp": "2022-05-08T09:11:01.000000Z", "price": 1388000000, "block": 1345860},
#     #                  {"timestamp": "2022-05-08T09:02:41.000000Z", "price": 1389000000, "block": 1345850},
#     #                  {"timestamp": "2022-05-08T08:50:34.000000Z", "price": 1391000000, "block": 1345840},
#     #                  {"timestamp": "2022-05-08T08:40:55.000000Z", "price": 1397794000, "block": 1345830},
#     #                  {"timestamp": "2022-05-08T08:11:02.000000Z", "price": 1400000000, "block": 1345800},
#     #                  {"timestamp": "2022-05-08T08:01:06.000000Z", "price": 1399064000, "block": 1345790},
#     #                  {"timestamp": "2022-05-08T07:51:25.000000Z", "price": 1384355000, "block": 1345780},
#     #                  {"timestamp": "2022-05-08T07:31:05.000000Z", "price": 1382045000, "block": 1345760},
#     #                  {"timestamp": "2022-05-08T07:01:11.000000Z", "price": 1380000000, "block": 1345730},
#     #                  {"timestamp": "2022-05-08T06:51:13.000000Z", "price": 1377977500, "block": 1345720},
#     #                  {"timestamp": "2022-05-08T06:40:53.000000Z", "price": 1377000000, "block": 1345710},
#     #                  {"timestamp": "2022-05-08T06:31:00.000000Z", "price": 1385388750, "block": 1345700},
#     #                  {"timestamp": "2022-05-08T06:21:19.000000Z", "price": 1387078750, "block": 1345690},
#     #                  {"timestamp": "2022-05-08T06:10:59.000000Z", "price": 1387420000, "block": 1345680},
#     #                  {"timestamp": "2022-05-08T06:01:09.000000Z", "price": 1388758750, "block": 1345670},
#     #                  {"timestamp": "2022-05-08T05:52:04.000000Z", "price": 1391754500, "block": 1345660},
#     #                  {"timestamp": "2022-05-08T05:40:47.000000Z", "price": 1393000000, "block": 1345650},
#     #                  {"timestamp": "2022-05-08T05:30:50.000000Z", "price": 1392486250, "block": 1345640},
#     #                  {"timestamp": "2022-05-08T05:20:57.000000Z", "price": 1387500000, "block": 1345630},
#     #                  {"timestamp": "2022-05-08T05:11:26.000000Z", "price": 1386220000, "block": 1345620},
#     #                  {"timestamp": "2022-05-08T05:00:55.000000Z", "price": 1380429500, "block": 1345610},
#     #                  {"timestamp": "2022-05-08T04:51:00.000000Z", "price": 1376615000, "block": 1345600},
#     #                  {"timestamp": "2022-05-08T04:41:24.000000Z", "price": 1379621250, "block": 1345590},
#     #                  {"timestamp": "2022-05-08T04:30:34.000000Z", "price": 1379670000, "block": 1345580},
#     #                  {"timestamp": "2022-05-08T04:20:42.000000Z", "price": 1375815000, "block": 1345570},
#     #                  {"timestamp": "2022-05-08T04:10:48.000000Z", "price": 1369447000, "block": 1345560},
#     #                  {"timestamp": "2022-05-08T03:59:57.000000Z", "price": 1372568750, "block": 1345550},
#     #                  {"timestamp": "2022-05-08T03:50:00.000000Z", "price": 1366105000, "block": 1345540},
#     #                  {"timestamp": "2022-05-08T03:40:06.000000Z", "price": 1362605000, "block": 1345530},
#     #                  {"timestamp": "2022-05-08T03:28:45.000000Z", "price": 1365483250, "block": 1345520},
#     #                  {"timestamp": "2022-05-08T03:18:51.000000Z", "price": 1377550000, "block": 1345510},
#     #                  {"timestamp": "2022-05-08T03:09:01.000000Z", "price": 1381132500, "block": 1345500},
#     #                  {"timestamp": "2022-05-08T02:57:24.000000Z", "price": 1387000000, "block": 1345490},
#     #                  {"timestamp": "2022-05-08T02:48:06.000000Z", "price": 1387310000, "block": 1345480},
#     #                  {"timestamp": "2022-05-08T02:38:39.000000Z", "price": 1387000000, "block": 1345470},
#     #                  {"timestamp": "2022-05-08T02:27:12.000000Z", "price": 1385375000, "block": 1345460},
#     #                  {"timestamp": "2022-05-08T02:08:55.000000Z", "price": 1387000000, "block": 1345440},
#     #                  {"timestamp": "2022-05-08T01:59:36.000000Z", "price": 1386195000, "block": 1345430},
#     #                  {"timestamp": "2022-05-08T01:49:56.000000Z", "price": 1391467500, "block": 1345420},
#     #                  {"timestamp": "2022-05-08T01:39:35.000000Z", "price": 1394040000, "block": 1345410},
#     #                  {"timestamp": "2022-05-08T01:30:20.000000Z", "price": 1398816250, "block": 1345400},
#     #                  {"timestamp": "2022-05-08T01:21:17.000000Z", "price": 1400820000, "block": 1345390},
#     #                  {"timestamp": "2022-05-08T01:00:35.000000Z", "price": 1400000000, "block": 1345370},
#     #                  {"timestamp": "2022-05-08T00:50:52.000000Z", "price": 1399918750, "block": 1345360},
#     #                  {"timestamp": "2022-05-08T00:39:54.000000Z", "price": 1403845000, "block": 1345350},
#     #                  {"timestamp": "2022-05-08T00:30:16.000000Z", "price": 1399736000, "block": 1345340},
#     #                  {"timestamp": "2022-05-08T00:20:50.000000Z", "price": 1381615000, "block": 1345330},
#     #                  {"timestamp": "2022-05-08T00:12:10.000000Z", "price": 1380115000, "block": 1345320},
#     #                  {"timestamp": "2022-05-08T00:00:24.000000Z", "price": 1402030000, "block": 1345310},
#     #                  {"timestamp": "2022-05-07T23:50:34.000000Z", "price": 1408105500, "block": 1345300},
#     #                  {"timestamp": "2022-05-07T23:41:36.000000Z", "price": 1415649500, "block": 1345290},
#     #                  {"timestamp": "2022-05-07T23:30:28.000000Z", "price": 1418220000, "block": 1345280},
#     #                  {"timestamp": "2022-05-07T23:20:38.000000Z", "price": 1427462000, "block": 1345270},
#     #                  {"timestamp": "2022-05-07T23:10:48.000000Z", "price": 1430381000, "block": 1345260},
#     #                  {"timestamp": "2022-05-07T23:01:52.000000Z", "price": 1436671250, "block": 1345250},
#     #                  {"timestamp": "2022-05-07T22:50:44.000000Z", "price": 1448260000, "block": 1345240},
#     #                  {"timestamp": "2022-05-07T22:40:53.000000Z", "price": 1447638750, "block": 1345230},
#     #                  {"timestamp": "2022-05-07T22:31:11.000000Z", "price": 1440658500, "block": 1345220},
#     #                  {"timestamp": "2022-05-07T22:20:48.000000Z", "price": 1439798500, "block": 1345210},
#     #                  {"timestamp": "2022-05-07T22:11:34.000000Z", "price": 1440682500, "block": 1345200},
#     #                  {"timestamp": "2022-05-07T22:03:14.000000Z", "price": 1440605000, "block": 1345190},
#     #                  {"timestamp": "2022-05-07T21:50:43.000000Z", "price": 1443746500, "block": 1345180},
#     #                  {"timestamp": "2022-05-07T21:40:53.000000Z", "price": 1444385000, "block": 1345170},
#     #                  {"timestamp": "2022-05-07T21:31:03.000000Z", "price": 1445700000, "block": 1345160},
#     #                  {"timestamp": "2022-05-07T21:20:46.000000Z", "price": 1450609000, "block": 1345150},
#     #                  {"timestamp": "2022-05-07T21:10:56.000000Z", "price": 1453993750, "block": 1345140},
#     #                  {"timestamp": "2022-05-07T21:01:06.000000Z", "price": 1455673750, "block": 1345130},
#     #                  {"timestamp": "2022-05-07T20:52:19.000000Z", "price": 1454671250, "block": 1345120},
#     #                  {"timestamp": "2022-05-07T20:40:07.000000Z", "price": 1456261500, "block": 1345110},
#     #                  {"timestamp": "2022-05-07T20:30:17.000000Z", "price": 1457870000, "block": 1345100},
#     #                  {"timestamp": "2022-05-07T20:20:27.000000Z", "price": 1458481250, "block": 1345090},
#     #                  {"timestamp": "2022-05-07T20:10:37.000000Z", "price": 1458566250, "block": 1345080},
#     #                  {"timestamp": "2022-05-07T20:00:47.000000Z", "price": 1459000000, "block": 1345070},
#     #                  {"timestamp": "2022-05-07T19:40:36.000000Z", "price": 1468465000, "block": 1345050},
#     #                  {"timestamp": "2022-05-07T19:30:46.000000Z", "price": 1466835000, "block": 1345040},
#     #                  {"timestamp": "2022-05-07T19:21:05.000000Z", "price": 1462840000, "block": 1345030},
#     #                  {"timestamp": "2022-05-07T19:10:54.000000Z", "price": 1462900000, "block": 1345020},
#     #                  {"timestamp": "2022-05-07T19:00:57.000000Z", "price": 1461573750, "block": 1345010},
#     #                  {"timestamp": "2022-05-07T18:51:00.000000Z", "price": 1465640250, "block": 1345000},
#     #                  {"timestamp": "2022-05-07T18:40:51.000000Z", "price": 1466280000, "block": 1344990},
#     #                  {"timestamp": "2022-05-07T18:30:51.000000Z", "price": 1464742250, "block": 1344980},
#     #                  {"timestamp": "2022-05-07T18:20:51.000000Z", "price": 1464576250, "block": 1344970},
#     #                  {"timestamp": "2022-05-07T18:10:50.000000Z", "price": 1463000000, "block": 1344960},
#     #                  {"timestamp": "2022-05-07T18:00:45.000000Z", "price": 1462115000, "block": 1344950},
#     #                  {"timestamp": "2022-05-07T17:50:55.000000Z", "price": 1462012500, "block": 1344940},
#     #                  {"timestamp": "2022-05-07T17:41:48.000000Z", "price": 1463033750, "block": 1344930},
#     #                  {"timestamp": "2022-05-07T17:30:47.000000Z", "price": 1463337500, "block": 1344920},
#     #                  {"timestamp": "2022-05-07T17:20:56.000000Z", "price": 1464283000, "block": 1344910},
#     #                  {"timestamp": "2022-05-07T17:11:05.000000Z", "price": 1465000000, "block": 1344900}],
#     #         "cursor": "eyJiZWZvcmUiOjEzNDQ5MDB9"}

##----------- GET LAST DAY AVARAGE HNT PRICES  - CODE WORKS, BUT EXTERNAL API SERVICE SHUT DOWN APTER 5 CALLS ----------------

# def update_daily_price():
# 	prices = {}
# 	tmp_date = ""
# 	tmp_price_list = []
# 	cursor = ""
#
# 	for n in range(3):
# 	    headers = {
# 	        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
# 	    }
#
# 	    if not cursor:
# 	        url = "https://api.helium.io/v1/oracle/prices"
# 	    else:
# 	        url = "https://api.helium.io/v1/oracle/prices" + cursor
#
# 	    try:
# 	        response = rq.get(url, headers=headers)
# 	        response.raise_for_status()
# 	    except Exception as ex:
# 	        print(f"{ex} - sleep 60 sec")
#
# 	        while True:
# 	            print("second exeption sleep")
# 	            sleep(1)
# 	            try:
# 	                response = rq.get(url, headers=headers)
# 	                response.raise_for_status()
# 	            except Exception as ex:
# 	                print(f"{ex} - Tried to fetch price again with no succses")
# 	                continue
# 	            break
#
# 	    data = response.json()
#
#
# 	    # print(data)
# 	    cursor = f"?cursor={data['cursor']}"
# 	    # print(cursor)
#
# 	    # print(f"there are {len(data['data'])} price stamps in data['data']")
#
# 	    for d in data["data"]:
# 	        # date = parser.parse(d["timestamp"]).date()
# 	        date = d["timestamp"][0:10]
# 	        price = round(float(d["price"] / 100000000),3)
#
# 	        # print(f"date - {date}")
#
# 	        if not tmp_date:
# 	            # print(f"tmp_date length - {tmp_date}")
# 	            tmp_date = date
# 	            tmp_price_list.append(price)
#
# 	        elif date == tmp_date:
# 	            # print(f"tmp_date length - {tmp_date}")
# 	            tmp_price_list.append(price)
#
# 	        else:
# 	            # print(f"tmp_price_list lentgh - {len(tmp_price_list)}")
#
# 	            if n == 0 and len(tmp_price_list) < 100:
# 	                avarage_price = sum(tmp_price_list) / len(tmp_price_list)
# 	                print(f"Under 100 {tmp_date} - {avarage_price}")
# 	                prices[str(tmp_date)] = round(avarage_price, 3)
#
# 	                last_price = Prices.query.filter_by(date=tmp_date).first()
#
# 	                if last_price != None:
# 		                last_price.price = round(avarage_price, 6)
# 	                else:
# 		                new_price_entry = Prices(
# 			                date=tmp_date,
# 			                price=round(avarage_price, 6)
# 		                )
# 		                db.session.add(new_price_entry)
#
# 	                db.session.commit()
#
# 	                tmp_date = ""
# 	                tmp_price_list = []
# 	                break
#
# 	            elif len(tmp_price_list) > 100:
# 	                avarage_price = sum(tmp_price_list) / len(tmp_price_list)
# 	                print(f"{tmp_date} - {avarage_price}")
# 	                prices[str(tmp_date)] = round(avarage_price, 3)
#
# 	                last_price = Prices.query.filter_by(date=tmp_date).first()
#
# 	                if last_price != None:
# 	                    last_price.price = round(avarage_price, 6)
# 	                else:
# 		                new_price_entry = Prices(
# 		                    date=tmp_date,
# 		                    price=round(avarage_price, 6)
# 		                )
# 		                db.session.add(new_price_entry)
#
# 	                db.session.commit()
#
# 	                tmp_date = ""
# 	                tmp_price_list = []
# 	                break
#
# 	            else:
# 	                # print(f"n = {n} and tmp_price_list lentgh - {len(tmp_price_list)}")
# 	                continue
#
#
# 	    sleep(1)
# 	print(prices)


#------- ENTER HISTORICAL HNT PRICES FROM FILE TO DB (YAHOO FINANCE) -------------------
#
# with open("HNT-USD.csv", newline='') as data:
#     reader = csv.reader(data)
#     count = 0
#     for row in reader:
#         print(row[0], row[4])
#         if count == 0:
#             count += 1
#             continue
#         new_price_entry = Prices(
#             date=row[0],
#             price=row[4]
#         )
#         db.session.add(new_price_entry)
#     db.session.commit()