import datetime
import random

import discord
from discord.ext import commands

import cards
import database

rates = {2: 480, 3: 880, 4: 980, 5: 995, 6: 1000}

admin = [933726675974381578, 200454087148437504, 937450639506669589]
rolling_channels = [933224926712836116, 932934074270642187, 934997810242265108]


class Deck(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print('deck.py loaded')

    @commands.command(name='roll', aliases=['r'])
    async def roll(self, ctx):
        if ctx.channel.id in rolling_channels:
            if database.user_exists(str(ctx.author.id)):
                if database.get_num_rolls(str(ctx.author.id)) > 0:
                    database.dec_rolls(str(ctx.author.id))
                    random_number = random.randint(1, 1000)
                    card = None
                    if random_number < rates.get(2):
                        card = random.choice(list(cards.rating_decks[2].values()))
                    elif random_number < rates.get(3):
                        card = random.choice(list(cards.rating_decks[3].values()))
                    elif random_number < rates.get(4):
                        card = random.choice(list(cards.rating_decks[4].values()))
                    elif random_number < rates.get(5):
                        card = random.choice(list(cards.rating_decks[5].values()))
                    elif random_number < rates.get(6):
                        card = random.choice(list(cards.rating_decks[6].values()))
                    embed, file = card.to_embed(ctx.author)
                    await ctx.send(embed=embed, view=CardView(card, ctx.author), file=file)
                else:
                    wait_response = get_time_until_reset()
                    await ctx.send(f'{ctx.author.mention}, you can only roll {database.max_rolls} '
                                   f'times every 12 hours!\n{wait_response}')
            else:
                await ctx.send(f'{ctx.author.mention}, please join using the ``*join`` command!')
        else:
            await ctx.send(f'{ctx.author.mention}, please roll in the rolling channel!')

    @commands.command(name='deck', aliases=['d'])
    async def show_deck(self, ctx):
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author
        caller = ctx.author
        if database.user_exists(str(user.id)):
            owned_cards = database.get_cards(str(user.id))
            if len(owned_cards) == 0:
                if user.id == ctx.author.id:
                    await ctx.send(f"{user.mention}, you don't have any cards yet!")
                else:
                    await ctx.send(f"{user.mention} doesn't have any cards in their deck yet!")
            else:
                num_pages = int((len(owned_cards) + 9) / 10)
                embed, file = cards.to_owned_embed(user, owned_cards, 0, num_pages)
                await ctx.send(embed=embed, file=file, view=DeckView(owned_cards, caller, user, cur_page=0))
        else:
            if user.id == ctx.author.id:
                await ctx.send(f'{user.mention}, Please join using the ``*join`` command!')
            else:
                await ctx.send(f'{user.mention} has not joined yet!')

    @commands.command(name='display')
    async def set_displayed_card(self, ctx):
        content: str = ctx.message.content
        query = content[9:].lower().replace('‘', "'").replace('’', "'")
        if len(query) > 0:
            if query in cards.name_deck:
                if database.has_card(str(ctx.author.id), cards.name_deck.get(query).id):
                    database.set_displayed_card(str(ctx.author.id), cards.name_deck.get(query).id)
                    await ctx.send(f'Successfully set your display card to {cards.name_deck.get(query).title}!')
                else:
                    await ctx.send(f"You don't own that card yet!")
            elif query == 'reset':
                database.set_displayed_card(str(ctx.author.id), 'c_id_-1')
                await ctx.send(f'Your deck display was reset!')
            else:
                await ctx.send(f'No card named {query} found!')

    @commands.command(name='ownerslist', aliases=['ol'])
    async def display_owners(self, ctx):
        content: str = ctx.message.content
        query = ''
        if content.startswith('*ownerslist '):
            query = content[12:].lower().replace('‘', "'").replace('’', "'")
        elif content.startswith('*ol '):
            query = content[4:].lower().replace('‘', "'").replace('’', "'")
        if query in cards.name_deck:
            card = cards.name_deck[query]
            card_owners = database.get_owners(card.id)
            user_list = []
            for owner in card_owners:
                try:
                    member = await ctx.guild.fetch_member(int(owner))
                except discord.HTTPException:
                    pass
                else:
                    user_list.append(member)
            if len(user_list) > 0:
                embed, file = card.to_owner_list_embed(user_list)
                await ctx.send(embed=embed, file=file)
            else:
                await ctx.send(f"No one owns {card.title} yet!")
        else:
            await ctx.send(f"No card named {query} found!")


class ClaimButton(discord.ui.Button):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super(ClaimButton, self).__init__(style=discord.ButtonStyle.primary, label='Claim', row=0)
        self.user = user
        self.card = card

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            if database.check_claimed(str(interaction.user.id)):
                await interaction.channel.send(f'{interaction.user.mention}, you can only claim once every 12 hours!')
                embed, file = self.card.to_embed(interaction.user)
                await interaction.response.edit_message(view=None, embed=embed)
            else:
                database.set_claimed(str(interaction.user.id), True)
                database.add_card(str(interaction.user.id), self.card.id)
                embed, file = self.card.to_embed(interaction.user)
                await interaction.response.edit_message(view=None, embed=embed)
                await interaction.channel.send(f'{interaction.user.mention} claimed {self.card.title}!')
        else:
            await interaction.channel.send(f'Only {self.user.mention} can claim this card!')


class PrevDeck(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User, caller: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == 0:
            super(PrevDeck, self).__init__(style=discord.ButtonStyle.primary, disabled=True, label='Previous Page',
                                           row=0)
        else:
            super(PrevDeck, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page', row=0)
        self.user = user
        self.caller = caller
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.cur_page - 1 >= 0:
            self.cur_page -= 1
            embed, file = cards.to_owned_embed(interaction.user, self.card_list, self.cur_page, self.num_pages)
            await interaction.message.edit(embed=embed,
                                           view=DeckView(self.card_list, self.user, self.caller, self.cur_page))


class NextDeck(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User, caller: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextDeck, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                           label='Next Page',
                                           row=0)
        else:
            super(NextDeck, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
        self.user = user
        self.caller = caller
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.cur_page + 1 < self.num_pages:
            self.cur_page += 1
            embed, file = cards.to_owned_embed(interaction.user, self.card_list, self.cur_page, self.num_pages)
            await interaction.message.edit(embed=embed,
                                           view=DeckView(self.card_list, self.user, self.caller, self.cur_page))


class CardView(discord.ui.View):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super(CardView, self).__init__()
        self.add_item(ClaimButton(card, user))


class DeckView(discord.ui.View):
    def __init__(self, card_list: [], user: discord.user.User, caller: discord.user.User, cur_page=0):
        super(DeckView, self).__init__()
        self.add_item(PrevDeck(card_list, cur_page, user, caller))
        self.add_item(NextDeck(card_list, cur_page, user, caller))


def get_time_until_reset():
    current_hour = datetime.datetime.now().hour
    current_min = datetime.datetime.now().minute
    if current_hour < 6:
        response_string = get_time_delta(current_hour, current_min, 6)
    elif current_hour < 18:
        response_string = get_time_delta(current_hour, current_min, 18)
    else:
        response_string = get_time_delta(current_hour, current_min, 30)
    return response_string


def get_time_delta(current_hour, current_min, target_hour):
    if current_min != 0:
        hour_delta = target_hour - current_hour - 1
        min_delta = 60 - current_min
        hour_string = f'{hour_delta} hours' if hour_delta != 1 else f'{hour_delta} hour'
        min_string = f'{min_delta} minutes' if min_delta != 1 else f'{min_delta} minutes'
        if hour_delta == 0:
            return f'There is currently {min_string} until roll reset.'
        else:
            return f'There is currently {hour_string} and {min_string} until roll reset.'
    else:
        hour_delta = target_hour - current_hour
        hour_string = f'{hour_delta} hours' if hour_delta != 1 else f'{hour_delta} hour'
        return f'There is currently {hour_string} until roll reset.'


def setup(bot: commands.Bot):
    bot.add_cog(Deck(bot))
