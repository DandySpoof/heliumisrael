from pytz import utc
from rq import Queue
from worker import conn
from collections.abc import Mapping
from utils import print_every_5_sec, get_miners_data, get_other_wallets_data

from apscheduler.schedulers.blocking import BlockingScheduler

q = Queue(connection=conn)
sched = BlockingScheduler()


@sched.scheduled_job('interval',  hours=1)
def miners_data():
    q.enqueue(get_miners_data)
    # get_miners_data()

@sched.scheduled_job('interval',  hours=2)
def wallets_data():
    q.enqueue(get_other_wallets_data)

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()