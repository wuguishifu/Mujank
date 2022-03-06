import asyncio
import database
import datetime
import channel_id_constants
import birthdays.birthday_dictionary as birthday_dictionary

from birthdays import birthday_constants
from discord.ext import commands, tasks

admin = [933726675974381578, 200454087148437504, 937450639506669589]


class BirthdayGift(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        Function ran when bot is initialized.
        """
        print(birthday_constants.MODULE_LOADED_MESSAGE)
        await self.wait_until()

    async def wait_until(self) -> None:
        """
        Makes function execution happen at 6PM every day.
        """
        # Grab the current datetime
        now = datetime.datetime.now()

        # This is the amount of seconds until 6PM
        delta = (datetime.timedelta(hours=birthday_constants.HOURS_IN_DAY) - (
                now - now.replace(hour=birthday_constants.SIX_PM_HOUR, minute=0, second=0,
                                  microsecond=0))).total_seconds() % (
                birthday_constants.HOURS_IN_DAY * birthday_constants.SECONDS_IN_HOUR)

        # Wait until we reach 6PM
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
        formatted_date = now.strftime(birthday_constants.DATE_FORMAT)

        # Check if this is anyone's birthday if it is, give this person 25 coins
        birthdays = birthday_dictionary.get_dictionary()

        if formatted_date in birthdays:
            for user_id in birthdays[formatted_date]:
                # Increment their balance
                database.add_coins(user_id, birthday_constants.GIFT_AMOUNT)

                # Make announcement of birthday in #mujank channel
                channel = self.bot.get_channel(channel_id_constants.TEST_CHANNEL)
                user = self.bot.get_user(int(user_id))
                await channel.send(f"Happy birthday {user.mention}, please enjoy this gift of 25 jankcoins!")


def setup(bot: commands.Bot) -> None:
    """
    Adds the BirthdayGift cog to the bot.

    :param bot: The current initialization of the Mujank bot.
    """
    bot.add_cog(BirthdayGift(bot))
