import datetime
import random

import json

import discord
from discord.ext import commands, tasks

coin_emoji = '<:jankcoin:935376607353397308>'

admin = [933726675974381578, 200454087148437504, 937450639506669589]


class Powerball(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('powerball.py loaded')
        self.time_test.start()

    @tasks.loop(hours=24)
    async def time_test(self):
        channel = self.bot.get_channel(932934074270642187)
        await channel.send(f'Got channel {channel}')

    @commands.command(name='powerball', aliases=['pb'])
    async def powerball(self, ctx, *args):
        with open('powerball.json', 'r') as json_file:
            data = json.load(json_file)
            if ctx.author.id not in data['users']:
                data['users'][str(ctx.author.id)] = {'ticket_id': 1, 'tickets': {}}
                data['users'][str(ctx.author.id)]['tickets'][0] = ','.join(num for num in args)
            else:
                cur_id = data['users'][str(ctx.author.id)]['ticket_id'] + 1
                data['users'][str(ctx.author.id)]['ticket_id'] = cur_id
                data['users'][str(ctx.author.id)]['tickets'][cur_id] = ','.join(num for num in args)
        with open('powerball.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)


def setup(bot: commands.Bot):
    bot.add_cog(Powerball(bot))
