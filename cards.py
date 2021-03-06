import csv

import discord

import cards
import database

colors = {
    2: discord.Colour.from_rgb(24, 204, 0),
    3: discord.Colour.from_rgb(0, 112, 221),
    4: discord.Colour.from_rgb(163, 53, 238),
    5: discord.Colour.from_rgb(255, 128, 0),
    6: discord.Colour.from_rgb(255, 237, 0)
}


class Card:
    def __init__(self, card_id: str, image_url: str, title: str, rating: int, tags: str, url_url: str):
        self.id = card_id
        self.image_url = image_url
        self.title = title
        self.rating = rating
        self.tags = tags
        self.url_url = url_url

    def to_embed(self, author: discord.member.Member):
        rolls_left = database.get_num_rolls(str(author.id))
        if rolls_left == 1:
            rolls_left_text = f'⚠️{rolls_left} roll left! ⚠️'
        else:
            rolls_left_text = f'⚠️{rolls_left} rolls left! ⚠️'

        stars = ''
        for i in range(self.rating):
            stars += '★'

        color = colors.get(self.rating)
        if 'gif' in self.image_url:
            file = discord.File(self.image_url, filename='image.gif')
        else:
            file = discord.File(self.image_url, filename='image.png')
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.tags}',
            colour=color,
        )

        num_owned = database.get_num(str(author.id), self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}\n{rolls_left_text}')
        if 'gif' in self.image_url:
            embed.set_image(url='attachment://image.gif')
        else:
            embed.set_image(url='attachment://image.png')
        return embed, file

    def to_display_embed(self, author: discord.member.Member):
        stars = ''
        for i in range(self.rating):
            stars += '★'

        color = colors.get(self.rating)
        if 'gif' in self.image_url:
            file = discord.File(self.image_url, filename='image.gif')
        else:
            file = discord.File(self.image_url, filename='image.png')
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.tags}',
            colour=color,
        )

        num_owned = database.get_num(str(author.id), self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}')
        if 'gif' in self.image_url:
            embed.set_image(url='attachment://image.gif')
        else:
            embed.set_image(url='attachment://image.png')
        return embed, file

    def to_url_display_embed(self, author: discord.member.Member):
        stars = ''
        for i in range(self.rating):
            stars += '★'
        color = colors.get(self.rating)
        embed = discord.Embed(
            title=f'{self.title}',
            description=f'{stars}\n{self.tags}',
            colour=color
        )
        num_owned = database.get_num(str(author.id), self.id)
        embed.set_footer(text=f'{num_owned} owned by {author.name}')
        embed.set_image(url=self.url_url)

    def to_owner_list_embed(self, owners: []):
        stars = ''
        for i in range(self.rating):
            stars += '★'

        description = ''
        for o in owners:
            if o.nick:
                description += f'\n{o.nick}'
            else:
                description += f'\n{o.name}'
        embed = discord.Embed(
            title=f'{self.title}\n{stars}',
            description=f'\n**People who own this card:**{description}',
            color=colors.get(self.rating)
        )

        if 'gif' in self.image_url:
            file = discord.File(self.image_url, filename='image.gif')
            embed.set_thumbnail(url='attachment://image.gif')
        else:
            file = discord.File(self.image_url, filename='image.png')
            embed.set_thumbnail(url='attachment://image.png')
        return embed, file


def to_owned_embed(user: discord.user.User, owned_list: [], page: int, num_pages: int):
    description = ''
    index_first = 10 * page
    index_last = 10 * (page + 1)
    for i in list(owned_list)[index_first:index_last]:
        card = card_deck.get(i).title
        description += f'{owned_list[i]}x **{card}**\n'
    embed = discord.Embed(
        title=f"{user.name}’s Deck - Page {page + 1}/{num_pages}",
        description=description,
        colour=discord.Colour.from_rgb(227, 24, 24)
    )
    displayed_id = database.get_displayed_card(str(user.id))
    if displayed_id == 'c_id_-1':
        file = discord.File('mujank-logo.jpg', 'image.png')
        gif = False
    else:
        displayed_card = card_deck.get(displayed_id)
        if 'gif' in displayed_card.image_url:
            file = discord.File(displayed_card.image_url, 'image.gif')
            gif = True
        else:
            file = discord.File(displayed_card.image_url, 'image.png')
            gif = False
    if gif:
        embed.set_thumbnail(url='attachment://image.gif')
    else:
        embed.set_thumbnail(url='attachment://image.png')
    return embed, file


