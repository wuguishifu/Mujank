import os

import discord
import dotenv
from discord.ext import commands

import database

intents = discord.Intents(messages=True, members=True, guilds=True)

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN_MAIN')
bot = commands.Bot(command_prefix='*', intents=intents)
bot.remove_command('help')

admin = [933726675974381578, 200454087148437504, 937450639506669589]

'''
2* - 49%
3* - 40%
4* - 10%
5* - 0.9%
6* - 0.1%
'''

# load all cogs at startup
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def load(ctx, extension):
    if ctx.author.id in admin:
        if f'{extension}.py' in os.listdir('./cogs'):
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} successfully loaded.')
        else:
            await ctx.send(f'No extension named {extension} was found.')


@bot.command()
async def unload(ctx, extension):
    if ctx.author.id in admin:
        bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    if ctx.author.id in admin:
        if extension == 'all':
            for f in os.listdir('./cogs'):
                if f.endswith('.py'):
                    bot.unload_extension(f'cogs.{f[:-3]}')
                    bot.load_extension(f'cogs.{f[:-3]}')
                    await ctx.send(f'{f[:-3]} successfully reloaded.')
        else:
            bot.unload_extension(f'cogs.{extension}')
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} successfully reloaded.')


@bot.command(name='award', aliases=['reward'])
async def award_coins(ctx, mention, amount='2'):
    if ctx.author.id in admin:
        if ctx.message.mentions:
            if amount.isnumeric():
                amount = int(amount)
                database.add_coins(str(ctx.message.mentions[0].id), amount)
                await ctx.send(f"{ctx.message.mentions[0].mention}, you've been awarded 2 "
                               f"<:jankcoin:935376607353397308> for finding a bug!")


@bot.command(name='bal_dec')
async def bal_dec(ctx, mention, amount='1'):
    if ctx.author.id in admin:
        if ctx.message.mentions:
            if amount.isnumeric():
                amount = int(amount)
                database.remove_coins(str(ctx.message.mentions[0].id), amount)


@bot.command(name='bal_inc')
async def bal_inc(ctx, mention, amount='1'):
    if ctx.author.id in admin:
        if ctx.message.mentions:
            if amount.isnumeric():
                amount = int(amount)
                database.add_coins(str(ctx.message.mentions[0].id), amount)


@bot.event
async def on_message(message):
    channel = message.channel
    if message.content == 'ping':
        await channel.send('pong')
    elif message.content == '!online' and str(message.author) == 'Bo#3515':
        await channel.send('Mujank is currently online.')
    await bot.process_commands(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'*help'))


@bot.event
async def on_command_error(ctx, error):
    print(error)


bot.run(BOT_TOKEN)
