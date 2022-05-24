from datetime import datetime, timedelta
from random import randint
import requests as rq
from time import sleep
from main import db, Miner, Wallet, NewUser, Prices, Post, Comment, Message, Chat
from dateutil import parser
import csv

# new_post = Post(
# 	category="Sell / Trade",
# 	title="several things  for sale",
# 	subtitle="ציוד היקפי",
# 	body="New Senscape miner and RAK Antenna",
# 	approved=True,
# 	time_stamp=datetime.now(),
# 	user_id=1,
# )
# db.session.add(new_post)

# new_comment = Comment(
# 	body="This is a comment",
# 	approved=True,
# 	time_stamp=datetime.now(),
# 	user_id=1,
# 	post_id=1,
# )

# new_chat = Chat(
# 	time_stamp=datetime.now(),
# 	user_1=2,
# 	user_2=1,
# 	hide=False,
# )
# db.session.add(new_chat)
# db.session.commit()

# new_msg = Message(
# 	chat_id=5,
# 	user_id=2,
# 	title="Hi man, I'm good!",
# 	body="very new id 5",
# 	time_stamp=datetime.now(),
# 	recipient=2,
# 	read=False,
# )
# db.session.add(new_msg)
# db.session.commit()

def get_miners_data():
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
	}

	## Get all hotspots in Israel Box
	israel_box = {
		"cursor": None,
		"swlat": 29.4255538961337,
		"swlon": 34.46116814079567,
		"nelat": 33.03202086923252,
		"nelon": 35.613699832312264,
	}

	url = "https://api.helium.io/v1/hotspots/location/box"
	try:
		response = rq.get(url, headers=headers, params=israel_box)
		response.raise_for_status()
	except Exception as ex:
		print(ex)
		sleep(5)
		get_miners_data()

	data = response.json()

	miners = data["data"]
	# print(miners)


	time = datetime.now()
	last_7_days = time - timedelta(days=7)
	last_30_days = time - timedelta(days=30)

	count = 0
	for m in miners:
		sleep(2)
		count += 1
		print(f"{count} - {m['name']}")

		## Get miner's 7 days earinings
		url = f"https://api.helium.io/v1/hotspots/{m['address']}/rewards/sum"
		parameters = {
			"max_time": time.isoformat(),
			"min_time": last_7_days.isoformat(),
		}
		try:
			response = rq.get(url, headers=headers, params=parameters)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} sleep 5 sec")
			sleep(5)
			try:
				response = rq.get(url, headers=headers, params=parameters)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} continue")
				continue

		data_7 = response.json()
		earining_7 = float(data_7["data"]['sum']) / 100000000
		print(earining_7)
		sleep(2)


		## Get miner's 30 days earinings
		url = f"https://api.helium.io/v1/hotspots/{m['address']}/rewards/sum"
		parameters = {
			"max_time": time.isoformat(),
			"min_time": last_30_days.isoformat(),
		}

		try:
			response = rq.get(url, headers=headers, params=parameters)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} sleep 5 sec")
			sleep(5)
			try:
				response = rq.get(url, headers=headers, params=parameters)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} continue")
				continue

		data_30 = response.json()
		earining_30 = float(data_30["data"]['sum']) / 100000000
		print(earining_30)
		sleep(2)

		## Check if wallet exist, if not, create new wallet
		if Wallet.query.filter_by(address=m["owner"]).first() == None:
			new_wallet = Wallet(
				address=m["owner"],
				balance=0,
			)
			db.session.add(new_wallet)
			db.session.commit()
		sleep(2)

		## Update wallet balance
		wallet = Wallet.query.filter_by(address=m["owner"]).first()
		url = f"https://api.helium.io/v1/accounts/{wallet.address}"
		try:
			response = rq.get(url, headers=headers)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} sleep 5 sec")
			sleep(5)
			try:
				response = rq.get(url, headers=headers)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} - continue")
				continue

		wallet_data = response.json()
		balance = int(wallet_data["data"]["balance"]) / 100000000
		if balance == None:
			wallet.balance = 0
		else:
			wallet.balance = balance

		print(f"Updated balnace for {wallet}  is: {balance} HNT")
		sleep(2)

		## Check If miner exist in DB, if not, create it and insert data.
		## If miner exist, update status, location and earnings
		if Miner.query.filter_by(name=m['name']).first() == None:
			if m['geocode']['long_country'] == None:
				country = "Israel"
			else:
				country = m['geocode']['long_country']

			miner = Miner(
				name=m['name'],
				address=m['address'],
				added=parser.parse(m['timestamp_added']),
				city=m['geocode']['long_city'],
				country=country,
				street=m['geocode']['long_street'],
				online=m['status']['online'],
				earnings_7=earining_7,
				earnings_30=earining_30,
				wallet_address=m["owner"],
			)
			db.session.add(miner)

			print(miner)
			print(f"{m['name']} - whole record was added to db\n-------------------------------------------------->")
		else:
			# break  #USE this break to only update the db with new miners
			miner = Miner.query.filter_by(name=m['name']).first()

			if m['geocode']['long_country'] == None:
				country = "Israel"
			else:
				country = m['geocode']['long_country']

			miner.city = m['geocode']['long_city']
			miner.country = country #m['geocode']['long_country']
			miner.street = m['geocode']['long_street']
			miner.online = m['status']['online']
			miner.earnings_7 = earining_7
			miner.earnings_30 = earining_30

			print(miner)
			print("db recored udpated\n-------------------------------------------------->")


		try:
			db.session.commit()
		except Exception as ex:
			print(ex)
			print(ex.args)
			continue


