import schedule
import time

def job():
    print("I'm working...")

schedule.every().day.at("00:54").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
    