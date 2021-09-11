import os
import dotenv
import random

import discord
from discord.ext import commands

import dataloader

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')


def get_prefix(client, message):
    return dataloader.get_guild_prefix(message.guild.id)


bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')


@bot.command(name='prefix', help='edits the bots prefix')
async def change_prefix(ctx, *args):
    if len(args) == 0:
        await ctx.send(f'Usage: `{dataloader.get_guild_prefix(ctx.guild.id)}prefix <set, reset> <prefix>`')
    if len(args) == 1 and args[0] == 'set':
        await ctx.send(f'Please enter a new prefix.\n\n'
                       f'Usage: `{dataloader.get_guild_prefix(ctx.guild.id)}prefix <set, reset> <prefix>`')
    if len(args) == 2 and args[0] == 'set':
        dataloader.change_guild_prefix(ctx.guild.id, args[1])
        await ctx.send(f'My prefix on this server has been changed to `{args[1]}`')
    elif len(args) == 1 and args[0] == 'reset':
        dataloader.change_guild_prefix(ctx.guild.id, '*')
        await ctx.send(f'My prefix on this server has been reset to `*`')


@bot.event
async def on_message(message):
    channel = message.channel
    if message.content == 'ping':
        await channel.send('pong')
    elif message.content == '69':
        await channel.send('Nice {0.author.mention}!'.format(message))
    await bot.process_commands(message)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'*help'))


@bot.event
async def on_guild_join(guild):
    dataloader.add_guild(guild.id)


@bot.event
async def on_command_error(ctx, error):
    print(error)


bot.run(BOT_TOKEN)
