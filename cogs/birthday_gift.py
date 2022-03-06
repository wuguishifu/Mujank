import asyncio
import database
import datetime
import birthdays.birthday_dictionary as birthday_dictionary

from discord.ext import commands, tasks

admin = [933726675974381578, 200454087148437504, 937450639506669589]

# We are writing a birthday message in the #mujank channel
CHANNEL_ID = 933225183936933908

# Number of coins given as gift
GIFT_AMOUNT = 25


class BirthdayGift(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        Function ran when bot is initialized.
        """
        print("birthday_gift.py loaded")
        await self.wait_until()

    async def wait_until(self) -> None:
        """
        Makes function execution happen at 6PM every day.

        """
        # Grab the current datetime
        now = datetime.datetime.now()

        # This is the amount of seconds until 6pm
        delta = (datetime.timedelta(hours=24) - (
                now - now.replace(hour=18, minute=0, second=0, microsecond=0))).total_seconds() % (24 * 3600)

        # Wait until we reach 6pm
        await asyncio.sleep(delta)
        self.give_birthday_gifts.start()

    @tasks.loop(hours=24)
    async def give_birthday_gifts(self) -> None:
        """
        Checks if  it is someone's birthday today, and if it is, then gives them a gift of
        25 jankcoins.
        """
        # Get the current date
        now = datetime.datetime.now()
        formatted_date = now.strftime("%m_%d")

        # Check if this is anyone's birthday if it is, give this person 25 coins
        birthdays = birthday_dictionary.get_dictionary()

        if formatted_date in birthdays:
            for user_id in birthdays[formatted_date]:
                # Increment their balance
                database.add_coins(user_id, GIFT_AMOUNT)

                # Make announcement of birthday in #mujank channel
                channel = self.bot.get_channel(CHANNEL_ID)
                user = self.bot.get_user(int(user_id))
                await channel.send(f"Happy birthday {user.mention}, please enjoy this gift of 25 jankcoins!")


def setup(bot: commands.Bot) -> None:
    """
    Adds the BirthdayGift cog to the bot.

    :param bot: The current initialization of the Mujank bot.
    """
    bot.add_cog(BirthdayGift(bot))
