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

from discord.ext import commands


class MaintenanceCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="extension", aliases=["cog"])
    async def manage_extensions(self, ctx: commands.Context, *args):
        """
        Load, unload or reload an extension. Currently supports only cogs, which names must end with _cog.
        :return:
        """
        try:
            operation = args[0]
            extension_namespace = args[1]
            if not extension_namespace.endswith("_cog"):
                extension_namespace += "_cog"
        except IndexError:
            await ctx.send("Please provide the arguments in order: `!extension [operation] [cog_namespace]`.")
            return

        if operation == "load":
            method = self.bot.load_extension
        elif operation == "unload":
            method = self.bot.unload_extension
        elif operation == "reload":
            method = self.bot.reload_extension
        else:
            await ctx.send(f"Invalid extension operation: `{operation}`. Supported operations are `load`, `unload` "
                           f"and `reload`.")
            return

        if extension_namespace == "cogs.discord_cog":
            await self.serialize_cog(ctx)
        try:
            method(extension_namespace)
            await ctx.send(f"Successfully {operation}ed extension `{extension_namespace}`.")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f"Extension `{extension_namespace}` is already loaded. Please ensure the full "
                           f"extension namespace was given.")
        except commands.ExtensionNotFound:
            await ctx.send(f"Extension `{extension_namespace}` could not be found. Please ensure the full "
                           f"extension namespace was given.")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"Extension `{extension_namespace}` is not loaded. Please ensure the full "
                           f"extension namespace was given.")

    @commands.command(name="serialize", aliases=["backup"])
    async def serialize_cog(self, ctx: commands.Context, *cog_name):
        if len(cog_name) == 0:
            cog_name = "DiscordCog"

        cog = self.bot.get_cog(cog_name)
        if cog is None:
            await ctx.send(f"Cog with name `{cog_name}` is not loaded.")
            return

        try:
            cog.serialize()
        except AttributeError:
            await ctx.send(f"Cog `{cog_name}` does not have method `serialize()`.")
            return

        await ctx.send("Cog data serialized.")

    @commands.command(name="extensions")
    async def get_loaded_extensions(self, ctx: commands.Context):
        loaded_extensions = [f"`{name}`" for name in self.bot.extensions]
        await ctx.send("Currently loaded extensions:\n" + "\n".join(loaded_extensions))

    @commands.command(name="cogs")
    async def get_loaded_cogs(self, ctx: commands.Context):
        loaded_cogs = [f"`{name}`" for name in self.bot.cogs]
        await ctx.send("Currently loaded cogs:\n" + "\n".join(loaded_cogs))

    @commands.command(name="id")
    async def get_item_id(self, ctx: commands.Context, *, item_name: str):
        raise NotImplementedError

    @commands.command(name="check")
    async def check_new_items(self, ctx: commands.Context):
        # TODO: Caching???
        raise NotImplementedError

    @commands.command(name="get")
    async def get_file(self, ctx: commands.Context, filename: str):
        raise NotImplementedError

    @commands.command("managedrinks")
    async def manage_drinks(self, ctx: commands.Context):
        raise NotImplementedError

    @commands.command("clear")
    async def clear_cache(self, ctx: commands.Context, cache_name: str):
        raise NotImplementedError

    @commands.command("devcommands")
    async def get_maintenance_commands(self, ctx: commands.Context):
        raise NotImplementedError


def setup(bot: commands.Bot):
    bot.add_cog(MaintenanceCog(bot))
