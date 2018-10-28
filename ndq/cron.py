import time

import schedule

from ndq.news import update_articles

schedule.every(1).hour.do(update_articles)

while True:
    schedule.run_pending()
    time.sleep(5)
