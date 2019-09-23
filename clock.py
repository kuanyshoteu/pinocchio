from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('************************************')
    print('This job is run every three minutes.')
    url = 'https://bilimtap.kz/subjects/api/update_cards_money?secret=NJf5wefewfm58keijnw'
    requests.post(url)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()