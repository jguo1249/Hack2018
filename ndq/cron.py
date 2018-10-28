import time
from datetime import timedelta

import schedule

jobs = {}

def edit_job(phone, frequency, firstDelivery):
    global jobs
    job_time = firstDelivery
    job_time_str = '{:02d}:{:02d}'.format(firstDelivery.hour,
                                          firstDelivery.minute)
    jobs[phone] = [schedule.every().day.at(job_time_str).do(send, phone=phone)]

    while job_time.hour < 24:
        job_time += timedelta(hours=frequency)
        job_time_str = '{:02d}:{:02d}'.format(firstDelivery.hour,
                                              firstDelivery.minute)
        print(job_time_str)
        jobs[phone].append(schedule.every().day.at(job_time_str).do(send, phone=phone)
        
    return None

edit_job('+15137602878', 3, '2019-08-23 12:00:00')

while True:
    schedule.run_pending()
    time.sleep(1)
