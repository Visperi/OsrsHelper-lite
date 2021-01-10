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


class OsrsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="namechange")
    async def change_tracked_name(self, ctx: commands.Context):
        pass

    @commands.command(name="wiki")
    async def search_osrs_wiki(self, ctx: commands.Context):
        pass

    @commands.command(name="stats", aliases=["ironstats", "uimstats", "dmmstats", "seasonstats", "hcstats",
                                             "tournamentstats", "lstats", "leaguestats"])
    async def get_user_hiscores(self, ctx: commands.Context):
        pass

    @commands.command(name="gains")
    async def get_user_gains(self, ctx: commands.Context):
        pass

    @commands.command(name="track")
    async def track_user(self, ctx: commands.Context):
        pass

    @commands.command(name="xp", aliaes=["exp"])
    async def get_required_xp(self, ctx: commands.Context):
        pass

    @commands.command(name="ehp", aliases=["ironehp", "skillerehp", "f2pehp"])
    async def get_ehp_rates(self, ctx: commands.Context):
        pass

    @commands.command(name="nicks")
    async def get_user_nicks(self, ctx: commands.Context):
        pass

    @commands.command(name="update", aliases=["gameupdates"])
    async def get_osrs_news(self, ctx: commands.Context):
        pass

    @commands.command(name="kc", aliases=["killcount"])
    async def get_user_boss_scores(self, ctx: commands.Context):
        pass

    @commands.command(name="keys")
    async def get_item_keywords(self, ctx: commands.Context):
        pass

    @commands.command(name="limit", aliases=["buylimit"])
    async def get_item_buylimit(self, ctx: commands.Context):
        pass

    @commands.command(name="price", aliases=["pricechange", "pc"])
    async def get_item_price(self, ctx: commands.Context):
        pass

#     TODO: Addkey & delkey here or to discord commands?


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(OsrsCog(bot))
