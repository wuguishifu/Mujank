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
                await interaction.channel.send(f'{interaction.user.mention}, you can only claim once every 6 hours!')
            else:
                dataloader.set_claimed(interaction.user.id, True)
                dataloader.add_card(interaction.user.id, self.card.id)
                embed, file = self.card.to_embed(interaction.user)
                await interaction.response.edit_message(view=None, embed=embed)
        else:
            await interaction.channel.send(f'Only {self.user.mention} can claim this card!')


class CardView(discord.ui.View):
    def __init__(self, card: cards.Card, user: discord.user.User):
        super().__init__()
        self.add_item(ClaimButton(card, user))


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DeleteButton())
