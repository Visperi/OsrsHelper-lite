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

import discord
from discord.ext import commands


class OsrsHelper(commands.Bot):
    """
    A subclass for commands.Bot to get full control (and to prevent PyCharm unresolved attribute warnings) on
    custom and dynamic attributes without touching the original library files.

    @DynamicAttrs
    """

    def __init__(self, command_prefix: str = "!", **options):
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        super().__init__(command_prefix=command_prefix, intents=intents, **options)
        self.remove_command("help")

        self.reminder_loop_running = False
        self.caches = {}
