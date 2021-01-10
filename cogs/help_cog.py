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
