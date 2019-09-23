from apscheduler.schedulers.blocking import BlockingScheduler
from subjects.views import update_cards_money
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('************************************')
    print('This job is run every three minutes.')
    update_cards_money()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()