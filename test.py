import bank
import datetime

now = datetime.datetime.now()
date_format = now.strftime('%m_%d_%Y')
time_format = now.strftime('%m_%d_%Y %H_%M_%S')


bank.backup(date_format)
# bank.update(time_format)
