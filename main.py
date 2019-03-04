from ten_percent import TenPercent
from apscheduler.schedulers.blocking import BlockingScheduler
import codecs

def job():
    tenper = TenPercent()
    ts_codes = tenper.get_10_percent()

    fobj = codecs.open('candidate_stocks.txt', 'w', 'utf-8')
    for code in ts_codes:
        fobj.write('{}\n'.format(code))

    fobj.close()


if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(job, 'cron', day_of_week='mon-fri',  hour=15, minute=15)
    sched.start()


