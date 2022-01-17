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
        await ctx.send(f'Thanks for joining, {ctx.author.mention}!')


@bot.command(name='roll', aliases=['r'])
async def roll(ctx):
    if dataloader.user_exists(ctx.author.id):
        if dataloader.get_num_rolls(ctx.author.id) > 0:
            dataloader.dec_rolls(ctx.author.id)
            card = random.choice(list(card_deck.values()))
            embed, file = card.to_embed(ctx.author)
            await ctx.send(embed=embed, view=buttons.CardView(card, ctx.author), file=file)
        else:
            await ctx.send(f'{ctx.author.mention}, you can only roll {dataloader.max_rolls} times every 6 hours!')
    else:
        await ctx.send(f'{ctx.author.mention}, Please join using the ``*join`` command!')


@bot.command(name='deck', aliases=['d'])
async def show_deck(ctx):
    if dataloader.user_exists(ctx.author.id):
        owned_cards = dataloader.get_cards(ctx.author.id)
        embed, file = to_owned_embed(ctx.author, owned_cards, 0)
        await ctx.send(embed=embed, file=file)
    else:
        await ctx.send(f'{ctx.author.mention}, Please join using the ``*join`` command!')


@bot.command(name='help')
async def help_menu(ctx):
    await ctx.send(embed=help_embed, view=buttons.HelpView(), file=help_thumbnail_file)


@bot.command(name='test')
async def test(ctx):
    embed = discord.Embed(
        title='Test Gif',
        description='mikey takes frickin years',
        colour=discord.Colour.red()
    )
    file = discord.File('mikey-_basketball_mikey.gif', filename='image.gif')
    embed.set_image(url='attachment://image.gif')
    await ctx.send(embed=embed, file=file)


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
    index_start = 10 * page
    index_last = 10 * (page + 1)
    for i in owned_list[index_start:index_last]:
        num = dataloader.get_num(user.id, i)
        card = card_deck[i].title
        description += f'{num}x **{card}**\n'
    embed = discord.Embed(
        title=f"{user.name}'s deck",
        description=description,
        colour=discord.Colour.red()
    )
    file = discord.File(card_deck[owned_list[0]].image_url, 'image.png')
    embed.set_thumbnail(url='attachment://image.png')
    return embed, file


help_thumbnail_file = discord.File('jank-logo.png', filename='logo.png')
help_embed = discord.Embed(
    title=f'Help - Page {1}',
    description=f'``*join`` - joins the game!\n\n'
                f'``*roll`` - rolls for a new card.\n\n'
                f'``*deck`` - displays your deck.\n\n'
                f'``*help`` - shows this message.',
    colour=discord.Colour.red()
)
help_embed.set_thumbnail(url='attachment://logo.png')


bot.run(BOT_TOKEN)
