import asyncio
import os
import random
import dotenv
import datetime

import cards
import buttons
import dataloader

import discord
from discord.ext import commands
from pyrebase import pyrebase

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot('*')
bot.remove_command('help')


rate_3 = 83
rate_4 = 15
rate_5 = 2


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
            random_number = random.randint(1, 100)
            card = None
            if random_number <= rate_3:
                card = random.choice(list(cards.card_deck_3.values()))
            elif random_number <= rate_4 + rate_3:
                card = random.choice(list(cards.card_deck_4.values()))
            elif random_number <= rate_5 + rate_4 + rate_3:
                card = random.choice(list(cards.card_deck_5.values()))
            embed, file = card.to_embed(ctx.author)
            await ctx.send(embed=embed, view=buttons.CardView(card, ctx.author), file=file)
        else:
            wait_response = get_time_until_reset()
            await ctx.send(f'{ctx.author.mention}, you can only roll {dataloader.max_rolls} times every 12 hours!\n'
                           f'{wait_response}')
    else:
        await ctx.send(f'{ctx.author.mention}, Please join using the ``*join`` command!')


@bot.command(name='deck', aliases=['d'])
async def show_deck(ctx):
    if dataloader.user_exists(ctx.author.id):
        owned_cards = dataloader.get_cards(ctx.author.id)
        if len(owned_cards) == 0:
            await ctx.send(f"{ctx.author.mention}, you don't have any cards yet!")
        else:
            embed, file = cards.to_owned_embed(ctx.author, owned_cards, 0)
            await ctx.send(embed=embed, file=file, view=buttons.DeckView(owned_cards, ctx.author, cur_page=0))
    else:
        await ctx.send(f'{ctx.author.mention}, Please join using the ``*join`` command!')


@bot.command(name='info', aliases=['i'])
async def show_card(ctx):
    content: str = ctx.message.content
    query = ''
    if content.startswith(f'*info '):
        query = content[6:]
    elif content.startswith(f'*i '):
        query = content[3:]
    if len(query) > 0:
        if query.lower() in cards.name_deck:
            embed, file = cards.name_deck.get(query.lower()).to_display_embed(ctx.author)
            await ctx.send(embed=embed, file=file)
        else:
            await ctx.send(f'No card named {query} found!')


@bot.command(name='display')
async def set_displayed_card(ctx):
    content: str = ctx.message.content
    query = content[9:]
    if len(query) > 0:
        if query.lower() in cards.name_deck:
            owned_cards: [pyrebase.Pyre] = dataloader.get_cards(ctx.author.id)
            if cards.name_deck.get(query.lower()).id in [item.key().lower() for item in owned_cards]:
                dataloader.set_displayed_card(ctx.author.id, cards.name_deck.get(query).id)
                await ctx.send(f'Successfully set your display card to {cards.name_deck.get(query).title}!')
            else:
                await ctx.send(f"You don't own that card yet!")
        elif query == 'reset':
            dataloader.set_displayed_card(ctx.author.id, 'c_id_-1')
            await ctx.send(f'Your deck display was reset!')
        else:
            await ctx.send(f'No card named {query} found!')


