from pytz import utc
from rq import Queue
from worker import conn
from collections.abc import Mapping
from utils import get_miners_data, get_all_hotspots_for_all_wallets, commit_prices_to_db, update_daily_price

from apscheduler.schedulers.blocking import BlockingScheduler

q = Queue(connection=conn)
sched = BlockingScheduler()

# commit_prices_to_db()

@sched.scheduled_job('interval', minutes=10)
def miners_data():
    update_daily_price()
    # q.enqueue(get_miners_data)
    print("I get miners data")
    get_miners_data()
    print("I get wallets data")
    get_all_hotspots_for_all_wallets()

# @sched.scheduled_job('interval',  seconds=10)
# def print_function():
#     print("i print every 10 seconds")

# @sched.scheduled_job('interval',  hours=6)
# def wallets_data():
#     # q.enqueue(get_other_wallets_data)
#     get_all_hotspots_for_all_wallets()

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()