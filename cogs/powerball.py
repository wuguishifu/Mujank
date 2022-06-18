import asyncio
import datetime
import json
import random

import discord
from discord.ext import commands, tasks

import database

coin_emoji = '<:jankcoin:935376607353397308>'
red = discord.Colour.from_rgb(227, 24, 24)

admin = [933726675974381578, 200454087148437504, 937450639506669589]

channel_id = 933225183936933908


class Powerball(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('powerball.py loaded')
        await self.wait_until()

    @tasks.loop(hours=24)
    async def draw_powerball(self):
        channel = self.bot.get_channel(channel_id)
        nums = []
        for i in range(5):
            nums.append(random.randint(1, 69))
        nums.append(random.randint(1, 26))
        await channel.send(f"**It's time for a drawing!**\n\n"
                           f"The lucky numbers are: {', '.join(str(i) for i in nums[:4])}, and {nums[4]}, "
                           f"and the power play is {nums[5]}!")
        winners = []
        with open('cogs/powerball.json', 'r') as json_file:
            data = json.load(json_file)
            for user_id in data['users'].keys():
                total_winnings = 0
                user = self.bot.get_user(int(user_id))
                for t in data['users'][user_id]['tickets'].keys():
                    ticket = data['users'][user_id]['tickets'][t]
                    total_winnings += check_winnings(nums, ticket)
                if total_winnings > 0:
                    winners.append(f"{user.mention}: {total_winnings}x {coin_emoji}")
                    database.add_coins(user_id, total_winnings)

        if len(winners) > 0:
            file = discord.File('mujank-logo.jpg', filename='logo.jpg')
            embed = discord.Embed(
                title='Winners!',
                description='\n'.join(i for i in winners),
                colour=red
            )
            embed.set_thumbnail(url='attachment://logo.jpg')
            await channel.send(embed=embed, file=file)
        else:
            await channel.send(f'No one won any {coin_emoji}!')

        # reset powerball tickets sheet
        data = {"users": {}}
        with open('cogs/powerball.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    # used in conjunction with draw_powerball() to start the daily powerball drawings
    async def wait_until(self):
        now = datetime.datetime.now()
        delta = (datetime.timedelta(hours=24) - (
                now - now.replace(hour=18, minute=0, second=0, microsecond=0))).total_seconds() % (24 * 3600)
        await asyncio.sleep(delta)
        self.draw_powerball.start()

    @commands.command(name='quickplay', aliases=['qp'])
    async def quick_play(self, ctx):
        database.remove_coins(str(ctx.author.id), 3)
        nums = []
        for i in range(5):
            nums.append(random.randint(1, 69))
        nums.append(random.randint(1, 26))
        ticket = ','.join(str(num) for num in nums)
        await ctx.send(f"{ctx.author.mention}, your ticket's numbers are {', '.join(str(i) for i in nums[:5])}, "
                       f"and {nums[5]}. You've been charged 3x {coin_emoji}. Come back at 6:00 PM PST to see if "
                       f"you've won!")
        with open('cogs/powerball.json', 'r') as json_file:
            data = json.load(json_file)
            if str(ctx.author.id) not in data['users']:
                data['users'][str(ctx.author.id)] = {'ticket_id': 1, 'tickets': {0: ticket}}
            else:
                cur_id = data['users'][str(ctx.author.id)]['ticket_id'] + 1
                data['users'][str(ctx.author.id)]['ticket_id'] = cur_id
                data['users'][str(ctx.author.id)]['tickets'][cur_id] = ticket
        with open('cogs/powerball.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @commands.command(name='powerball', aliases=['pb'])
    async def powerball(self, ctx, *args):
        if len(args) < 5:
            await ctx.send('Please enter at least 5 numbers separated by spaces!')
        else:
            in_bound = True
            for i in args:
                if i.isnumeric():
                    if int(i) not in range(1, 69):
                        in_bound = False
                        break
                else:
                    in_bound = False
            if in_bound:
                if len(args) == 5:
                    database.remove_coins(str(ctx.author.id), 2)
                    nums = [i for i in args]
                    nums.append(str(random.randint(1, 26)))
                    charge = 2
                else:
                    database.remove_coins(str(ctx.author.id), 3)
                    nums = args[:6]
                    charge = 3
                ticket = ','.join(num for num in nums)
                with open('cogs/powerball.json', 'r') as json_file:
                    data = json.load(json_file)
                    if str(ctx.author.id) not in data['users']:
                        data['users'][str(ctx.author.id)] = {'ticket_id': 1, 'tickets': {0: ticket}}
                    else:
                        cur_id = data['users'][str(ctx.author.id)]['ticket_id'] + 1
                        data['users'][str(ctx.author.id)]['ticket_id'] = cur_id
                        data['users'][str(ctx.author.id)]['tickets'][cur_id] = ticket
                with open('cogs/powerball.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                await ctx.send(
                    f"{ctx.author.mention}, your ticket's numbers are {', '.join(str(i) for i in nums[:5])}, "
                    f"and {nums[5]}. You've been charged {charge}x {coin_emoji}. Come back at 6:00  PM PST to see "
                    f"if you've won!")
            else:
                await ctx.send('Please make sure your first 5 numbers are between 1 and 69, inclusive, and your '
                               'optional 6th number is between 1 and 26, inclusive!')


def check_winnings(nums, user_nums):
    user_nums = [int(x) for x in user_nums.split(',')]
    matches = 0
    for x in user_nums[:5]:
        if x in nums:
            matches += 1
    if user_nums[5] in nums:
        return red_matches[matches]
    else:
        return white_matches[matches]


red_matches = {
    0: 4,
    1: 4,
    2: 7,
    3: 50,
    4: 100,
    5: 1000
}

white_matches = {
    0: 0,
    1: 0,
    2: 0,
    3: 7,
    4: 75,
    5: 1000
}


def setup(bot: commands.Bot):
    pass
    # bot.add_cog(Powerball(bot))
