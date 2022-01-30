import random

import discord
from discord.ext import commands

import database

coin_emoji = '<:jankcoin:935376607353397308>'


class Gambling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('gambling.py loaded')

    @commands.command(name='dice')
    async def dice(self, ctx, a: str = '1'):
        if a.isnumeric():
            amount = str(a)
        else:
            amount = 1
        balance = database.get_coins(str(ctx.author.id))
        if amount <= balance:
            roll = random.randint(1, 6) + random.randint(1, 6)
            if roll > 8:
                await ctx.send(f"{ctx.author.mention}, you won {2 * amount}x {coin_emoji}!")
                database.add_coins(str(ctx.author.mention), amount)
            else:
                await ctx.send(f"{ctx.author.mention}, you lost {amount}x {coin_emoji}.")
                database.remove_coins(str(ctx.author.mention), amount)
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have enough coins for that!")

    @commands.command(name='coinflip')
    async def coinflip(self, ctx, a: str = '1'):
        if a.isnumeric():
            amount = str(a)
        else:
            amount = 1
        balance = database.get_coins(str(ctx.author.id))
        if amount <= balance:
            flip = random.randint(1, 3)
            if flip == 3:
                await ctx.send(f"{ctx.author.mention}, you won {2 * amount}x {coin_emoji}!")
                database.add_coins(str(ctx.author.mention), amount)
            else:
                await ctx.send(f"{ctx.author.mention}, you lost {amount}x {coin_emoji}.")
                database.remove_coins(str(ctx.author.mention), amount)
        else:
            await ctx.send(f"{ctx.author.mention}, you don't have enough coins for that!")

    @commands.command(name='rules')
    async def rules(self, ctx):
        embed = discord.Embed(
            title='Rules',
            description='**Dice**:\n'
                        'Rolls 2 dice, if the sum is higher than 8 then you win.\n\n'
                        '**Coinflip**:\n'
                        'Flips a coin, if the coin lands on heads then you win.',
            colour=discord.Colour.from_rgb(227, 24, 24)
        )
        file = discord.File('mujank-logo.jpg', filename='logo.jpg')
        embed.set_thumbnail(url='attachment://logo.jpg')
        await ctx.send(embed=embed, file=file)


def setup(bot: commands.Bot):
    bot.add_cog(Gambling(bot))