@bot.command(name='trade')
async def trade(ctx):
    if ctx.message.mentions:

        if ctx.message.mentions[0].id == ctx.author.id:
            await ctx.send(f"{ctx.author.mention}, you can't trade with yourself!")
        else:

            def check_user1(m):
                if m.author == ctx.author:
                    return True

            def check_user2(m):
                if m.author == ctx.message.mentions[0]:
                    return True

            def confirm(m):
                if m.author == ctx.author:
                    return True

            # get the first users card to trade
            await ctx.send(f'{ctx.author.mention}, enter the name of the card you would like to trade.')
            try:
                user1_msg = await bot.wait_for("message", check=check_user1, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send(f'No message sent, trade cancelled.')
            else:
                card_title: str = user1_msg.content
                user1_cards = dataloader.get_cards(ctx.author.id)
                if card_title.lower() in cards.name_deck:
                    if cards.name_deck.get(card_title.lower()).id in [item.key().lower() for item in user1_cards]:
                        user1_card_to_trade = cards.name_deck.get(card_title.lower())
                    else:
                        await ctx.send(f"{ctx.author.mention}, you don't own any cards named {card_title}"
                                       f", trade cancelled.")
                        return
                else:
                    await ctx.send(f"{ctx.author.mention}, no cards found named {card_title}."
                                   f" Trade cancelled.")
                    return

                # get the second users card to trade
                await ctx.send(f'{ctx.message.mentions[0].mention}, enter the name of the '
                               f'card you would like to trade.')
                try:
                    user2_msg = await bot.wait_for("message", check=check_user2, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send(f'No message sent, trade cancelled.')
                else:
                    card_title: str = user2_msg.content
                    user2_cards = dataloader.get_cards(ctx.message.mentions[0].id)
                    if card_title.lower() in cards.name_deck:
                        if cards.name_deck.get(card_title.lower()).id in [item.key().lower() for item in user2_cards]:
                            user2_card_to_trade = cards.name_deck.get(card_title.lower())
                        else:
                            await ctx.send(f"{ctx.message.mentions[0].mention}, you don't own any cards named "
                                           f"{card_title}. Trade cancelled.")
                            return
                    else:
                        await ctx.send(f"{ctx.message.mentions[0].mention}, no cards found named {card_title}."
                                       f" Trade cancelled")
                        return

                    # confirm
                    await ctx.send(f'{ctx.author.mention}, do you accept this trade? (yes/no)')
                    try:
                        confirm_msg = await bot.wait_for("message", check=confirm, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(f'No message sent, trade cancelled.')
                    else:
                        if confirm_msg.content == 'yes':
                            dataloader.add_card(ctx.author.id, user2_card_to_trade.id)
                            dataloader.add_card(ctx.message.mentions[0].id, user1_card_to_trade.id)
                            dataloader.remove_card(ctx.author.id, user1_card_to_trade.id)
                            dataloader.remove_card(ctx.message.mentions[0].id, user2_card_to_trade.id)

                            user1_display_card = dataloader.get_displayed_card(ctx.author.id)
                            user2_display_card = dataloader.get_displayed_card(ctx.message.mentions[0].id)
                            if user1_display_card == user1_card_to_trade.id:
                                if dataloader.get_num(ctx.author.id, user1_display_card) == 0:
                                    dataloader.reset_displayed_card(ctx.author.id)

                            if user2_display_card == user2_card_to_trade.id:
                                if dataloader.get_num(ctx.message.mentions[0].id, user2_display_card) == 0:
                                    dataloader.reset_displayed_card(ctx.message.mentions[0].id)

                            await ctx.send('Trade completed!')
                        else:
                            await ctx.send(f'Trade cancelled.')


@bot.command(name='time')
async def time_until_reset(ctx):
    response_string = get_time_until_reset()
    await ctx.send(response_string)


def get_time_until_reset():
    current_hour = datetime.datetime.now().hour
    current_min = datetime.datetime.now().minute
    if current_hour < 6:
        response_string = get_time_delta(current_hour, current_min, 6)
    elif current_hour < 18:
        response_string = get_time_delta(current_hour, current_min, 18)
    else:
        response_string = get_time_delta(current_hour, current_min, 30)
    return response_string


def get_time_delta(current_hour, current_min, target_hour):
    if current_min != 0:
        hour_delta = target_hour - current_hour - 1
        min_delta = 60 - current_min
        hour_string = f'{hour_delta} hours' if hour_delta != 1 else f'{hour_delta} hour'
        min_string = f'{min_delta} minutes' if min_delta != 1 else f'{min_delta} minutes'
        if hour_delta == 0:
            return f'There is currently {min_string} until roll reset.'
        else:
            return f'There is currently {hour_string} and {min_string} until roll reset.'
    else:
        hour_delta = target_hour - current_hour
        hour_string = f'{hour_delta} hours' if hour_delta != 1 else f'{hour_delta} hour'
        return f'There is currently {hour_string} until roll reset.'


@bot.command(name='help')
async def help_menu(ctx):
    await ctx.send(embed=help_embed, file=help_thumbnail_file)


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


help_thumbnail_file = discord.File('mujank-logo.jpg', filename='logo.png')
help_embed = discord.Embed(
    title=f'Help - Page {1}',
    description=f'``*join`` - joins the game!\n\n'
                f'``*roll`` - rolls for a new card.\n\n'
                f'``*time`` - checks how much time until roll reset.\n\n'
                f'``*deck`` - displays your deck.\n\n'
                f'``*info <card name>`` - displays a specific card.\n\n'
                f'``*display <card name>`` - sets the thumbnail of your deck.\n\n'
                f'``*trade <@user>`` - initiates a trade with the tagged user.\n\n'
                f'``*help`` - shows this message.',
    colour=discord.Colour.red()
)
help_embed.set_thumbnail(url='attachment://logo.png')


# # test commands
# @bot.command(name='test')
# async def test(ctx):
#     for card in cards.cards:
#         dataloader.add_card(ctx.author.id, card[0])
#
#
# @bot.command(name='give')
# async def give(ctx):
#     query = ctx.message.content[6:]
#     dataloader.add_card(ctx.author.id, cards.name_deck.get(query.lower()).id)
#
#
# @bot.command(name='remove')
# async def remove(ctx):
#     query = ctx.message.content[8:]
#     dataloader.remove_card(ctx.author.id, cards.name_deck.get(query.lower()).id)
#
#
# @bot.command(name='reset')
# async def reset(ctx):
#     dataloader.reset_all_timers()


bot.run(BOT_TOKEN)