def to_owned_url_display_embed(user: discord.user.User, owned_list: [], page: int, num_pages: int):
    card: Card = cards.card_deck[list(owned_list)[page]]
    stars = ''
    for i in range(card.rating):
        stars += '★'
    description = f'**{card.title}**\n{stars}\n{card.tags}'
    embed = discord.Embed(
        title=f"{user.name}'s Deck - Page {page + 1}/{num_pages}",
        description=description,
        colour=colors[card.rating]
    )
    embed.set_image(url=card.url_url)
    embed.set_footer()
    num_owned = database.get_num(str(user.id), card.id)
    embed.set_footer(text=f'{num_owned} owned by {user.name}')
    return embed


def to_wishlist_embed(user: discord.user.User, wishlist: [], page: int, num_pages: int):
    description = ''
    index_first = 10 * page
    index_last = 10 * (page + 1)
    for i in list(wishlist)[index_first:index_last]:
        card = card_deck.get(i).title
        description += f'{list(wishlist).index(i) + 1}. **{card}**\n'
    embed = discord.Embed(
        title=f"{user.name}’s Wishlist - Page {page + 1}/{num_pages}",
        description=description,
        colour=discord.Colour.from_rgb(227, 24, 24)
    )
    displayed_id = database.get_displayed_card(str(user.id))
    if displayed_id == 'c_id_-1':
        file = discord.File('mujank-logo.jpg', 'image.png')
        gif = False
    else:
        displayed_card = card_deck.get(displayed_id)
        if 'gif' in displayed_card.image_url:
            file = discord.File(displayed_card.image_url, 'image.gif')
            gif = True
        else:
            file = discord.File(displayed_card.image_url, 'image.png')
            gif = False
    if gif:
        embed.set_thumbnail(url='attachment://image.gif')
    else:
        embed.set_thumbnail(url='attachment://image.png')
    return embed, file


def to_search_embed(search_query: str, card_list: [], page: int, num_pages):
    description = ''
    index_first = 10 * page
    index_last = 10 * (page + 1)
    for i in card_list[index_first:index_last]:
        card = i.title
        stars = ''
        for j in range(i.rating):
            stars += '★'
        description += f'{card_list.index(i) + 1}. **{card}** - {stars}\n'
    embed = discord.Embed(
        title=f"Search: {search_query} - Page {page + 1}/{num_pages}",
        description=description,
        colour=discord.Colour.from_rgb(227, 24, 24)
    )
    display_id = card_list[0].id
    display_card = card_deck.get(display_id)
    if 'gif' in display_card.image_url:
        file = discord.File(display_card.image_url, 'image.gif')
        embed.set_thumbnail(url='attachment://image.gif')
    else:
        file = discord.File(display_card.image_url, 'image.png')
        embed.set_thumbnail(url='attachment://image.png')
    return embed, file


def name_search(query: []):
    card_list = []
    for card in card_deck.values():
        if card.tags.lower() in query:
            card_list.append(card)
    return card_list


def rating_search(query: int):
    card_list = []
    for card in card_deck.values():
        if card.rating == query:
            card_list.append(card)
    return card_list


mujank_spreadsheet = open('Mujank spreadsheet.csv')
csvreader = csv.reader(mujank_spreadsheet)
header = next(csvreader)

card_deck = {}
name_deck = {}
rating_decks = {2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

cards_path = f'cards/'
url_path = f'https://mujank.com/img/'

for c in csvreader:
    if int(c[3]) != 0:
        card_deck[c[0]] = Card(c[0], f'{cards_path}{c[1]}', c[2], int(c[3]), c[4], f'{url_path}{c[1]}'.replace(" ", ""))
        name_deck[c[2].lower()] = Card(c[0], f'{cards_path}{c[1]}', c[2], int(c[3]), c[4],
                                       f'{url_path}{c[1]}'.replace(" ", ""))
        name_deck[c[2].lower().replace('’', "'")] = Card(c[0], f'{cards_path}{c[1]}', c[2], int(c[3]), c[4],
                                                         f'{url_path}{c[1]}'.replace(" ", ""))
        rating_decks[int(c[3])][c[0]] = Card(c[0], f'{cards_path}{c[1]}', c[2], int(c[3]), c[4],
                                             f'{url_path}{c[1]}'.replace(" ", ""))

t = ["c_id_0337", "cards/matt- poptart.jpg", "Poptart \*in a British accent\*", 5, "Matt"]
name_deck[t[2].lower().replace('\*', '*')] = Card(t[0], t[1], t[2], t[3], t[4], f'{url_path}{t[1]}'.replace(" ", ""))
