import discord
from discord.ext import commands

import cards


class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('search.py loaded')

    @commands.command(name='info', aliases=['i', 'im'])
    async def show_card(self, ctx):
        content: str = ctx.message.content
        query = ''
        if content.startswith(f'*info '):
            query = content[6:]
        elif content.startswith(f'*i '):
            query = content[3:]
        elif content.startswith(f'*im '):
            query = content[4:]
        if len(query) > 0:
            if query.lower() in cards.name_deck:
                embed, file = cards.name_deck.get(query.lower()).to_display_embed(ctx.author)
                await ctx.send(embed=embed, file=file)
            else:
                await ctx.send(f'No card named {query} found!')

    @commands.command(name='search', aliases=['s'])
    async def search_list(self, ctx, *args):
        args = [i.lower() for i in args]
        content: str = ctx.message.content
        query = ''
        if content.startswith(f'*search '):
            query = content[8:]
        elif content.startswith(f'*s '):
            query = content[3:]
        if len(query) > 0:
            cards_list = cards.name_search(args)
            if len(cards_list) > 0:
                num_pages = int((len(cards_list) + 9) / 10)
                embed, file = cards.to_search_embed(query, cards_list, 0, num_pages)
                await ctx.send(embed=embed, file=file, view=SearchListView(ctx.author, query, cards_list, 0))
            else:
                await ctx.send('No cards were found.')

    @commands.command(name='searchrarity', aliases=['sr'])
    async def search_rare(self, ctx, rating: str):
        if rating:
            if rating.isnumeric():
                query = int(rating)
                cards_list = cards.rating_search(query)
                if len(cards_list) > 0:
                    num_pages = int((len(cards_list) + 9) / 10)
                    embed, file = cards.to_search_embed(rating, cards_list, 0, num_pages)
                    await ctx.send(embed=embed, file=file, view=SearchListView(ctx.author, rating, cards_list, 0))
                else:
                    await ctx.send('No cards were found.')

    @commands.command(name='categories', aliases=['c'])
    async def categories(self, ctx):
        await ctx.send(
            'The categories are:\nAlex, Misc, Bo, Combo, Flynn, Haroon, Jenn, Matt, Mikey, Nayoung, Nina, Noah, '
            'Patrick, Steven, Tim, Tommy, Wendy, Will, Elijah, Ashwin, John')


class PrevSearch(discord.ui.Button):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page: int):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == 0:
            super(PrevSearch, self).__init__(style=discord.ButtonStyle.primary, disabled=True, label='Previous Page',
                                             row=0)
        else:
            super(PrevSearch, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page', row=0)
        self.query = query
        self.cur_page = cur_page
        self.card_list = card_list
        self.num_pages = num_pages
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page - 1 >= 0:
                self.cur_page -= 1
                embed, file = cards.to_search_embed(self.query, self.card_list, self.cur_page, self.num_pages)
                await interaction.message.edit(embed=embed, view=SearchListView(self.user, self.query, self.card_list,
                                                                                self.cur_page))


class NextSearch(discord.ui.Button):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page: int):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextSearch, self).__init__(style=discord.ButtonStyle.primary, disabled=True, label='Next Page', row=0)
        else:
            super(NextSearch, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
        self.query = query
        self.cur_page = cur_page
        self.card_list = card_list
        self.num_pages = num_pages
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page + 1 < self.num_pages:
                self.cur_page += 1
                embed, file = cards.to_search_embed(self.query, self.card_list, self.cur_page, self.num_pages)
                await interaction.message.edit(embed=embed, view=SearchListView(self.user, self.query, self.card_list,
                                                                                self.cur_page))


class SearchListView(discord.ui.View):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page=0):
        super(SearchListView, self).__init__()
        self.add_item(PrevSearch(user, query, card_list, cur_page))
        self.add_item(NextSearch(user, query, card_list, cur_page))


def setup(bot: commands.Bot):
    bot.add_cog(Search(bot))
