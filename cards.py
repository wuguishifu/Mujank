import discord
import dataloader


class Card:
    def __init__(self, card_id: str, image_url: str, title: str, rating: int, tags: str):
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

    def to_display_embed(self, author: discord.member.Member):
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
        embed.set_footer(text=f'{num_owned} owned by {author.name}')
        embed.set_image(url='attachment://image.png')
        return embed, file


def to_owned_embed(user: discord.user.User, owned_list: [], page: int):
    description = ''
    index_start = 10 * page
    index_last = 10 * (page + 1)
    for i in owned_list[index_start:index_last]:
        num = i.val()
        card = card_deck.get(i.key()).title
        description += f'{num}x **{card}**\n'
    embed = discord.Embed(
        title=f"{user.name}'s deck",
        description=description,
        colour=discord.Colour.red()
    )
    displayed_id = dataloader.get_displayed_card(user.id)
    if displayed_id == 'c_id_-1':
        file = discord.File('jank-logo.png', 'image.png')
    else:
        file = discord.File(card_deck.get(displayed_id).image_url, 'image.png')
    embed.set_thumbnail(url='attachment://image.png')
    return embed, file


cards = [
    ['c_id_0000', 'cards/alex- _3.jpg', 'Much Love', 3, 'Alex'],
    ['c_id_0001', 'cards/alex- puppy.jpg', 'Wassup Dog', 3, 'Alex'],
    ['c_id_0002', 'cards/anteatery_cup_tower.png', 'The Legendary Tower', 3, 'Misc'],
    ['c_id_0003', 'cards/bo- ac_A.jpg', 'A', 3, 'Bo'],
    ['c_id_0004', 'cards/bo- airpods.jpg', 'Hey, Look at my Airpods!', 3, 'Bo'],
    ['c_id_0005', 'cards/bo- beard.jpg', 'Hey, Look at my Beard!', 3, 'Bo'],
    ['c_id_0006', 'cards/bo- bomomo.png', 'BOmomo', 3, 'Bo'],
    ['c_id_0007', 'cards/bo- cream.jpg', 'Oops, cream!', 3, 'Bo'],
    ['c_id_0008', 'cards/bo- dead_inside_outside.PNG', "he's dead on the inside and the outside", 3, 'Bo'],
    ['c_id_0009', 'cards/bo- death_stare.png', 'Death Stare', 3, 'Bo'],
    ['c_id_0010', 'cards/bo- eggplant.jpg', 'Hey, Look at my Eggplant!', 3, 'Bo'],
    ['c_id_0011', 'cards/bo- full.jpg', "Oh man, I'm optimally full", 3, 'Bo']
]


card_deck = {}
name_deck = {}
for c in cards:
    card_deck[c[0]] = Card(c[0], c[1], c[2], c[3], c[4])
    name_deck[c[2].lower()] = Card(c[0], c[1], c[2], c[3], c[4])