def get_all_hotspots_for_all_wallets():
	wallets = Wallet.query.all()
	# print(wallets)

	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
	}

	count = 0
	for w in wallets:
		url = f"https://api.helium.io/v1/accounts/{w.address}/hotspots"
		try:
			response = rq.get(url, headers=headers)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} - sleep 5 sec")
			sleep(5)
			try:
				response = rq.get(url, headers=headers)
				response.raise_for_status()
			except Exception as ex:
				print(f"{ex} - Continue without update of {w}")
				continue

		miners_for_wallet = response.json()
		for m in miners_for_wallet["data"]:
			time = datetime.now()
			if Miner.query.filter_by(address=m["address"]).first() == None:
				new_miner = Miner(
					name=m['name'],
					address=m['address'],
					added=time,
					city=m['geocode']['long_city'],
					country=m['geocode']['long_country'],
					street=m['geocode']['long_street'],
					online=m['status']['online'],
					earnings_7=0.0,
					earnings_30=0.0,
					wallet_address=m["owner"],
				)
				db.session.add(new_miner)

				print(new_miner)
				print(
					f"{m['name']} - A new, non-Israeli miner was added to db\n------------------------------------>")
			else:
				print(f"Miner {m['name']} already exist in wallet {w.address}")
		db.session.commit()
		sleep(2)


def commit_prices_to_db():
	with open("HNT-USD.csv", newline='') as data:
	    reader = csv.reader(data)
	    count = 0
	    for row in reader:
	        print(row[0], row[4])
	        if count == 0:
	            count += 1
	            continue
	        new_price_entry = Prices(
	            date=row[0],
	            price=row[4]
	        )
	        db.session.add(new_price_entry)
	    db.session.commit()

def update_daily_price():
	"""
	GET LAST DAY AVARAGE HNT PRICES, Checks the latest entry in prices table,
	if exist, it will update it to the current price avarage of that day.
	If not exist, will create a new entry of the new date and will update it to the current price avarage of that day.
	"""
	# print("I update helium price")
	prices = {}
	tmp_date = ""
	tmp_price_list = []
	cursor = ""

	for n in range(3):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
		}

		if not cursor:
			url = "https://api.helium.io/v1/oracle/prices"
		else:
			url = "https://api.helium.io/v1/oracle/prices" + cursor

		try:
			response = rq.get(url, headers=headers)
			response.raise_for_status()
		except Exception as ex:
			print(f"{ex} - sleep 60 sec")

			while True:
				print("second exeption sleep")
				sleep(1)
				try:
					response = rq.get(url, headers=headers)
					response.raise_for_status()
				except Exception as ex:
					print(f"{ex} - Tried to fetch price again with no succses")
					continue
				break

		data = response.json()

		# print(data)
		cursor = f"?cursor={data['cursor']}"
		# print(cursor)

		# print(f"there are {len(data['data'])} price stamps in data['data']")

		for d in data["data"]:
			# date = parser.parse(d["timestamp"]).date()
			date = d["timestamp"][0:10]
			price = round(float(d["price"] / 100000000), 3)

			# print(f"date - {date}")

			if not tmp_date:
				# print(f"tmp_date length - {tmp_date}")
				tmp_date = date
				tmp_price_list.append(price)

			elif date == tmp_date:
				# print(f"tmp_date length - {tmp_date}")
				tmp_price_list.append(price)

			else:
				# print(f"tmp_price_list lentgh - {len(tmp_price_list)}")

				if n == 0 and len(tmp_price_list) < 100:
					avarage_price = sum(tmp_price_list) / len(tmp_price_list)
					print(f"Under 100 {tmp_date} - {avarage_price}")
					prices[str(tmp_date)] = round(avarage_price, 3)

					last_price = Prices.query.filter_by(date=tmp_date).first()

					if last_price != None:
						last_price.price = round(avarage_price, 6)
					else:
						new_price_entry = Prices(
							date=tmp_date,
							price=round(avarage_price, 6)
						)
						db.session.add(new_price_entry)

					db.session.commit()

					tmp_date = ""
					tmp_price_list = []
					break

				elif len(tmp_price_list) > 100:
					avarage_price = sum(tmp_price_list) / len(tmp_price_list)
					print(f"{tmp_date} - {avarage_price}")
					prices[str(tmp_date)] = round(avarage_price, 3)

					last_price = Prices.query.filter_by(date=tmp_date).first()

					if last_price != None:
						last_price.price = round(avarage_price, 6)
					else:
						new_price_entry = Prices(
							date=tmp_date,
							price=round(avarage_price, 6)
						)
						db.session.add(new_price_entry)

					db.session.commit()
					# print(round(avarage_price, 6))
					tmp_date = ""
					tmp_price_list = []
					break

				else:
					# print(f"n = {n} and tmp_price_list lentgh - {len(tmp_price_list)}")
					continue

		sleep(1)
	return prices
