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
                 serialize_path: str = "Data files/reminders.json",
                 backup_threshold: int = 1800):
        """
        :param bot: Bot owning this reminder. This is used in actually sending the reminders to Discord
        :param loop: Event loop where the reminder is initialized to as a task
        :param cache: Cache where the reminders are deserialized and stored to
        :param serialize_path: Path to a file where reminders can be serialized to
        :param backup_threshold: Number of rounds after which the reminders are serialized into file in serialize_path
        """
        self.__name = type(self).__name__
        self.__loop_task: Union[asyncio.tasks.Task, None] = None
        self.bot = bot
        self.cache = cache
        self.serialize_path = serialize_path
        self.loop = loop
        self.backup_threshold = backup_threshold

    # @staticmethod
    def __log(self, msg: str):
        print(f"[{self.__name}] {msg}")

    @staticmethod
    def __cache_delete_check(cache_item: caching.CacheItem):
        return cache_item.key <= int(datetime.datetime.utcnow().timestamp())

    def serialize(self, file: str = None) -> None:
        """
        Serialize reminders in cache to json file
        :param file: Path to a file. One is made if it does not already exist. None is serialize_path.
        """
        if file is None:
            file = self.serialize_path

        tmp = {}
        self.cache.delete_delegated(self.__cache_delete_check)

        for timestamp, cache_item in self.cache.items():
            tmp[str(timestamp)] = cache_item.value

        with open(file, "w", encoding="utf-8") as target_file:
            json.dump(tmp, target_file, indent=4, ensure_ascii=False)

    def add(self, timestamp: int, author_id: Union[int, str], channel_id: Union[int, str], message: str) -> None:
        """
        Add a reminder

        :param timestamp: UTC timestamp when the reminder should be triggered at. Is floored to integer
        :param author_id: Discord ID of the reminder author. Reminder is mentioned when the reminder is triggered.
        :param channel_id: Discord ID of the reminder channel. Reminder is sent to this channel when triggered.
        :param message: Message for the reminder.
        """
        if self.__loop_task is None:
            self.__log("WARNING: Reminder loop is not running. Reminders will not be triggered until one is started.")

        reminder_data = dict(channel=str(channel_id), message=message, author=str(author_id))
        try:
            self.cache[int(timestamp)].append(reminder_data)
        except KeyError:
            self.cache[int(timestamp)] = [reminder_data]

    def delete(self):
        raise NotImplementedError

    def stop(self) -> None:
        """
        Stop a reminder loop.
        :raises ValueError: If no loop is running for executing instance.
        """
        if self.__loop_task is None:
            raise ValueError("No loop running for this Reminder instance.")

        self.__loop_task.cancel()
        self.__log("Reminder loop stopped.")
        self.__loop_task = None

    def start(self) -> None:
        """
        Start a reminder loop.
        :raises ValueError: If a reminder loop is already running for executing instance.
        """
        if self.__loop_task is not None:
            raise ValueError("Reminder loop is already running for this Reminder instance.")

        with open(self.serialize_path, "r", encoding="utf-8") as reminders_file:
            try:
                serialized_reminders = json.load(reminders_file)
            except Exception as e:
                traceback.print_exc(type(e), e, e.__traceback__)
                self.__log("Failed to load serialized JSON reminders. Aborting...")
                return

        # Load serialized reminders into the cache
        # They are in format {ts: [reminder, ... , reminder_n], ts2: [reminder, ... , reminder_m], ...}
        for timestamp in serialized_reminders.keys():
            self.cache[int(timestamp)] = serialized_reminders[timestamp]

        num_deprecated = self.cache.delete_delegated(self.__cache_delete_check)
        self.__log(f"Deleted {num_deprecated} deprecated reminders.")
        # Serialize remaining reminders back to file and start the loop
        self.serialize()
        self.__loop_task = self.loop.create_task(self.__loop())

    async def __loop(self):
        deserialized_loops = 0

        self.__log("Reminder loop started.")
        while True:
            # Do a backup serialization every X loops
            if deserialized_loops == self.backup_threshold:
                deserialized_loops = 0
                self.serialize()

            utc_ts = int(datetime.datetime.utcnow().timestamp())

            try:
                reminder_list = self.cache.pop(utc_ts)
            except KeyError:
                deserialized_loops += 1
                await asyncio.sleep(1)
                continue

            for reminder in reminder_list:
                channel = self.bot.get_channel(int(reminder["channel"]))
                author = self.bot.get_user(int(reminder["author"]))
                message = reminder["message"]
                await channel.send(f"{author.mention} {message}")

            deserialized_loops += 1
            await asyncio.sleep(1)


if __name__ == '__main__':
    print("This module should be used only through a Discord bot.")
