import json

from discord.ext import commands

admin = [933726675974381578, 200454087148437504, 937450639506669589]


class Bugs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('bugs.py loaded')

    @commands.command(name='report')
    async def report_bug(self, ctx):
        with open('cogs/bugs.json') as json_file:
            data = json.load(json_file)
            ticket_id = data['ticket_id']
            data['ticket_id'] += 1
            data['open'][ticket_id] = ctx.message.content
        with open('cogs/bugs.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        await ctx.send(f"{ctx.author.mention}, thank you for your submission. Your bug's ticket number is {ticket_id}.")

    @commands.command(name='resolve', aliases=['close'])
    async def resolve_bug(self, ctx, *args):
        if ctx.author.id in admin:
            with open('cogs/bugs.json') as json_file:
                updated = False
                data = json.load(json_file)
                resolved = []
                missing = []
                if args:
                    for ticket_id in args:
                        if ticket_id in data['open']:
                            bug = data['open'][ticket_id]
                            del data['open'][ticket_id]
                            data['closed'][ticket_id] = bug
                            updated = True
                            resolved.append(ticket_id)
                        else:
                            missing.append(ticket_id)
                    if len(resolved) > 0:
                        resolved_msg = f"Ticket(s) {', '.join(t for t in resolved)} resolved."
                    else:
                        resolved_msg = f""
                    if len(missing) > 0:
                        missing_msg = f"Ticket(s) {', '.join(t for t in missing)} not found or already resolved."
                    else:
                        missing_msg = f""
                    await ctx.send(f'{resolved_msg} {missing_msg}')
        if updated:
            with open('cogs/bugs.json', 'w') as json_file:
                json.dump(data, json_file, indent=4)

    @commands.command(name='view')
    async def view_bug(self, ctx, ticket_id=None):
        with open('cogs/bugs.json') as json_file:
            data = json.load(json_file)
            if ticket_id:
                if ticket_id in data['open']:
                    await ctx.send(data['open'][ticket_id][8:])
                elif ticket_id in data['closed']:
                    await ctx.send(data['closed'][ticket_id][8:])
                else:
                    await ctx.send(f"No ticket {ticket_id} found.")

    @commands.command(name='viewopen')
    async def view_open(self, ctx):
        with open('cogs/bugs.json') as json_file:
            data = json.load(json_file)
            if len(list(data['open'])) > 0:
                tickets = ', '.join(ticket for ticket in list(data['open']))
                await ctx.send(f'Here is a list of open tickets:\n{tickets}')
            else:
                await ctx.send(f'There are no open tickets!')

    @commands.command(name='status')
    async def check_status(self, ctx, ticket_id=None):
        with open('cogs/bugs.json') as json_file:
            data = json.load(json_file)
            if ticket_id:
                if ticket_id in data['open']:
                    await ctx.send(f'Ticket {ticket_id} is currently still unresolved.')
                elif ticket_id in data['closed']:
                    await ctx.send(f'Ticket {ticket_id} is resolved.')
                else:
                    await ctx.send(f'Ticket {ticket_id} not found.')


def setup(bot: commands.Bot):
    bot.add_cog(Bugs(bot))
