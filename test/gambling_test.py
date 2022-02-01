import random


def dice(c):
    roll = random.randint(1, 6) + random.randint(1, 6)
    if roll >= 8:
        c += 2
    else:
        c -= 1
    return c


x = []


for i in range(1000):
    coins = 100
    for j in range(1000):
        coins = dice(coins)
    x.append(coins)



