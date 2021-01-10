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
