"""
MIT License

Copyright (c) 2021 Visperi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
import asyncio
import json
import traceback
import caching
from discord.ext import commands
from typing import Union


class Reminder:

    def __init__(self, bot: commands.Bot, loop: asyncio.BaseEventLoop,
                 cache: caching.Cache = caching.Cache(name="Reminder cache"),
                 reminder_path: str = "Data files/reminders.json",
                 backup_cycle: int = 1800):
        self.bot = bot
        self.cache = cache
        self.reminder_path = reminder_path
        self.loop = loop
        self.backup_cycle = backup_cycle

    @staticmethod
    def log(msg: str):
        print(f"[Reminder] {msg}")

    @staticmethod
    def cache_delete_check(cache_item: caching.CacheItem):
        return cache_item.key <= int(datetime.datetime.utcnow().timestamp())

    def serialize(self, file: str = None):
        if file is None:
            file = self.reminder_path

        tmp = {}
        self.cache.delete_delegated(self.cache_delete_check)

        for timestamp, cache_item in self.cache.items():
            tmp[str(timestamp)] = cache_item.value

        with open(file, "w", encoding="utf-8") as target_file:
            json.dump(tmp, target_file, indent=4, ensure_ascii=False)

    def add(self, timestamp: int, author_id: Union[int, str], channel_id: Union[int, str], message: str):
        reminder_data = dict(channel=str(channel_id), message=message, author=str(author_id))
        try:
            self.cache[int(timestamp)].append(reminder_data)
        except KeyError:
            self.cache[int(timestamp)] = [reminder_data]

    def delete(self):
        raise NotImplementedError

    def start(self):
        with open(self.reminder_path, "r", encoding="utf-8") as reminders_file:
            try:
                serialized_reminders = json.load(reminders_file)
            except Exception as e:
                traceback.print_exc(type(e), e, e.__traceback__)
                self.log("Failed to load serialized JSON reminders. Aborting...")
                return

        # Load serialized reminders into the cache
        # They are in format {ts: [reminder, ... , reminder_n], ts2: [reminder, ... , reminder_m], ...}
        for timestamp in serialized_reminders.keys():
            self.cache[int(timestamp)] = serialized_reminders[timestamp]

        num_deprecated = self.cache.delete_delegated(self.cache_delete_check)
        self.log(f"Deleted {num_deprecated} deprecated reminders.")
        # Serialize remaining reminders back to file and start the loop
        self.serialize()
        self.loop.create_task(self.__loop())

    async def __loop(self):
        unserialized_loops = 0

        self.log("Reminder loop started.")
        while True:
            # Do a backup serialization every X loops
            if unserialized_loops == self.backup_cycle:
                unserialized_loops = 0
                self.serialize()

            utc_ts = int(datetime.datetime.utcnow().timestamp())

            try:
                reminder_list = self.cache.pop(utc_ts)
            except KeyError:
                unserialized_loops += 1
                await asyncio.sleep(1)
                continue

            for reminder in reminder_list:
                channel = self.bot.get_channel(int(reminder["channel"]))
                author = self.bot.get_user(int(reminder["author"]))
                message = reminder["message"]
                await channel.send(f"{author.mention} {message}")

            unserialized_loops += 1
            await asyncio.sleep(1)


if __name__ == '__main__':
    print("This module should be used only through a Discord bot.")
