from discord.ext import commands


class HelpCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def send_help(ctx: commands.Context, invoked_with: str, help_dict: dict):
        description = help_dict["description"]
        additional = help_dict["additional"] or "-"
        example = help_dict["example"] or "-"

        command_help = f"**{invoked_with}**\n" \
                       f"{description}\n\n" \
                       f"**Additional:** {additional}\n" \
                       f"**Example:** {example}"
        await ctx.send(command_help)

    @commands.group(name="help")
    async def command_help(self, ctx: commands.Context):
        message_content = ctx.message.content
        if ctx.invoked_subcommand is None and message_content != "!help":
            await ctx.send("No help found for such command.")
            return
        elif message_content == "!help":
            await ctx.send("`!info`: Basic info about the bot and latest updates\n"
                           "`!commands`: Get a list of all available commands\n"
                           "`!server commands`: Get a list of all custom commands for this server\n"
                           "`!help <command name>`: Get instructions for one command")

    @command_help.command(name="me")
    async def get_user_info(self, ctx: commands.Context):
        help_dict = {"description": "Fetch some data related to the command invoker and represent it in a nice "
                                    "embed.",
                     "additional": None,
                     "example": "`!me`"}
        await self.send_help(ctx, ctx.invoked_with, help_dict)

    @command_help.command(name="info")
    async def get_bot_info(self, ctx: commands.Context):
        help_dict = {"description": "Get some basic information and latest updates related to this bot.",
                     "additional": None,
                     "example": "`!info`"}
        await self.send_help(ctx, ctx.invoked_with, help_dict)


def setup(bot: commands.Bot):
    bot.add_cog(HelpCog(bot))
