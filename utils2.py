import requests as rq


def get_oracle_price():
	"""
	API call to Helium, het current HNT price
	:return: current HNT price - float
	"""
	try:
		response = rq.get("https://api.helium.io/v1/oracle/prices/current")
		response.raise_for_status()
	except:
		return 0
	response = response.json()
	price = str(response["data"]["price"])
	hnt = round(int(price) / 100000000 , 2)
	return hnt