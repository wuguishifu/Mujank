import discord

import database
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
            if database.check_claimed(str(interaction.user.id)):
                await interaction.channel.send(f'{interaction.user.mention}, you can only claim once every 12 hours!')
            else:
                database.set_claimed(str(interaction.user.id), True)
                database.add_card(str(interaction.user.id), self.card.id)
                embed, file = self.card.to_embed(interaction.user)
                await interaction.response.edit_message(view=None, embed=embed)
                await interaction.channel.send(f'{interaction.user.mention} claimed {self.card.title}!')
        else:
            await interaction.channel.send(f'Only {self.user.mention} can claim this card!')


class NextDeckPageButton(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextDeckPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                     label='Next Page',
                                                     row=0)
        else:
            super(NextDeckPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
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


class PrevDeckPageButton(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == 0:
            super(PrevDeckPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                     label='Previous Page', row=0)
        else:
            super(PrevDeckPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page', row=0)
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


class NextWishlistPageButton(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextWishlistPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                         label='Next Page', row=0)
        else:
            super(NextWishlistPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
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


class PrevWishlistPageButton(discord.ui.Button):
    def __init__(self, card_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(card_list) + 9) / 10)
        if cur_page == 0:
            super(PrevWishlistPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                         label='Previous Page', row=0)
        else:
            super(PrevWishlistPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page',
                                                         row=0)
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
        self.add_item(PrevDeckPageButton(card_list, cur_page, user))
        self.add_item(NextDeckPageButton(card_list, cur_page, user))


class WishlistView(discord.ui.View):
    def __init__(self, card_list: [], user: discord.user.User, cur_page=0):
        super(WishlistView, self).__init__()
        self.add_item(PrevWishlistPageButton(card_list, cur_page, user))
        self.add_item(NextWishlistPageButton(card_list, cur_page, user))


class SearchListView(discord.ui.View):
    def __init__(self, user: discord.user.User, query: str, card_list: [], cur_page=0):
        super(SearchListView, self).__init__()
        self.add_item(PrevSearchListPageButton(user, query, card_list, cur_page))
        self.add_item(NextSearchListPageButton(user, query, card_list, cur_page))
