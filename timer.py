import dataloader
import schedule
import time


def reset():
    dataloader.reset_all_timers()


schedule.every(6).hours.do(reset)

while True:
    schedule.run_pending()
    time.sleep(1)
