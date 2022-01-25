import shutil
import time
from datetime import date

import schedule

import database


def reset():
    database.reset_all_timers()


def reset_daily():
    database.reset_dailies()


def backup(t):
    today = date.today()
    date_format = today.strftime('%m_%d_%Y')
    destination = f'mujank_backup_{date_format}_{t}'
    shutil.copy('mujank_db.json', f'db_backups/{destination}.json')


schedule.every().day.at('06:00').do(reset)
schedule.every().day.at('18:00').do(reset)
schedule.every().day.at('00:00').do(backup, '00_00')
schedule.every().day.at('12:00').do(backup, '12_00')
schedule.every().day.at('06:00').do(reset_daily)

while True:
    schedule.run_pending()
    time.sleep(1)
