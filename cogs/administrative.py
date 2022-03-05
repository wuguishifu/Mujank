import datetime

import discord
from discord.ext import commands

import database

red = discord.Colour.from_rgb(227, 24, 24)


class Administrative(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # event
    @commands.Cog.listener()
    async def on_ready(self):
        print('administrative.py loaded')

    @commands.command(name='join', aliases=['j'])
    async def join(self, ctx):
        if database.user_exists(str(ctx.author.id)):
            await ctx.send('You have already joined!')
        else:
            database.add_user(str(ctx.author.id), ctx.author.name)
            await ctx.send(f'Thanks for joining, {ctx.author.mention}!')

    @commands.command(name='time')
    async def time_until_reset(self, ctx):
        response_string = get_time_until_reset()
        await ctx.send(response_string)

    @commands.command(name='help')
    async def help_menu(self, ctx):
        help_thumbnail_file = discord.File('mujank-logo.jpg', filename='logo.jpg')
        help_embed.set_thumbnail(url='attachment://logo.jpg')
        await ctx.send(embed=help_embed, file=help_thumbnail_file)

    @commands.command(name='patchnotes')
    async def patch_notes(self, ctx, arg=None):
        if not arg:
            await ctx.send(f'Please enter a version. Use ``*versions`` to see a list of version.')
        else:
            if arg in list(patches):
                await ctx.send(embed=patches[arg])
            else:
                await ctx.send('That is not a recognized version. Use ``*versions`` to see a list of version.')

    @commands.command(name='versions')
    async def patches(self, ctx):
        patch_list = ''
        for p in list(patches):
            patch_list += f'{p}, '
        patch_list = patch_list[:-2]
        await ctx.send(f'Here are the previous versions:\n{patch_list}')


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


patches = {
    'v0.6b': discord.Embed(
        title='Version ***v0.6b*** (1/19/2022)',
        description="""✩ Added Bot to Jank for beta release
        ✩ Integrated Trading, Deck Viewing, Rolling, and Claiming Features
        ✩ Created cute anime girl as mascot
        ✩ Includes 433 different cards of different rarities""",
        colour=red
    ),

    'v0.7b': discord.Embed(
        title='Version ***v0.7b*** (1/19/2022)',
        description="""✩ Added 2-star and 6-star categories!!
        ✩ Converted some 3-star cards into 2-star cards
        ✩ Added 90+ new cards across all rarities
        ✩ Adjusted rates for all rarities
        ✩ Added a way to search for tags (AKA names!)
        ✩ Added a way to search by rarity
        ✩ Added wishing
        ✩ Added way to display all tags
        ✩ Can now see other people's decks using the ``*deck <@user>`` command
        ✩ Can now give cards to other players using the ``*give <@user>`` command""",
        colour=red
    ),

    'v0.7.1b': discord.Embed(
        title='Version ***v0.7.1b*** (1/20/2022)',
        description="""✩ Changed database to offline solution
        ✩ Made it so that you can set your thumbnail to a gif card
        ✩ Added ``*im`` as an alias for ``*info``""",
        colour=red
    ),

    'v0.8b': discord.Embed(
        title='Version ***v0.8b*** - The Mujank Marketplace',
        description="""✩ Introduced the Mujank Marketplace
        ✩ Improved and Updated the ``*help`` menu
        ✩ Adjusted rates for all rarities
        ✩ Restricted rolling to specific channels
        ✩ Added new cards for every rarity
        ✩ Modified some card rarities
        ✩ _Hello and Welcome to my TEDTalk_: 3-star → 5-star""",
        colour=red
    ),

    'v0.9b': discord.Embed(
        title='Version ***v0.9b***',
        description="""✩ Added \*lb as an Alias for \*leaderboard
        ✩ Changed Daily Coin Rates
        ✩ Added New Units Across all Rarities
        ✩ Added \*ownerlist command to see who owns a specific card
        ✩ Fixed Various Bugs""",
        colour=red
    ),
}

patches_full = {
    'v0.6b': """***Patch v0.6b (1/19/2022)***
✩ Added Bot to Jank for beta release
✩ Integrated Trading, Deck Viewing, Rolling, and Claiming Features
✩ Created cute anime girl as mascot
✩ Includes 433 different cards of different rarities""",

    'v0.7b': """***Patch v0.7b (1/19/2022)***
✩ Added 2 Star and 6 Star Categories!!
✩ Converted some 3 Star Units into 2 Star Units
✩ Added 90+ New Units Across all Rarities
✩ Adjusted Rates for All Rarities
_ _\t\t- 2* = 49%
_ _\t\t- 3* = 40%
_ _\t\t- 4* = 10%
_ _\t\t- 5* = 0.9%
_ _\t\t- 6* = 0.1%
✩ Added a Way to Search for Tags (AKA Names!) 
_ _\t\t- Use commands ``*search <tag>`` or ``*s <tag>`` to check!
✩ Added a Way to Search by Rarity
_ _\t\t- Use commands ``*searchrarity [2-6]`` or ``*sr [2-6]``
✩ Added Wishing  (doesn't actually do much right now)
_ _\t\t- Use commands ``*wish <card name>`` or ``*w <card name>`` to wish for an item
_ _\t\t- Use commands ``*wishlist`` or ``*wl <@user>`` to display your own or someone else's wishlist
_ _\t\t- Use commands ``*wishremove <card name>`` or ``*wr <card name>`` to remove a wish from your wishlist
✩ Added a Way to Display All Tags
_ _\t\t- Use command ``*categories``
✩ Now Allowed to See Someone Else's Deck
_ _\t\t- Use command ``*deck <@user>`` or ``*d <@user>``
✩ Now Allowed to Give Units to Other Players
_ _\t\t- Use command ``*give <@user>`` or ``*g <@user>``""",

    'v0.7.1b': """***Patch v0.7.1b (1/20/2022)***
✩ Changed database to an offline solution
_ _\t\t- This should increase performance
_ _\t\t- Please report any bugs
✩ Made it so that you can set your thumbnail to a gif card
✩ Added ``*im`` as an alias for ``*info``""",

    'v0.8b': """***Patch v0.8b - The Mujank Marketplace (1/24/2022)
✩ Introducing the 
"""
}

help_embed_old = discord.Embed(
    title=f'Help',
    description=f'``*balance`` - checks your Jankcoin balance.\n\n'
                f'``*buy <item name>`` - buys an item from the shop for Jankcoins.\n\n'
                f'``*categories`` - shows all the search tags\n\n'
                f'``*deck`` - displays your deck.\n\n'
                f'``*display <card name>`` - sets the thumbnail of your deck.\n\n'
                f'``*give <@user>`` - gives the tagged user a card.\n\n'
                f'``*info <card name>`` - displays a specific card.\n\n'
                f'``*inventory`` - shows your inventory.\n\n'
                f'``*item <item name>`` - shows information about the specified item.\n\n'
                f'``*join`` - joins the game!\n\n'
                f'``*help`` - shows this message.\n\n'
                f'``*patchnotes <version>`` - shows the patchnotes from the entered Mujank version.\n\n'
                f'``*pay <@user> <amount>`` - pays `amount` of Jankcoins to the tagged user.\n\n'
                f'``*price <card name>`` - checks the selling price of a card.\n\n'
                f'``*prices`` - displays the selling price of each card rarity.\n\n'
                f'``*roll`` - rolls for a new card.\n\n'
                f'``*search <person>`` - searches for cards of that person.\n\n'
                f'``*searchrarity <rarity>`` - searches for cards by rarity.\n\n'
                f'``*sell <card name>`` - sell a card for Jankcoins.\n\n'
                f'``*shop`` - displays the item shop.\n\n'
                f'``*time`` - checks how much time until roll reset.\n\n'
                f'``*trade <@user>`` - initiates a trade with the tagged user.\n\n'
                f'``*use <card name>`` - uses an item from your inventory.\n\n'
                f'``*versions`` - shows a list of previous Mujank versions.\n\n'
                f'``*wishadd <card name>`` - adds a card to wishlist.\n\n'
                f'``*wishlist`` - displays your wishlist.\n\n'
                f'``*wishremove <card name>`` - removes a card from your wishlist.',
    colour=red
)

help_embed = discord.Embed(
    title=f'Help',
    description=f'**Utility** :pick:\n'
                f'**\*time**: displays how much time until roll reset.\n'
                f'**\*join**: joins the game!\n'
                f'**\*roll**: rolls a card!\n'
                f'**\*help**: shows this message.\n\n'
                f''
                f'**Information** :information_source:\n'
                f'**\*info <card name>**: displays a specific card.\n'
                f'**\*item <item name>**: displays a specific item.\n'
                f'**\*categories**: displays a list of categories for the **\*search** command.\n'
                f'**\*search <tag>**: searches for cards with the specified tag.\n'
                f'**\*searchrarity <rarity [2-6]>**: searches for cards with the specified rarity.\n'
                f'**\*versions**: displays a list of previous versions.\n'
                f'**\*patchnotes <version>**: displays the patch-notes from that version.\n\n'
                f''
                f'**Shop** :shopping_cart:\n'
                f'**\*balance**: displays your balance of Jankcoins.\n'
                f'**\*daily**: claim your daily Jankcoins!\n'
                f'**\*shop**: displays the Mujank Marketplace.\n'
                f'**\*buy <item name>**: buys an item from the Mujank Marketplace with Jankcoins.\n'
                f'**\*sell <card name>**: sells a card to the Mujank Marketplace for Jankcoins.\n'
                f'**\*sellall**: sells all your cards to the Mujank Marketplace for Jankcoins.\n'
                f'**\*price <card name>**: displays the price of that card in Jankcoins.\n'
                f'**\*prices**: displays the price of the different card rarities in Jankcoins.\n\n'
                f''
                f'**Gambling** :game_die:\n'
                f'**\*rules**: shows the rules of the different games.\n'
                f'**\*dice <coin amount>**: gambles specified amount of Jankcoins in the dice game.\n'
                f'**\*coinflip <coin amount>**: gambles specified amount of Jankcoins in the coinflip game.\n\n'
                f''
                f'**Inventory** :school_satchel:\n'
                f'**\*ownerslist <card name>**: shows who owns a card.\n'
                f'**\*deck**: displays your deck of cards.\n'
                f'**\*display <card name>**: sets the thumbnail of your deck.\n'
                f'**\*inventory**: displays your inventory of items.\n'
                f'**\*use <item name>**: uses an item from your inventory.\n\n'
                f''
                f'**Social** :family:\n'
                f'**\*leaderboard**: displays the Mujank leaderboard.\n'
                f'**\*give <@user>**: gives the tagged user a card.\n'
                f'**\*pay <@user> <amount>**: gives the tagged user the specified amount of Jankcoins.\n'
                f'**\*trade <@user>**: initiates a trade with the tagged user.\n\n'
                f''
                f'**Wishlist** :sparkles:\n'
                f'**\*wishadd <card name>**: adds the specified card to your wishlist.\n'
                f'**\*wishlist**: displays your wishlist.\n'
                f'**\*wishremove <card name>**: removes the specified card from your wishlist.\n\n'
                f''
                f'**Help** :information_source:\n'
                f'**\*report <bug message>**: make a bug report.\n'
                f'**\*status <ticket number>**: checks the status of your bug report.\n'
                f'**\*view <ticket number>**: checks the bug report message.\n'
                f'**\*viewopen**: view the currently unresolved bugs.',
    colour=red
)


def setup(bot: commands.Bot):
    bot.add_cog(Administrative(bot))
