import matplotlib.pyplot as plt
import matplotlib.style
import pandas as pd

matplotlib.style.use('ggplot')

database_path = 'mujank_db.json'
bank_path = 'bank/history.csv'

bank = pd.read_csv(bank_path)
bank.plot()

plt.show()
