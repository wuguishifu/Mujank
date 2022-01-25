import asyncio
import random

import discord
from discord.ext import commands

import cards
import database
import item

card_price = {2: 1, 3: 1, 4: 3, 5: 15, 6: 30}


class Econ(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print('econ.py loaded')

    @commands.command(name='sell')
    async def sell(self, ctx):
        content: str = ctx.message.content
        query = content[6:]
        if len(query) > 0:

            def confirm(m):
                if m.author == ctx.author:
                    return True

            if query.lower() in cards.name_deck:
                card = cards.name_deck[query.lower()]
                if card.id in database.get_cards(str(ctx.author.id)):
                    await ctx.send(f'Are you sure you would like to sell **{card.title}** '
                                   f'for {card_price[card.rating]} Jankcoins? (yes/no)')
                    try:
                        user_msg = await self.bot.wait_for("message", check=confirm, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(f'No message sent, transaction cancelled.')
                    else:
                        if user_msg.content.lower() in ['yes', 'y']:
                            database.remove_card(str(ctx.author.id), card.id)
                            database.add_coins(str(ctx.author.id), card_price[card.rating])
                            if card_price[card.rating] == 1:
                                await ctx.send(f"{ctx.author.mention}, you've sold **{card.title}** "
                                               f"for {card_price[card.rating]} Jankcoin!")
                            else:
                                await ctx.send(f"{ctx.author.mention}, you've sold **{card.title}** "
                                               f"for {card_price[card.rating]} Jankcoins!")
                        else:
                            await ctx.send(f'Transaction cancelled.')
                else:
                    await ctx.send(f"{ctx.author.mention}, you don't have that card!")
            else:
                await ctx.send(f"{ctx.author.mention}, no cards found named {query}.")

    @commands.command(name='balance', aliases=['bal', 'b'])
    async def check_balance(self, ctx):
        if not ctx.message.mentions:
            balance = database.get_coins(str(ctx.author.id))
            if balance == 1:
                await ctx.send(f'{ctx.author.mention}, your balance is {balance} Jankcoin.')
            else:
                await ctx.send(f'{ctx.author.mention}, your balance is {balance} Jankcoins.')
        else:
            balance = database.get_coins(str(ctx.message.mentions[0].id))
            if balance == 1:
                await ctx.send(f"{ctx.message.mentions[0].mention}'s balance is {balance} Jankcoin.")
            else:
                await ctx.send(f"{ctx.message.mentions[0].mention}'s balance is {balance} Jankcoins.")

    @commands.command(name='price')
    async def check_price(self, ctx):
        content: str = ctx.message.content
        query = ''
        if content.startswith('*price '):
            query = content[7:]
        elif content.startswith('*p '):
            query = content[3:]
        if len(query) > 0:
            if query.lower() in cards.name_deck:
                card = cards.name_deck[query.lower()]
                price = card_price[card.rating]
                if price == 1:
                    await ctx.send(f"{ctx.author.mention}, the selling price of **{card.title}** is {price} Jankcoin.")
                else:
                    await ctx.send(f"{ctx.author.mention}, the selling price of **{card.title}** is {price} Jankcoins.")
            else:
                await ctx.send(f"{ctx.author.mention}, no cards found named {query}.")

    @commands.command(name='prices')
    async def display_prices(self, ctx):
        thumbnail_file = discord.File('mujank-logo.jpg', filename='logo.jpg')
        prices_embed = discord.Embed(
            title='Card Prices',
            description=f'2★ - {card_price[2]} Jankcoins\n'
                        f'3★ - {card_price[3]} Jankcoins\n'
                        f'4★ - {card_price[4]} Jankcoins\n'
                        f'5★ - {card_price[5]} Jankcoins\n'
                        f'6★ - {card_price[6]} Jankcoins',
            colour=discord.Colour.from_rgb(227, 24, 24)
        )
        prices_embed.set_thumbnail(url='attachment://logo.jpg')
        await ctx.send(embed=prices_embed, file=thumbnail_file)

    @commands.command(name='shop', aliases=['store', 'market'])
    async def show_shop(self, ctx):
        thumbnail_file = discord.File('mujank-logo.jpg', filename='logo.jpg')
        description = ''
        for j in list(item.item_ids):
            i = item.item_ids[j]
            description += f'{i.icon} **{i.title}** - {i.price} Jankcoins\n'
        embed = discord.Embed(
            title=':convenience_store: Mujank Marketplace :shopping_cart:',
            description=description,
            colour=discord.Colour.from_rgb(227, 24, 24)
        )
        embed.set_thumbnail(url='attachment://logo.jpg')
        await ctx.send(embed=embed, file=thumbnail_file)

    @commands.command(name='buy')
    async def buy(self, ctx):
        query = ctx.message.content[5:].lower()
        if len(query) > 0:
            if query in item.item_names:
                i = item.item_names[query.lower()]
                balance = database.get_coins(str(ctx.author.id))
                if balance >= i.price:
                    def confirm(s):
                        if s.author == ctx.author:
                            return True

                    await ctx.send(f'{ctx.author.mention}, are you sure you would like to buy **{i.title}** '
                                   f'for {i.price} Jankcoins? (yes/no)')
                    try:
                        user_msg = await self.bot.wait_for("message", check=confirm, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(f'No message sent, transaction cancelled')
                    else:
                        if user_msg.content.lower() in ['yes', 'y']:
                            database.add_item(str(ctx.author.id), i.id)
                            database.remove_coins(str(ctx.author.id), i.price)
                            await ctx.send(f"{ctx.author.mention}, you've bought **{i.title}** for {i.price}"
                                           f" Jankcoins!")
                        else:
                            await ctx.send(f'Transaction cancelled.')
                else:
                    await ctx.send(f"{ctx.author.mention}, you don't have enough Jankcoins to buy that item!")
            else:
                await ctx.send(f'{ctx.author.mention}, no item found called {query}.')

    @commands.command(name='pay', aliases=['p'])
    async def pay(self, ctx, mention, amount='none'):
        if not ctx.message.mentions:
            await ctx.send('Please mention someone to pay!')
        elif not amount.isnumeric():
            await ctx.send('Please enter a number greater than 0.')
        elif int(amount) <= 0:
            await ctx.send('Please enter a number greater than 0.')
        elif ctx.message.mentions[0].id == ctx.author.id:
            await ctx.send('Please mention someone to pay!')
        else:
            amount = int(amount)
            balance = database.get_coins(str(ctx.author.id))
            if balance < amount:
                await ctx.send(f"{ctx.author.mention}, you don't have enough Jankcoins!")
            else:
                database.remove_coins(str(ctx.author.id), amount)
                database.add_coins(str(ctx.message.mentions[0].id), amount)
                await ctx.send(f"{ctx.author.mention}, you've paid {ctx.message.mentions[0].mention} {amount} "
                               f"Jankcoins!")

    @commands.command(name='inventory', aliases=['inv'])
    async def show_inventory(self, ctx):
        inventory = database.get_items(str(ctx.author.id))
        if len(list(inventory)) > 0:
            displayed_card = cards.card_deck[database.get_displayed_card(str(ctx.author.id))]
            description = ''
            for j in list(inventory):
                i = item.item_ids[j]
                description += f'{inventory[j]}x {i.icon} **{i.title}**\n'
            embed = discord.Embed(
                title=f"{ctx.author.name}'s Inventory",
                description=description,
                colour=discord.Colour.from_rgb(227, 24, 24)
            )

            if 'gif' in displayed_card.image_url:
                file = discord.File(displayed_card.image_url, filename='image.gif')
                embed.set_thumbnail(url='attachment://image.gif')
            else:
                file = discord.File(displayed_card.image_url, filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            await ctx.send(embed=embed, file=file)
        else:
            await ctx.send(f"{ctx.author.mention}, your inventory is empty!")

    @commands.command(name='use', aliases=['u'])
    async def use_item(self, ctx):
        content: str = ctx.message.content
        query = ''
        if content.startswith('*u '):
            query = content[3:].lower()
        elif content.startswith('*use '):
            query = content[5:].lower()
        if len(query) > 0:
            if query in list(item.item_names):
                item_to_use = item.item_names[query]

                if item_to_use.id in list(database.get_items(str(ctx.author.id))):
                    def confirm(s):
                        if s.author == ctx.author:
                            return True

                    await ctx.send(f'{ctx.author.mention}, are you sure you want to use {item_to_use.icon} '
                                   f'**{item_to_use.title}**? (yes/no)')
                    try:
                        user_msg = await self.bot.wait_for("message", check=confirm, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send('No message sent, transaction cancelled.')
                    else:
                        if user_msg.content.lower() in ['yes', 'y']:
                            database.remove_item(str(ctx.author.id), item_to_use.id)
                            await execute_item_function(ctx, item_to_use.id)
                        else:
                            await ctx.send('Transaction cancelled.')
                else:
                    await ctx.send(f"{ctx.author.mention}, you don't have any of that item!")
            else:
                await ctx.send(f'{ctx.author.mention}, could not find an item named {query}.')

    @commands.command(name='item')
    async def show_item(self, ctx):
        query = ctx.message.content[6:].lower()
        if len(query) > 0:
            if query in list(item.item_names):
                embed, file = item.item_names[query].to_item_embed()
                await ctx.send(embed=embed, file=file)
            else:
                await ctx.send(f"{ctx.author.mention}, could not find an item named {query}.")


async def execute_item_function(ctx, item_id):
    card = None
    if item_id == 'i_id_0000':  # 2-star roll
        card = random.choice(list(cards.rating_decks[2].values()))
    if item_id == 'i_id_0001':  # 3-star roll
        card = random.choice(list(cards.rating_decks[3].values()))
    if item_id == 'i_id_0002':  # 4-star roll
        card = random.choice(list(cards.rating_decks[4].values()))
    if item_id == 'i_id_0003':  # 5-star roll
        card = random.choice(list(cards.rating_decks[5].values()))
    if item_id == 'i_id_0004':  # 6-star roll
        card = random.choice(list(cards.rating_decks[6].values()))
    embed, file = make_free_roll_card(card, ctx.author)
    await ctx.send(embed=embed, view=CardView(card, ctx.author), file=file)


def make_free_roll_card(card: cards.Card, author: discord.user.User):
    stars = ''
    for i in range(card.rating):
        stars += '★'
    color = cards.colors[card.rating]
    embed = discord.Embed(
        title=f'{card.title}',
        description=f'{stars}\n{card.tags}',
        colour=color
    )
    if 'gif' in card.image_url:
        file = discord.File(card.image_url, filename='image.gif')
        embed.set_image(url='attachment://image.gif')
    else:
        file = discord.File(card.image_url, filename='image.png')
        embed.set_image(url='attachment://image.png')
    num_owned = database.get_num(str(author.id), card.id)
    embed.set_footer(text=f'{num_owned} owned by {author.name}')
    return embed, file


class CardView(discord.ui.View):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super(CardView, self).__init__()
        self.add_item(ClaimButton(card, user))


class ClaimButton(discord.ui.Button):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super(ClaimButton, self).__init__(style=discord.ButtonStyle.primary, label='Claim (free)', row=0)
        self.user = user
        self.card = card

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            database.add_card(str(interaction.user.id), self.card.id)
            embed, file = make_free_roll_card(self.card, interaction.user)
            await interaction.response.edit_message(view=None, embed=embed)
            await interaction.channel.send(f'{interaction.user.mention} claimed {self.card.title}!')
        else:
            await interaction.channel.send(f'Only {self.user.mention} can claim this card!')


def setup(bot: commands.Bot):
    bot.add_cog(Econ(bot))
