# coding=utf-8

import discord
import datetime
import json
import asyncio
import dateutil.parser
import traceback
import os
from osrshelper import OsrsHelper

bot = OsrsHelper()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Say !help"))
    print("Logged in as:")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    # on_ready is not guaranteed to execute only once so a check is needed to guarantee only one reminder loop
    if not bot.reminder_loop_running:
        await start_reminder_loop()


# TODO: Rewrite to use caching instead of opening files every second
async def start_reminder_loop():
    reminder_file = "Data files/reminders.json"
    num_deprecated = 0

    with open(reminder_file, "r") as data_file:
        reminder_data = json.load(data_file)

    deprecated_mentions = [ts for ts in reminder_data if dateutil.parser.isoparse(ts) < datetime.datetime.utcnow()]

    for ts in deprecated_mentions:
        num_deprecated += len(reminder_data[ts])
        del reminder_data[ts]

    with open(reminder_file, "w") as output_file:
        json.dump(reminder_data, output_file, indent=4, ensure_ascii=False)

    # Set the state true to prevent multiple reminder loops
    bot.reminder_loop_running = True
    print(f"Reminder loop started. Deleted {num_deprecated} deprecated reminders.")

    # Start reminder loop
    while True:
        ts_now = str(datetime.datetime.utcnow().replace(microsecond=0))

        with open(reminder_file, "r") as data_file:
            reminder_data = json.load(data_file)

        try:
            finished_reminders = reminder_data[ts_now]

            for reminder in finished_reminders:
                channel = bot.get_channel(int(reminder["channel"]))
                message = reminder["message"]
                author_id = reminder["author"]
                author = channel.guild.get_member(int(author_id))

                await channel.send(f"{author.mention} {message}")

            del reminder_data[ts_now]

            with open(reminder_file, "w") as output_file:
                json.dump(reminder_data, output_file, indent=4, ensure_ascii=False)

        except KeyError:
            pass

        await asyncio.sleep(1)


# noinspection PyBroadException
def run(bot_version: str):
    with open("Data files/credentials.json", "r") as credential_file:
        credential_data = json.load(credential_file)

    api_token = credential_data["tokens"][bot_version]
    # bot.mwiki_cache = Cache(name="Melvoridle")
    # bot.wiki_cache = Cache(name="Osrs")

    # Initialize all default cogs into a list and try to load them
    cogs_path = f"{os.path.dirname(__file__)}/cogs"
    startup_extensions = ["cogs." + fname.rstrip(".py") for fname in os.listdir(cogs_path) if fname.endswith("_cog.py")]

    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except:
            print(f"Failed to load extension {extension}")
            traceback.print_exc()

    bot.run(api_token, reconnect=True)


if __name__ == "__main__":
    # token = Settings.get_credential("tokens", "kehittajaversio")
    # bot.aiohttp_session = aiohttp.ClientSession(loop=bot.loop)
    # bot.reminder_loop_running = False
    # bot.mwiki_cache = Cache(name="Melvoridle")
    # bot.wiki_cache = Cache(name="Osrs")
    run("kehittajaversio")
