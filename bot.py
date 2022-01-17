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
for c in cards.cards:
    card_deck[c[0]] = cards.Card(c[0], c[1], c[2], c[3], c[4])


@bot.command(name='join', aliases=['j'])
async def join(ctx):
    if dataloader.user_exists(ctx.author.id):
        await ctx.send('You have already joined!')
    else:
        dataloader.add_user(ctx.author.id)


@bot.command(name='roll', aliases=['r'])
async def roll(ctx):
    card = random.choice(card_deck)
    embed, file = card.to_embed(ctx.author)
    await ctx.send(embed=embed, view=buttons.CardView(card, ctx.author), file=file)


@bot.command(name='deck', aliases=['d'])
async def show_deck(ctx):
    if dataloader.user_exists(ctx.author.id):
        owned_cards = dataloader.get_cards(ctx.author.id)
        embed, file = to_owned_embed(ctx.author, owned_cards, 0)
        await ctx.send(embed=embed, file=file)
    else:
        await ctx.send(f'Please join using the ``*join`` command!')


@bot.command(name='help')
async def help_menu(ctx):
    pass


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


def to_owned_embed(user: discord.user.User, owned_list: [], page: int):
    description = ''
    for i in owned_list[page:page+10]:
        description += f'{dataloader.get_num(user.id, owned_list[i])}x {card_deck[owned_list[i + page]].title}\n'
    embed = discord.Embed(
        title=f"{user.name}'s deck",
        description=description,
        colour=discord.Colour.red()
    )
    file = discord.File(card_deck[owned_list[page]].image_url, 'image.png')
    embed.set_thumbnail(url='attachment://image.png')
    return embed, file


bot.run(BOT_TOKEN)
