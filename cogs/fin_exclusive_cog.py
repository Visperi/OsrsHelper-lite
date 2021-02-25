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

import discord
from discord.ext import commands
import datetime
import json
import covid19_parser
import helper_methods


class FinExclusiveCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.covid_parser = covid19_parser.CovidParser(loop=bot.loop)

    @commands.command(name="satokausi")
    async def satokausi(self, ctx: commands.Context, *args):
        """
        A command function for getting list of fruits and vegetables that currently are in their harvest season.
        This command is currently exclusive to Finnish module.
        """

        months = ["tammikuu", "helmikuu", "maaliskuu", "huhtikuu", "toukokuu", "kesäkuu", "heinäkuu", "elokuu",
                  "syyskuu", "lokakuu", "marraskuu", "joulukuu"]
        if len(args) == 0:
            month_number = int(datetime.datetime.now().strftime("%m"))
            month_str = months[month_number - 1]
        else:
            try:
                month_str = args[0].lower()
                month_number = months.index(month_str) + 1
            except ValueError:
                await ctx.send("Anna kuukautta hakiessa sen nimi kirjoitettuna.")
                return

        with open("Data files/satokaudet.json", encoding="utf-8-sig") as data_file:
            data = json.load(data_file)
        kotimaiset = sorted(data[str(month_number)]["kotimaiset"])
        ulkomaiset = sorted(data[str(month_number)]["ulkomaiset"])
        embed = discord.Embed(title=f"Satokaudet {month_str}lle")
        embed.add_field(name="Kotimaiset", value="\n".join(kotimaiset))
        embed.add_field(name="Ulkomaiset", value="\n".join(ulkomaiset))

        await ctx.send(embed=embed)

    @commands.command(name="satokaudet")
    async def satokaudet(self, ctx: commands.Context):
        """
        A command function for searching when a given plant is in its harvest season. This command is currently
        exclusive to Finnish language.
        """

        months = ["tammikuu", "helmikuu", "maaliskuu", "huhtikuu", "toukokuu", "kesäkuu", "heinäkuu", "elokuu",
                  "syyskuu", "lokakuu", "marraskuu", "joulukuu"]
        search = ctx.message.content.split()[1]
        as_domestic = []
        as_foreign = []
        with open("Data files/satokaudet.json", encoding="utf-8-sig") as data_file:
            data = json.load(data_file)

        for month in data:
            month_name = months[int(month) - 1]
            if search in data[month]["kotimaiset"]:
                as_domestic.append(month_name)
            if search in data[month]["ulkomaiset"]:
                as_foreign.append(month_name)

        if not as_domestic and not as_foreign:
            await ctx.send("Antamallesi hakusanalle ei löytynyt satokausia.")
            return

        embed = discord.Embed(title=f"Satokaudet {search}lle")
        if as_domestic:
            embed.add_field(name="Kotimaisena", value="\n".join(as_domestic))
        if as_foreign:
            embed.add_field(name="Ulkomaisena", value="\n".join(as_foreign))
        await ctx.send(embed=embed)

    @staticmethod
    def __format_daily_differences(daily_cases: dict) -> dict:
        for key, diff in daily_cases.items():
            if diff == 0:
                daily_cases[key] = ""
            else:
                daily_cases[key] = f"({diff:+})"

        return daily_cases

    @commands.command(name="korona", aliases=["corona", "gorre"])
    async def get_corona_situation(self, ctx: commands.Context):
        """
        Get current status of Covid-19 (coronavirus) in Finland. This command is currently
        exclusive to Finnish language.
        """

        try:
            summarized_data = await self.covid_parser.get_summarized_data()
        except ValueError:
            await ctx.send("Dataa ei ole vielä päivitetty. Yritä hetken kuluttua uudelleen.")
            return

        update_ts = helper_methods.localize_timestamp(self.covid_parser.last_update_dt)
        embed = discord.Embed(title="Koronan tilanne Suomessa")
        embed.set_thumbnail(url=covid19_parser.urls.corona_icon_url)
        if self.covid_parser.update_in_progress:
            embed.set_footer(text="Datan päivitys oli parhaillaan käynnissä komennon aikana.\n"
                                  "Näytetty data ei välttämättä vastaa viimeisimpiä tietoja.")
        else:
            embed.set_footer(text=f"Data päivitetty viimeksi: {update_ts}")

        corona_data = summarized_data["corona_data"]
        hospital_data = summarized_data["hospitalised_data"]
        vaccination_data = summarized_data["shots_data"]
        daily_cases = summarized_data["daily_cases"].copy()
        daily_cases_formatted = self.__format_daily_differences(daily_cases)

        daily_confirmed = daily_cases_formatted["confirmed"]
        daily_deaths = daily_cases_formatted["deaths"]
        daily_total_hospitalized = daily_cases_formatted["totalHospitalised"]
        daily_in_ward = daily_cases_formatted["inWard"]
        daily_in_icu = daily_cases_formatted["inIcu"]
        daily_vaccinations = daily_cases_formatted["shots"]

        confirmed = corona_data["confirmed"]["count"]
        confirmed_last = corona_data["confirmed"]["last_case"]
        confirmed_last_area = confirmed_last["healthCareDistrict"]
        confirmed_last_ts = helper_methods.localize_timestamp(confirmed_last["date"])
        embed.add_field(name="Tartunnat", value=f"{confirmed} {daily_confirmed}\n"
                                                f"Viimeisin: {confirmed_last_ts}\n"
                                                f"Alue: {confirmed_last_area}")

        hospital_in_ward = hospital_data["inWard"]
        hospital_in_icu = hospital_data["inIcu"]
        hospital_total = hospital_data["totalHospitalised"]
        embed.add_field(name="Hoitoa vaativat", value=f"Osastohoidossa: {hospital_in_ward} {daily_in_ward}\n"
                                                      f"Tehohoidossa: {hospital_in_icu} {daily_in_icu}\n"
                                                      f"Yhteensä: {hospital_total} {daily_total_hospitalized}")

        deaths = corona_data["deaths"]["count"]
        deaths_last = corona_data["deaths"]["last_case"]
        deaths_last_area = deaths_last["area"]
        deaths_last_ts = helper_methods.localize_timestamp(deaths_last["date"])
        embed.add_field(inline=False, name="Menehtyneet", value=f"{deaths} {daily_deaths}\n"
                                                                f"Viimeisin: {deaths_last_ts}\n"
                                                                f"Alue: {deaths_last_area}")

        vaccinations_total = vaccination_data["shots"]
        vaccinations_last_ts = helper_methods.localize_timestamp(vaccination_data["date"])
        embed.add_field(inline=True, name="Rokotuksia", value=f"Yhteensä: {vaccinations_total} {daily_vaccinations}\n"
                                                              f"Viimeisin: {vaccinations_last_ts}\n"
                                                              f"Alue: Koko Suomi")

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(FinExclusiveCog(bot))
