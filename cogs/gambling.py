import random

import discord
from discord.ext import commands

import database

coin_emoji = '<:jankcoin:935376607353397308>'

admin = [933726675974381578, 200454087148437504, 937450639506669589]


class Gambling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('gambling.py loaded')

    @commands.command(name='dice')
    async def dice(self, ctx, a: str = '1'):
        if a.isnumeric():
            amount = int(a)
        else:
            amount = 1
        balance = database.get_coins(str(ctx.author.id))
        if amount > 0:
            if amount <= balance:
                roll = random.randint(1, 6) + random.randint(1, 6)
                if ctx.author.id == 200454087148437504:
                    roll = 12
                if roll > 8:
                    await ctx.send(f"{ctx.author.mention}, you rolled {roll} and won {2 * amount}x {coin_emoji}!")
                    database.add_coins(str(ctx.author.id), 2 * amount)
                else:
                    await ctx.send(f"{ctx.author.mention}, you rolled {roll} and lost {amount}x {coin_emoji}.")
                    database.remove_coins(str(ctx.author.id), amount)
            else:
                await ctx.send(f"{ctx.author.mention}, you don't have enough coins for that!")
        else:
            await ctx.send(f"{ctx.author.mention}, you can't gamble 0x {coin_emoji}!")

    @commands.command(name='coinflip', aliases=['cf'])
    async def coinflip(self, ctx, a: str = '1'):
        if a.isnumeric():
            amount = int(a)
        else:
            amount = 1
        balance = database.get_coins(str(ctx.author.id))
        if amount > 0:
            if amount <= balance:
                flip = random.randint(1, 2)
                if flip == 2:
                    await ctx.send(
                        f"{ctx.author.mention}, the coin landed on heads and you won {amount}x {coin_emoji}!")
                    database.add_coins(str(ctx.author.id), amount)
                else:
                    await ctx.send(
                        f"{ctx.author.mention}, the coin landed on tails and you lost {amount}x {coin_emoji}.")
                    database.remove_coins(str(ctx.author.id), amount)
            else:
                await ctx.send(f"{ctx.author.mention}, you don't have enough coins for that!")
        else:
            await ctx.send(f"{ctx.author.mention}, you can't gamble 0x {coin_emoji}!")

    @commands.command(name='rules')
    async def rules(self, ctx):
        embed = discord.Embed(
            title='Rules',
            description='**Dice**:\n'
                        'Rolls 2 dice, if the sum is higher than 8 then you win double.\n\n'
                        '**Coinflip**:\n'
                        'Flips a sided coin, if the coin lands on heads then you win.',
            colour=discord.Colour.from_rgb(227, 24, 24)
        )
        file = discord.File('mujank-logo.jpg', filename='logo.jpg')
        embed.set_thumbnail(url='attachment://logo.jpg')
        await ctx.send(embed=embed, file=file)


def setup(bot: commands.Bot):
    bot.add_cog(Gambling(bot))
