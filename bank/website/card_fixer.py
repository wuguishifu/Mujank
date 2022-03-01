import os

for f in os.listdir("./bank/website/cards"):
    r = f.replace(" ", "")
    os.rename(f'./bank/website/cards/{f}', f'./bank/website/cards/{r}')

for f in os.listdir("./bank/website/cards"):
    print(f)
