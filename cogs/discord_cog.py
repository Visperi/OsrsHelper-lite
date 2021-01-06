import discord
from discord.ext import commands
import datetime
import os
import platform
import static_functions
import random
from typing import Union
from mathparse import mathparse


class DiscordCog(commands.Cog):

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @staticmethod
    def fetch_activity(activity: Union[discord.BaseActivity, discord.Spotify, discord.Activity]) -> str:
        if activity is None:
            _activity = "None"
        elif isinstance(activity, discord.Spotify):
            _activity = f"Listening to Spotify:\n{activity.artist} - {activity.title}"
        elif isinstance(activity, discord.Game):
            _activity = f"Playing {activity.name}"
        elif isinstance(activity, discord.Streaming):
            _activity = f"Streaming {activity.game}\nat {activity.platform} ([Link]({activity.url}))"
        elif isinstance(activity, discord.CustomActivity):
            if activity.emoji is None:
                _activity = activity.name
            else:
                _activity = f"{activity.emoji} {activity.name}"
        else:
            name = activity.name
            _type = str(activity.type).split(".")[1].capitalize()
            _activity = f"{_type} {name}\n{activity.state}"

        return _activity

    @commands.command(name="info", aliases=["version"])
    async def get_bot_info(self, ctx: commands.Context):
        with open("Data files/changelog_en.txt", "r", encoding="utf-8") as changelog_file:
            changelog = changelog_file.read()

        appinfo = await self.bot.application_info()
        last_updated = datetime.datetime.fromtimestamp(os.path.getmtime("main.py")).strftime("%Y-%m-%d")

        embed_desc = f"Developer: {appinfo.owner}\n" \
                     f"Updated: {last_updated}\n" \
                     f"Source code: Python {platform.python_version()} " \
                     f"([GitHub](https://github.com/Visperi/OsrsHelper))\n" \
                     f"using discord.py {discord.__version__}\n"
        credits_val = "[discord.py](https://github.com/Rapptz/discord.py) (Discord library used in bot)\n" \
                      "[Crystalmathlabs](http://www.crystalmathlabs.com/tracker/) (EHP rates)\n" \
                      "[Old school runescape](http://oldschool.runescape.com/) (Hiscores, game news)\n" \
                      "[RSBuddy](https://rsbuddy.com/) (G.E. prices)\n" \
                      "[Melvoridle wiki](https://wiki.melvoridle.com/) (Melvoridle wiki)\n" \
                      "[OSRS Wiki](https://oldschool.runescape.wiki) (Wiki)"
        embed = discord.Embed(title=appinfo.name, description=embed_desc)
        embed.add_field(name="Credits", value=credits_val, inline=False)
        embed.add_field(name="Latest changes", value=changelog)
        embed.set_thumbnail(url=appinfo.icon_url)

        await ctx.send(embed=embed)

    @commands.command(name="me")
    @commands.guild_only()
    async def get_user_info(self, ctx: commands.Context):
        author = ctx.message.author

        created_at = static_functions.isofy(author.created_at) + " UTC"
        joined_at = static_functions.isofy(author.joined_at) + " UTC"
        # Every user always have role @everyone so it's a little bit redundant here
        server_roles = [str(role) for role in author.roles if str(role) != "@everyone"]

        author_info = discord.Embed().set_author(name=author.display_name).set_thumbnail(url=author.avatar_url)
        author_info.add_field(name="Username", value=str(author))
        author_info.add_field(name="Is on mobile", value=author.is_on_mobile())
        author_info.add_field(name="Is early supporter", value=author.public_flags.early_supporter)
        author_info.add_field(name="User created", value=created_at)
        author_info.add_field(name="Joined at", value=joined_at)
        author_info.add_field(name="Current activity", value=self.fetch_activity(author.activity), inline=False)
        author_info.add_field(name="Server roles", value=", ".join(server_roles))

        await ctx.send(embed=author_info)

    # TODO: Timeout for this command? (For way too big calculations)
    @commands.command(name="calc")
    @commands.guild_only()
    async def calculator(self, ctx: commands.Context, *, equation: str):
        replace_pairs = [("^", " ^ "), ("**", " ^ "), (",", "."), ("+", " + "), ("-", " - "), ("*", " * "),
                         ("/", " / ")]
        for pair in replace_pairs:
            equation = equation.replace(pair[0], pair[1])

        try:
            solution = mathparse.parse(equation)
        except IndexError:
            await ctx.send("The equation was not in supported format. Try to put parts of it inside brackets, or "
                           "see the supported operations via command `!help calc`.")
            return
        except ValueError:
            await ctx.send("Could not calculate some part of the equation. All the possible errors are not known yet, "
                           "so try to do this calculation in parts.")
            return
        except KeyError:
            await ctx.send("The equation contained factors that could not be converted into mathematical operators.")
            return
        except OverflowError:
            await ctx.send("The equation result was to big for this command.")
            return
        if type(solution) is str:
            solution_formatted = solution
        else:
            solution_formatted = f"{round(solution, 3):,}".replace(",", " ")
        await ctx.send(solution_formatted)

    @commands.command(name="beer", aliases=["drink"])
    @commands.guild_only()
    async def add_drink(self, ctx: commands.Context):
        pass

    @commands.command(name="undrink", aliases=["unbeer", "puke"])
    @commands.guild_only()
    async def remove_drink(self, ctx: commands.Context):
        pass

    @commands.command(name="beerscores", aliases=["beers", "drinks"])
    @commands.guild_only()
    async def beerscores(self, ctx: commands.Context):
        pass

    @commands.command(name="reminder", aliases=["remindme"])
    @commands.guild_only()
    async def add_reminder(self, ctx: commands.Context, *args):
        pass

    @commands.command(name="roll", aliases=["dice", "die"])
    async def roll_die(self, ctx: commands.Context, dice_options: Union[str, int] = 6):
        max_dices = 20
        max_sides = 120

        try:
            dice_options = dice_options.split("d")

            # User gave only sides
            if len(dice_options) == 1:
                sides = int(dice_options[0])
                rolls = 1
            # User gave either RPG dice notation or invalid format
            elif len(dice_options) == 2:
                sides = int(dice_options[1])
                rolls = int(dice_options[0])
            else:
                raise IndexError()
        except AttributeError:
            sides = dice_options
            rolls = 1
        except (ValueError, IndexError):
            await ctx.send("Die info was given in invalid format.")
            return

        if sides > 120:
            await ctx.send(f"The die can only have maximum of {max_sides} sides.")
            return
        elif rolls > max_dices:
            await ctx.send(f"You can throw at most {max_dices} dice at once.")
            return
        elif sides < 1:
            await ctx.send("The die must have at least 1 sides.")
            return
        elif rolls < 1:
            await ctx.send("The die must be thrown at least once.")
            return

        roll_results = [random.randint(1, sides) for _ in range(rolls)]
        if rolls > 1:
            results = ", ".join(str(_int) for _int in roll_results)
            msg = f"{sides}-sided die roll results: `{results}`\n\nTotal sum: {sum(roll_results)}"
        else:
            msg = roll_results[0]

        await  ctx.send(msg)

    @commands.command(name="scommands", aliases=["servercommands", "customcommands", "ccommands"])
    @commands.guild_only()
    async def get_server_commands(self, ctx: commands.Context):
        await ctx.send("yeet")

    @commands.command("commands")
    async def get_all_commands(self, ctx: commands.Context):
        pass

#     TODO: Mod commands and settings commands here?


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(DiscordCog(bot))
