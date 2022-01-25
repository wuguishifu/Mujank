import csv

import discord


class Item:
    def __init__(self, card_id: str, title: str, price: int, description: str, icon: str, image_url: str):
        self.id = card_id
        self.title = title
        self.price = price
        self.description = description
        self.icon = icon
        self.image_url = image_url

    def to_item_embed(self):
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'Price: {self.price} Jankcoins\n\n{self.description}',
            colour=discord.Colour.from_rgb(227, 24, 24)
        )
        file = discord.File(self.image_url, filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        return embed, file


item_spreadsheet = open('Item spreadsheet.csv')
csvreader = csv.reader(item_spreadsheet)
header = next(csvreader)

item_ids = {}
item_names = {}

for i in csvreader:
    item_ids[i[0]] = Item(i[0], i[1], int(i[2]), i[3], i[4], i[5])
    item_names[i[1].lower()] = Item(i[0], i[1], int(i[2]), i[3], i[4], i[5])
