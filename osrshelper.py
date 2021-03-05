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

import aiohttp
import discord
from discord.ext import commands
from caching import Cache


class OsrsHelper(commands.Bot):
    """
    A subclass for commands.Bot to get full control (and to prevent PyCharm unresolved attribute warnings) on
    custom and dynamic attributes without touching the original library files.

    @DynamicAttrs
    """

    def __init__(self, command_prefix: str = "!", **options):
        __intents = discord.Intents.default()
        __intents.members = True
        __intents.presences = True
        super().__init__(command_prefix=command_prefix, intents=__intents, activity=discord.Game(name="Say !help"),
                         **options)
        self.remove_command("help")
        self.on_ready_called = False

        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)
        self.mwiki_cache = Cache("mwiki")
        self.wiki_cache = Cache("wiki")

    async def fetch_url(self, url: str) -> str:
        if url is None:
            raise ValueError("Url can not be None.")
        async with self.aiohttp_session.get(url, timeout=10) as resp:
            if resp.status != 200:
                resp.raise_for_status()
            return await resp.text()
