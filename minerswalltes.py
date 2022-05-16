# from datetime import datetime, timedelta
# from random import randint
# import requests as rq
# from time import sleep
# from main import db, Miner, Wallet, NewUser, Prices
# from dateutil import parser
# import csv
from utils import get_miners_data, get_all_hotspots_for_all_wallets


print("I get miners data")
get_miners_data()

print("I get wallets data")
get_all_hotspots_for_all_wallets()