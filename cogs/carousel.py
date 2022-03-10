import discord
from discord.ext import commands

import cards
import database


class Carousel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('carousel.py loaded')

    @commands.command(name='show')
    async def show_deck(self, ctx):
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author
        if database.user_exists(str(user.id)):
            owned_cards = database.get_cards(str(user.id))
            if len(owned_cards) == 0:
                if user.id == ctx.author.id:
                    await ctx.send(f"{user.mention}, you don't have any cards in your deck yet!")
                else:
                    await ctx.send(f"{user.mention} doesn't have any cards in their deck yet!")
            else:
                num_pages = len(owned_cards)
                embed = cards.to_owned_url_display_embed(user, owned_cards, 0, num_pages)
                await ctx.send(embed=embed, view=CarouselView(user, owned_cards, 0))
        else:
            if user.id == ctx.author.id:
                await ctx.send(f'{user.mention}, Please join using the ``*join`` command!')
            else:
                await ctx.send(f'{user.mention} has not joined yet!')


class PrevCarouselView(discord.ui.Button):
    def __init__(self, user: discord.user.User, card_list: [], cur_page=0):
        num_pages = len(card_list)
        if cur_page == 0:
            super(PrevCarouselView, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                   label='Previous Page', row=0)
        else:
            super(PrevCarouselView, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.cur_page - 1 >= 0:
            self.cur_page -= 1
            embed = cards.to_owned_url_display_embed(self.user, self.card_list, self.cur_page, self.num_pages)
            await interaction.message.edit(embed=embed, view=CarouselView(self.user, self.card_list, self.cur_page))


class NextCarouselView(discord.ui.Button):
    def __init__(self, user: discord.user.User, card_list: [], cur_page=0):
        num_pages = len(card_list)
        if cur_page == num_pages - 1:
            super(NextCarouselView, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                   label='Next Page', row=0)
        else:
            super(NextCarouselView, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.cur_page + 1 < self.num_pages:
            self.cur_page += 1
            embed = cards.to_owned_url_display_embed(self.user, self.card_list, self.cur_page, self.num_pages)
            await interaction.message.edit(embed=embed, view=CarouselView(self.user, self.card_list, self.cur_page))


class CarouselView(discord.ui.View):
    def __init__(self, user: discord.user.User, card_list: [], cur_page=0):
        super(CarouselView, self).__init__()
        self.add_item(PrevCarouselView(user, card_list, cur_page))
        self.add_item(NextCarouselView(user, card_list, cur_page))


def setup(bot: commands.Bot):
    bot.add_cog(Carousel(bot))
