import discord
from discord.ext import commands

import cards
import database


class Wishlist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print('wishlist.py loaded')

    @commands.command(name='wishadd', aliases=['wa'])
    async def add_wish(self, ctx):
        content: str = ctx.message.content
        query = ''
        if content.startswith(f'*wishadd '):
            query = content[9:]
        elif content.startswith(f'*wa '):
            query = content[4:]
        if len(query) > 0:
            if query.lower() in cards.name_deck:
                database.add_card_to_wishlist(str(ctx.author.id), cards.name_deck.get(query.lower()).id)
                await ctx.send(f"You've added {cards.name_deck.get(query.lower()).title} to your wishlist!")

    @commands.command(name='wishlist', aliases=['wl'])
    async def show_wishlist(self, ctx):
        if ctx.message.mentions:
            user = ctx.message.mentions[0]
        else:
            user = ctx.author
        if database.user_exists(str(user.id)):
            wishlist = database.get_wishlist(str(user.id))
            if len(wishlist) == 0:
                if user.id == ctx.author.id:
                    await ctx.send(f"{user.mention}, you don't have any cards on your wishlist yet!")
                else:
                    await ctx.send(f"{user.mention} doesn't have any cards on their wishlist yet!")
            else:
                num_pages = int((len(wishlist) + 9) / 10)
                embed, file = cards.to_wishlist_embed(user, wishlist, 0, num_pages)
                await ctx.send(embed=embed, file=file, view=WishlistView(wishlist, user, cur_page=0))

    @commands.command(name='wishremove', aliases=['wr'])
    async def remove_wish(self, ctx):
        content: str = ctx.message.content
        query = ''
        if content.startswith(f'*wishremove '):
            query = content[12:]
        elif content.startswith(f'*wr '):
            query = content[4:]
        if len(query) > 0:
            if query.lower() in cards.name_deck:
                database.remove_card_from_wishlist(str(ctx.author.id), cards.name_deck.get(query.lower()).id)
                await ctx.send(f"You've removed {cards.name_deck.get(query.lower()).title} from your wishlist!")


class PrevWish(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == 0:
            super(PrevWish, self).__init__(style=discord.ButtonStyle.primary, disabled=True, label='Previous Page',
                                           row=0)
        else:
            super(PrevWish, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page - 1 >= 0:
                self.cur_page -= 1
                embed, file = cards.to_wishlist_embed(interaction.user, self.card_list, self.cur_page, self.num_pages)
                await interaction.message.edit(embed=embed, view=WishlistView(self.card_list, self.user, self.cur_page))


class NextWish(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextWish, self).__init__(style=discord.ButtonStyle.primary, disabled=True, label='Next Page', row=0)
        else:
            super(NextWish, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page + 1 < self.num_pages:
                self.cur_page += 1
                embed, file = cards.to_wishlist_embed(interaction.user, self.card_list, self.cur_page, self.num_pages)
                await interaction.message.edit(embed=embed, view=WishlistView(self.card_list, self.user, self.cur_page))


class WishlistView(discord.ui.View):
    def __init__(self, card_list: [], user: discord.user.User, cur_page=0):
        super(WishlistView, self).__init__()
        self.add_item(PrevWish(card_list, cur_page, user))
        self.add_item(NextWish(card_list, cur_page, user))


def setup(bot: commands.Bot):
    bot.add_cog(Wishlist(bot))
