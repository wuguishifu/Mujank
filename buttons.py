import discord
import dataloader
import cards


class DeleteButton(discord.ui.Button):
    def __init__(self):
        super(DeleteButton, self).__init__(style=discord.ButtonStyle.danger, label='Delete', row=0)

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.delete()


class ClaimButton(discord.ui.Button):
    def __init__(self, c: cards.Card):
        super(ClaimButton, self).__init__(style=discord.ButtonStyle.primary, label='Claim', row=0)
        self.card = c

    async def callback(self, interaction: discord.Interaction):
        if dataloader.user_exists(interaction.user.id):
            dataloader.add_card(interaction.user.id, self.card.id)
            description = f'{self.card.description}\n\n- Belongs to {interaction.user.name}'
            stars = ''
            for i in range(self.card.rating):
                stars += '★'
            embed = discord.Embed(
                title=f'{self.card.title}\n{stars}',
                description=description,
                colour=discord.Colour.red()
            )
            embed.set_image(url=self.card.image_url)
            await interaction.response.edit_message(view=None, embed=embed)
        else:
            await interaction.channel.send('Please join using the ``*join`` command!')


class CardView(discord.ui.View):
    def __init__(self, c: cards.Card):
        super().__init__()
        self.add_item(ClaimButton(c))
        # self.add_item(DeleteButton())
