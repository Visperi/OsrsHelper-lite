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
import traceback
import sys


class ErrorHandlerCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
            The event triggered when an error is raised while invoking a command.

            ctx   : Context
            error : Exception
        """
        if hasattr(ctx.command, "on_error"):
            return

        # MissingRequiredArgument should be raised only when user doesn't give any input to command when needed
        ignored = (commands.CommandNotFound, commands.MissingRequiredArgument)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"{ctx.command} has been disabled.")
            return

        elif isinstance(error, commands.NoPrivateMessage):
            # noinspection PyBroadException
            try:
                await ctx.author.send(f"Command `{ctx.command}` does not support direct messages.")
                return
            except:
                pass

        elif isinstance(error, commands.NotOwner):
            await ctx.send("Only the bot owner can execute this command.")
            return

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You need more permissions to execute this command.")
            return

        elif isinstance(error, commands.MissingRole):
            await ctx.send("You need more roles to execute this command.")
            return

        elif isinstance(error, NotImplementedError):
            await ctx.send("Sorry, this command has not been implemented yet :(")
            return

        print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))
