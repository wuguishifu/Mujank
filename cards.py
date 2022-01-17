import discord
import dataloader


class Card:
    def __init__(self, card_id, image_url, rating, title, description, rarity=1):
        self.id = card_id
        self.image_url = image_url
        self.rating = rating
        self.title = title
        self.description = description
        self.rarity = rarity

    def to_embed(self, author: discord.member.Member):
        stars = ''
        for i in range(self.rating):
            stars += '★'
        file = discord.File(self.image_url, filename='image.png')
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.description}',
            colour=discord.Colour.red(),
        )
        num_owned = dataloader.get_num(author.id, self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}')
        embed.set_image(url='attachment://image.png')
        return embed, file


def to_owned_embed(user: discord.user.User, owned_list: [], page: int, card_deck: {}):
    description = ''
    for i in owned_list[page:page + 10]:
        description += f'{dataloader.get_num(user.id, owned_list[i])}x {card_deck[owned_list[i + page]].title}\n'


cards = [
    [0, 'cards/IMG_0140.jpg', 5, 'Raze', 'Made by Susie'],
]
