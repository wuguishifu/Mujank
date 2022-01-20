import database
import schedule
import time


def reset():
    database.reset_all_timers()


schedule.every().day.at("06:00").do(reset)
schedule.every().day.at("18:00").do(reset)


while True:
    schedule.run_pending()
    time.sleep(1)
