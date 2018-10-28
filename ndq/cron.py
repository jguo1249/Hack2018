import time

import requests
import schedule


def update_articles():
    r = requests.post("http://localhost:8000/update-articles")
    print(r.status_code, r.reason)


update_articles()

schedule.every(1).hour.do(update_articles)

while True:
    schedule.run_pending()
    time.sleep(5)
