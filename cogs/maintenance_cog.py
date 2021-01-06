from discord.ext import commands


class MaintenanceCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="extension")
    @commands.is_owner()
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

    @commands.command(name="id")
    @commands.is_owner()
    async def get_item_id(self, ctx: commands.Context, *, item_name: str):
        pass

    @commands.command(name="check")
    @commands.is_owner()
    async def check_new_items(self, ctx: commands.Context):
        # TODO: Caching???
        pass
        # tradeables_file = "Data files/Tradeables.json"
        # url = "https://rsbuddy.com/exchange/summary.json"
        #
        # try:
        #     resp = await static_functions.make_request(client.aiohttp_session, url)
        # except asyncio.TimeoutError:
        #     await message.channel.send("RsBuddy answered too slowly.")
        #     return
        #
        # resp_data = json.loads(resp)
        # new_items = []
        #
        # with open(tradeables_file, "r") as data_file:
        #     saved_data = json.load(data_file)
        #
        # for item in resp_data.values():
        #     item_id = item["id"]
        #     item_name = item["name"]
        #     members = item["members"]
        #     store_price = item["sp"]
        #
        #     if item_name not in saved_data:
        #         saved_data[item_name] = dict(id=item_id, members=members, store_price=store_price)
        #         new_items.append(item_name)
        #
        # if len(new_items) > 0:
        #     with open(tradeables_file, "w") as data_file:
        #         json.dump(saved_data, data_file, indent=4)
        #
        #     finish_message = "Added {} new items:\n\n{}".format(len(new_items), "\n".join(new_items))
        #     if len(finish_message) > 2000:
        #         finish_message = f"Added {len(new_items)} new items but they do not fit into one Discord message."
        #
        # else:
        #     finish_message = "No new items to add."
        #
        # await ctx.send(finish_message)

    @commands.command(name="get")
    @commands.is_owner()
    async def get_file(self, ctx: commands.Context, filename: str):
        print(type(filename))
        await ctx.send(filename)

    @commands.command("managedrinks")
    @commands.is_owner()
    async def manage_drinks(self, ctx: commands.Context):
        pass

    @commands.command("clear")
    @commands.is_owner()
    async def clear_cache(self, ctx: commands.Context, cache_name: str):
        pass

    @commands.command("devcommands")
    @commands.is_owner()
    async def get_maintenance_commands(self, ctx: commands.Context):
        pass


def setup(bot: commands.Bot):
    bot.add_cog(MaintenanceCog(bot))
