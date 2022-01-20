import discord
import dataloader
import cards


class DeleteButton(discord.ui.Button):
    def __init__(self):
        super(DeleteButton, self).__init__(style=discord.ButtonStyle.danger, label='Delete', row=0)

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()


class ClaimButton(discord.ui.Button):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super(ClaimButton, self).__init__(style=discord.ButtonStyle.primary, label='Claim', row=0)
        self.user = user
        self.card = card

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.user.id:
            if dataloader.check_claimed(interaction.user.id):
                await interaction.channel.send(f'{interaction.user.mention}, you can only claim once every 12 hours!')
            else:
                dataloader.set_claimed(interaction.user.id, True)
                dataloader.add_card(interaction.user.id, self.card.id)
                embed, file = self.card.to_embed(interaction.user)
                await interaction.response.edit_message(view=None, embed=embed)
                await interaction.channel.send(f'{interaction.user.mention} claimed {self.card.title}!')
        else:
            await interaction.channel.send(f'Only {self.user.mention} can claim this card!')


class NextPageButton(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True, label='Next Page',
                                                 row=0)
        else:
            super(NextPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page + 1 < self.num_pages:
                self.cur_page += 1
                embed, file = cards.to_owned_embed(interaction.user, self.card_list, self.cur_page, self.num_pages)
                await interaction.message.edit(embed=embed, view=DeckView(self.card_list, self.user, self.cur_page))


class PrevPageButton(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == 0:
            super(PrevPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                 label='Previous Page', row=0)
        else:
            super(PrevPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.card_list = card_list

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page - 1 >= 0:
                self.cur_page -= 1
                embed, file = cards.to_owned_embed(interaction.user, self.card_list, self.cur_page, self.num_pages)
                await interaction.message.edit(embed=embed, view=DeckView(self.card_list, self.user, self.cur_page))


class NextSearchListPageButton(discord.ui.Button):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page: int):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextSearchListPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                           label='Next Page', row=0)
        else:
            super(NextSearchListPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
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


class PrevSearchListPageButton(discord.ui.Button):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page: int):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == 0:
            super(PrevSearchListPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                           label='Previous Page', row=0)
        else:
            super(PrevSearchListPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page',
                                                           row=0)
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


class NextSearchSlideshowPageButton(discord.ui.Button):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page: int):
        if cur_page == len(card_list) - 1:
            super(NextSearchSlideshowPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                                label='Next Page', row=0)
        else:
            super(NextSearchSlideshowPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Next Page',
                                                                row=0)
        self.num_pages = len(card_list)
        self.user = user
        self.query = query
        self.card_list = card_list
        self.cur_page = cur_page

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page + 1 < self.num_pages:
                self.cur_page += 1
                embed, file = cards.to_search_slideshow_embed(self.query, self.card_list, self.cur_page)
                await interaction.message.edit(embed=embed, view=SearchSlideshowView(self.user, self.query,
                                                                                     self.card_list, self.cur_page))


class PrevSearchSlideshowPageButton(discord.ui.Button):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page: int):
        if cur_page == 0:
            super(PrevSearchSlideshowPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                                label='Previous Page', row=0)
        else:
            super(PrevSearchSlideshowPageButton, self).__init__(style=discord.ButtonStyle.primary,
                                                                label='Previous Page', row=0)
        self.num_pages = len(card_list)
        self.user = user
        self.query = query
        self.card_list = card_list
        self.cur_page = cur_page

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page - 1 >= 0:
                self.cur_page -= 1
                embed, file = cards.to_search_slideshow_embed(self.query, self.card_list, self.cur_page)
                await interaction.message.edit(embed=embed, view=SearchSlideshowView(self.user, self.query,
                                                                                     self.card_list, self.cur_page))


class CardView(discord.ui.View):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super(CardView, self).__init__()
        self.add_item(ClaimButton(card, user))


class HelpView(discord.ui.View):
    def __init__(self):
        super(HelpView, self).__init__()
        self.add_item(DeleteButton())


class DeckView(discord.ui.View):
    def __init__(self, card_list: [], user: discord.user.User, cur_page=0):
        super(DeckView, self).__init__()
        self.add_item(PrevPageButton(card_list, cur_page, user))
        self.add_item(NextPageButton(card_list, cur_page, user))


class SearchListView(discord.ui.View):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page=0):
        super(SearchListView, self).__init__()
        self.add_item(PrevSearchListPageButton(user, query, card_list, cur_page))
        self.add_item(NextSearchListPageButton(user, query, card_list, cur_page))


class SearchSlideshowView(discord.ui.View):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page=0):
        super(SearchSlideshowView, self).__init__()
        self.add_item(PrevSearchSlideshowPageButton(user, query, card_list, cur_page))
        self.add_item(NextSearchSlideshowPageButton(user, query, card_list, cur_page))
