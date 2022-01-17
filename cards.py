import discord
import dataloader


class Card:
    def __init__(self, card_id: int, image_url: str, title: str, rating: int, tags: str):
        self.id = card_id
        self.image_url = image_url
        self.title = title
        self.rating = rating
        self.tags = tags

    def to_embed(self, author: discord.member.Member):
        rolls_left = dataloader.get_num_rolls(author.id)
        if rolls_left == 1:
            rolls_left_text = f'⚠️{rolls_left} roll left! ⚠️'
        else:
            rolls_left_text = f'⚠️{rolls_left} rolls left! ⚠️'

        stars = ''
        for i in range(self.rating):
            stars += '★'

        file = discord.File(self.image_url, filename='image.png')
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.tags}',
            colour=discord.Colour.red(),
        )

        num_owned = dataloader.get_num(author.id, self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}\n{rolls_left_text}')
        embed.set_image(url='attachment://image.png')
        return embed, file


def to_owned_embed(user: discord.user.User, owned_list: [], page: int, card_deck: {}):
    description = ''
    for i in owned_list[page:page + 10]:
        description += f'{dataloader.get_num(user.id, owned_list[i])}x {card_deck[owned_list[i + page]].title}\n'


cards = [
    [2, 'cards/alex- _3.jpg', 'Much Love', 3, 'Alex'],
    [3, 'cards/alex- puppy.jpg', 'Wassup Dog', 3, 'Alex'],
    [4, 'cards/anteatery_cup_tower.png', 'The Legendary Tower', 3, 'Misc'],
    [5, 'cards/bo- ac_A.jpg', 'A', 3, 'Bo'],
    [6, 'cards/bo- airpods.jpg', 'Hey, Look at my Airpods!', 3, 'Bo'],
    [7, 'cards/bo- beard.jpg', 'Hey, Look at my Beard!', 3, 'Bo'],
    [8, 'cards/bo- cream.jpg', 'Oops, cream!', 3, 'Bo'],
]
