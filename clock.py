from apscheduler.schedulers.blocking import BlockingScheduler
from subjects.models import Subject
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('************************************')
    print('This job is run every three minutes.')
    print(Subject.objects.first())


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()