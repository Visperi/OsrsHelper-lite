# coding=utf-8

import discord
import json
import traceback
import os
from osrshelper import OsrsHelper
from enum import Enum

bot = OsrsHelper()


class EBotVersion(Enum):
    """
    Enum for all available bot versions. All version values must be exact match with a key in credentials.json.
    """
    development = "development"
    production = "production"


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Say !help"))
    print("Logged in as:")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    # on_ready is not guaranteed to execute only once so a check is needed to guarantee only one reminder loop


# noinspection PyBroadException
def run(bot_version: EBotVersion):
    with open("Data files/credentials.json", "r") as credential_file:
        credential_data = json.load(credential_file)

    discord_api_token = credential_data["discord_api_tokens"][bot_version.value]

    # Initialize all default cogs into a list and try to load them
    # Cog names must end with _cog
    cogs_path = f"{os.path.dirname(__file__)}/cogs"
    startup_extensions = ["cogs." + fname.rstrip(".py") for fname in os.listdir(cogs_path) if fname.endswith("_cog.py")]

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"Failed to load extension {extension}")
            traceback.print_exc()

    bot.run(discord_api_token, reconnect=True)


if __name__ == "__main__":
    run(EBotVersion.development)
