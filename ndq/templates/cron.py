import schedule
import time


def update_news_sources():
    print('Updating news sources')


def send():
    print("Sending link to user")


schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(30).to(40).minutes.do(update_news_sources)

while True:
    schedule.run_pending()
    time.sleep(1)
