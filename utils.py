from datetime import datetime, timedelta
from random import randint
import requests as rq
from time import sleep
from main import Miner, Wallet, NewUser, db
from dateutil import parser


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

