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
    def __init__(self, owned_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(owned_list) + 9) / 10)
        if cur_page == num_pages - 1:
            super(NextPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True, label='Next Page',
                                                 row=0)
        else:
            super(NextPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Next Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.owned_list = owned_list

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page + 1 < self.num_pages:
                self.cur_page += 1
                embed, file = cards.to_owned_embed(interaction.user, self.owned_list, self.cur_page)
                await interaction.message.edit(embed=embed, view=DeckView(self.owned_list, self.user, self.cur_page))


class PrevPageButton(discord.ui.Button):
    def __init__(self, owned_list: [], cur_page: int, user: discord.user.User):
        num_pages = int((len(owned_list) + 9) / 10)
        if cur_page == 0:
            super(PrevPageButton, self).__init__(style=discord.ButtonStyle.primary, disabled=True,
                                                 label='Previous Page', row=0)
        else:
            super(PrevPageButton, self).__init__(style=discord.ButtonStyle.primary, label='Previous Page', row=0)
        self.user = user
        self.cur_page = cur_page
        self.num_pages = num_pages
        self.owned_list = owned_list

    async def callback(self, interaction: discord.Interaction):
        if self.user.id == interaction.user.id:
            if self.cur_page - 1 >= 0:
                self.cur_page -= 1
                embed, file = cards.to_owned_embed(interaction.user, self.owned_list, self.cur_page)
                await interaction.message.edit(embed=embed, view=DeckView(self.owned_list, self.user, self.cur_page))


class CardView(discord.ui.View):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super().__init__()
        self.add_item(ClaimButton(card, user))


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DeleteButton())


class DeckView(discord.ui.View):
    def __init__(self, owned_list: [], user: discord.user.User, cur_page=0):
        super().__init__()
        self.add_item(PrevPageButton(owned_list, cur_page, user))
        self.add_item(NextPageButton(owned_list, cur_page, user))
