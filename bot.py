import os
import random
import dotenv

import cards
import buttons
import dataloader

import discord
from discord.ext import commands

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot('*')

bot.remove_command('help')


card_deck = {}
for c in cards.card_deck:
    card_deck[c[0]] = cards.Card(c[0], c[1], c[2], c[3], c[4])


@bot.command(name='roll', aliases=['r'])
async def roll(ctx):
    card = random.choice(card_deck)
    await ctx.send(embed=card.to_embed(), view=buttons.CardView(card))


@bot.command(name='test')
async def test(ctx):
    print(dataloader.card_owned(0))


@bot.command(name='join', aliases=['j'])
async def join(ctx):
    if dataloader.user_exists(ctx.author.id):
        await ctx.send('You have already joined!')
    else:
        dataloader.add_user(ctx.author.id)


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


@bot.command(name='help')
async def help_menu(ctx):
    await ctx.send(embed=card_deck[0].to_embed())


bot.run(BOT_TOKEN)
