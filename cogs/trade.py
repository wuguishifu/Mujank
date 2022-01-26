import asyncio

import discord
from discord.ext import commands

import cards
import database


class Trade(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print('trade.py loaded')

    # trade command
    @commands.command(name='trade', aliases=['t'])
    async def trade(self, ctx):
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
                    user1_msg = await self.bot.wait_for("message", check=check_user1, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send(f'No message sent, trade cancelled.')
                else:
                    card_title: str = user1_msg.content.replace('‘', "'").replace('’', "'")
                    if card_title.lower() in cards.name_deck:
                        if database.has_card(str(ctx.author.id), cards.name_deck.get(card_title.lower()).id):
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
                        user2_msg = await self.bot.wait_for("message", check=check_user2, timeout=30)
                    except asyncio.TimeoutError:
                        await ctx.send(f'No message sent, trade cancelled.')
                    else:
                        card_title: str = user2_msg.content.replace('‘', "'").replace('’', "'")
                        if card_title.lower() in cards.name_deck:
                            if database.has_card(str(ctx.message.mentions[0].id),
                                                 cards.name_deck.get(card_title.lower()).id):
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
                            confirm_msg = await self.bot.wait_for("message", check=confirm, timeout=30)
                        except asyncio.TimeoutError:
                            await ctx.send(f'No message sent, trade cancelled.')
                        else:
                            if confirm_msg.content.lower() in ['yes', 'y']:
                                database.add_card(str(ctx.author.id), user2_card_to_trade.id)
                                database.add_card(str(ctx.message.mentions[0].id), user1_card_to_trade.id)
                                database.remove_card(str(ctx.author.id), user1_card_to_trade.id)
                                database.remove_card(str(ctx.message.mentions[0].id), user2_card_to_trade.id)
                                await ctx.send('Trade completed!')
                            else:
                                await ctx.send(f'Trade cancelled.')

    # give command
    @commands.command(name='give', aliasas=['g'])
    async def give_card(self, ctx):
        if ctx.message.mentions:
            user2: discord.user.User = ctx.message.mentions[0]
            user1: discord.user.User = ctx.author
            if user1.id == user2.id:
                await ctx.send(f"{user1.mention}, you can't give a card to yourself!")
            else:

                def check_user1(m):
                    if m.author == user1:
                        return True

                def check_user2(m):
                    if m.author == user2:
                        return True

                # get the card for the first user to give
                user1_card_to_give = None
                await ctx.send(
                    f'{user1.mention}, enter the name of the card you would like to give to {user2.mention}.')
                try:
                    user1_msg = await self.bot.wait_for("message", check=check_user1, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send(f'No message sent, give cancelled.')
                else:
                    card_title: str = user1_msg.content.replace('‘', "'").replace('’', "'")
                    if card_title.lower() in cards.name_deck:
                        if database.has_card(str(ctx.author.id), cards.name_deck.get(card_title.lower()).id):
                            user1_card_to_give = cards.name_deck.get(card_title.lower())
                        else:
                            await ctx.send(f"{user1.mention}, you don't own any cards named {card_title}"
                                           f", give cancelled.")
                            return
                    else:
                        await ctx.send(f"{user1.mention}, no cards found named {card_title}."
                                       f" Give cancelled.")
                        return

                # ask second user to confirm
                await ctx.send(f"{user2.mention}, {user1.mention} is trying to give you {user1_card_to_give.title}."
                               f" Do you accept? (yes/no)")
                try:
                    confirm_msg = await self.bot.wait_for("message", check=check_user2, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send(f'No message sent, give cancelled.')
                else:
                    if confirm_msg.content.lower() in ['yes', 'y']:
                        database.add_card(str(user2.id), user1_card_to_give.id)
                        database.remove_card(str(user1.id), user1_card_to_give.id)

                        # if Will gives a card to Nina
                        will_id = 129387033993936897
                        nina_id = 280550248135262209
                        if user1.id == will_id and user2.id == nina_id:
                            await ctx.send(f'Will is a simp for Nina by giving her {user1_card_to_give.title}')
                        else:
                            await ctx.send('Give completed!')
                    else:
                        await ctx.send('Give cancelled.')


def setup(bot: commands.Bot):
    bot.add_cog(Trade(bot))
