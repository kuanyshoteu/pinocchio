from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from pytz import utc

sched = BlockingScheduler()
sched.add_job(scheduled_job,'cron',
   day_of_week='mon-sat', hour='03-13',
   timezone='Asia/Almaty')

def scheduled_job():
    print('******************')
    url = 'https://www.bilimtap.kz/subjects/api/update_cards_money?secret=NJf5wefewfm58keijnw'
    requests.get(url,verify=False)

sched.start()