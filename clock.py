from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sat', hour=02:40, timezone='Asia/Almaty')
def scheduled_job():
    print('******************')
    url = 'https://www.bilimtap.kz/subjects/api/update_cards_money?secret=NJf5wefewfm58keijnw'
    requests.get(url,verify=False)

sched.start()