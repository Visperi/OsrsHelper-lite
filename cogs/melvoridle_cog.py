import discord
from discord.ext import commands


class MelvoridleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mwiki")
    async def search_melvoridle_wiki(self, ctx: commands.Context):
        pass


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(MelvoridleCog(bot))
