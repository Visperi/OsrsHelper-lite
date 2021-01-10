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

import helper_methods
import discord
import asyncio
import aiohttp
from osrshelper import OsrsHelper
from discord.ext import commands


class MelvoridleCog(commands.Cog):

    def __init__(self, bot: OsrsHelper):
        self.bot = bot

    @commands.command(name="mwiki")
    async def search_melvoridle_wiki(self, ctx: commands.Context, *, search: str):
        base_url = "https://wiki.melvoridle.com"
        direct_url = f"{base_url}/index.php?title="
        full_search_url = f"{base_url}/index.php?search="
        direct_page = helper_methods.titlecase(search).replace(" ", "_")
        search_parameter = direct_page.replace("_", "+")

        try:
            direct_link = f"{direct_url}{direct_page}"
            await self.bot.fetch_url(f"{direct_url}{direct_page}")
            await ctx.send(f"<{direct_link}>")
        except asyncio.TimeoutError:
            await ctx.send("Melvoridle wiki answered too slowly. Try again later.")
            return
        except aiohttp.ClientError:
            # No page was found with direct url, try using search page
            search_page = f"{full_search_url}{search_parameter}"
            try:
                response = await self.bot.fetch_url(search_page)
            except asyncio.TimeoutError:
                await ctx.send("Melvoridle wiki answered too slowly. Try again later.")
                return
            except aiohttp.ClientError:
                await ctx.send("Could not find anything.")
                return
            
            candidates = helper_methods.parse_wiki_search_candidates(response, base_url)
            embed = discord.Embed(title="Did you mean", description="\n".join(candidates))
            await ctx.send(embed=embed)


def setup(bot: OsrsHelper):
    bot.add_cog(MelvoridleCog(bot))
