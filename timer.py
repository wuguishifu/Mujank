import datetime
import shutil

import database
import schedule
import time
from datetime import date


def reset():
    database.reset_all_timers()


def backup(t):
    today = date.today()
    date_format = today.strftime('%m_%d_%Y')
    destination = f'mujank_backup_{date_format}_{t}'
    shutil.copy('mujank_db.json', f'db_backups/{destination}')


schedule.every().day.at('06:00').do(reset)
schedule.every().day.at('18:00').do(reset)
schedule.every().day.at('00:00').do(backup, '00_00')
schedule.every().day.at('12:00').do(backup, '12_00')


while True:
    schedule.run_pending()
    time.sleep(1)
