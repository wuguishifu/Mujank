import bank
import datetime

now = datetime.datetime.now()
date_format = now.strftime('%m_%d_%Y %H_%M_%S')
bank.update(date_format)
