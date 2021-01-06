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

        # Will be raised if user gives amount of kills that is inconvertible to int in command 'loot'.
        elif isinstance(error, commands.UserInputError) and ctx.command.name == "loot":
            await ctx.send("The amount of kills must be an integer. Give kills first and then the boss name.")
            return

        print(f"Ignoring exception in command {ctx.command}:", file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))
