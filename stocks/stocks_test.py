import matplotlib.pyplot
import numpy as np
import matplotlib as mp

mu = 0.001
sigma = 0.01
start_price = 10

np.random.seed(0)
returns = np.random.normal(loc=mu, scale=sigma, size=10000)
price = start_price*(1+returns).cumprod()

matplotlib.pyplot.plot(price)
matplotlib.pyplot.show()
