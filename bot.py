import os

import discord
import dotenv
from discord.ext import commands

intents = discord.Intents(messages=True,members = True, guilds=True)

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN_MAIN')
bot = commands.Bot(command_prefix='*', intents=intents)
bot.remove_command('help')

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
    if ctx.author.id == 200454087148437504:
        if f'{extension}.py' in os.listdir('./cogs'):
            bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'{extension} successfully loaded.')
        else:
            await ctx.send(f'No extension named {extension} was found.')


@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == 200454087148437504:
        bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == 200454087148437504:
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
