import dataloader
import schedule
import time


def reset():
    dataloader.reset_all_timers()


# schedule.every().day.at("00:00").do(reset)
schedule.every().day.at("06:00").do(reset)
# schedule.every().day.at("12:00").do(reset)
schedule.every().day.at("18:00").do(reset)


while True:
    schedule.run_pending()
    time.sleep(1)
