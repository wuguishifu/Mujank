import discord


class Card:
    def __init__(self, card_id, image_url, rating, title, description, rarity=1):
        self.id = card_id
        self.image_url = image_url
        self.rating = rating
        self.title = title
        self.description = description
        self.rarity = rarity

    def to_embed(self):
        stars = ''
        for i in range(self.rating):
            stars += '★'
        embed = discord.Embed(
            title=f'{self.title}\n{stars}',
            description=self.description,
            colour=discord.Colour.red()
        )
        embed.set_image(url=self.image_url)
        return embed


card_deck = [[0, 'https://media.discordapp.net/attachments/932061869911453696/932061898441125888/IMG_0140.jpg',
              5, 'Raze', 'Made by Susie']]
