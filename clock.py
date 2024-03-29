from pytz import utc
from rq import Queue
from worker import conn
from collections.abc import Mapping
from utils import get_miners_data, get_all_hotspots_for_all_wallets, commit_prices_to_db, update_daily_price
from apscheduler.schedulers.blocking import BlockingScheduler

q = Queue(connection=conn)
sched = BlockingScheduler()


# commit_prices_to_db()
# get_miners_data()
# get_all_hotspots_for_all_wallets()
# update_daily_price()


@sched.scheduled_job('interval', hours=3)
def miners_data():
    # print("I update the price chart")
    # update_daily_price()
    print("I get miners data")
    get_miners_data()
    print("I get wallets data")
    get_all_hotspots_for_all_wallets()

# @sched.scheduled_job('interval',  seconds=60)
# def update_price_chart():
#     print("I update the price chart")
#     q.enqueue(update_daily_price)

# @sched.scheduled_job('interval',  hours=6)
# def wallets_data():
#     # q.enqueue(get_other_wallets_data)
#     get_all_hotspots_for_all_wallets()

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()