import cards
import os
import csv

print(f'number of each rating: {[len(i) for i in cards.rating_decks.values()]}')

file = open('Mujank spreadsheet.csv')
csvreader = csv.reader(file)
header = next(csvreader)
for element in csvreader:
    if not os.path.exists(f'cards/{element[1]}'):
        print(element)
