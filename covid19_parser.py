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

import pytz
import aiohttp
import asyncio
import traceback
import sys
import datetime
from typing import Tuple, Union


class __UrlContainer:
    def __init__(self):
        self.hospital_data_url = "https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaHospitalData"
        self.corona_data_url = "https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData/v2"
        self.vaccination_data_url = "https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishVaccinationData"
        self.corona_icon_url = "https://i.imgur.com/lQ5ecBe.png"


urls = __UrlContainer()


class CovidFiParser:

    def __init__(self, loop: asyncio.BaseEventLoop = asyncio.get_event_loop()):
        self.local_tz = pytz.timezone("Europe/Helsinki")
        self.__client_session = aiohttp.ClientSession(loop=loop)

        # Data variables
        self.hospitalised_data: dict = dict()
        self.corona_data: dict = dict()
        self.vaccination_data: dict = dict()
        self.update_timestamp: Union[None, datetime.datetime] = None

        # Cache update cooldown in minutes
        self.cooldown = 30
        # Start the loop for caching
        loop.create_task(self.__cache_loop())

    @staticmethod
    async def __fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
        """
        Fetch url content. The response must be in json format.

        :param session: ClientSession that is used to fetch the url
        :param url: Url to fetch
        :return: The response parsed into a dictionary
        """
        if url is None:
            raise ValueError("Url can not be None.")
        async with session.get(url, timeout=10) as resp:
            if resp.status != 200:
                resp.raise_for_status()
            return await resp.json()

    async def get_raw_data(self) -> Tuple[dict, dict, dict]:
        """
        Get the raw data of both corona data and hospitalized data. This data contains all information that the
        response from Helsingin Sanomat APIs provide. No any extra parsing.
        :return: Tuple of summarized data, where the corona data is first, then hospitalized data.
        """
        if not self.corona_data or not self.hospitalised_data or not self.vaccination_data:
            raise ValueError("Cache has not been updated properly yet.")
        return self.corona_data, self.hospitalised_data, self.vaccination_data

    async def get_summarized_data(self) -> Tuple[dict, dict, dict]:
        """
        Get summarized corona data, hospitalized data and vaccination data based on the latest data synchronization.
        The corona data contains the amount of confirmed cases and deaths, and the health care
        district for the latest report in both categories.
        Hospitalized data contains the amount of people requiring health care services. They are categorized into
        categories in ward, in ICU and total.
        Vaccination data contains the amount of vaccinations in whole area of Finland.

        :return: Tuple of summarized data, where the data is in order (corona_data, hospitalized, vaccinations)
        """
        raw_data = await self.get_raw_data()
        corona_data = raw_data[0]
        hospitalised_data = raw_data[1]
        vaccination_data = raw_data[2]
        summarized_corona = \
            {
                "confirmed": {"count": 0, "last_case": None},
                "deaths": {"count": 0, "last_case": None}
            }
        # Hospital data and vaccination data are in much simpler format
        summarized_hospital = hospitalised_data["hospitalised"][-1]
        summarized_vaccination = vaccination_data[-1]

        summarized_corona["confirmed"]["count"] = len(corona_data["confirmed"])
        last_case = corona_data["confirmed"][-1]
        summarized_corona["confirmed"]["last_case"] = last_case

        summarized_corona["deaths"]["count"] = len(corona_data["deaths"])
        last_case = corona_data["deaths"][-1]
        summarized_corona["deaths"]["last_case"] = last_case

        return summarized_corona, summarized_hospital, summarized_vaccination

    # todo: Implement this and return with summarized
    def __get_daily_cases(self) -> dict:
        """
        Get the new cases that were reported during the last day. Can also be negative, if some of the cases are
        removed. The data is parsed into signed format into categories confirmed and deaths.
        :return: Dictionary containing new daily corona cases and deaths as a signed numbers.
        """
        utc_now = datetime.datetime.utcnow()
        daily_cases = {"confirmed": 0, "deaths": 0, "vaccinations": 0}

        return daily_cases

    async def __cache_loop(self) -> None:
        """
        A loop that runs indefinitely. Updates the internally cached data, to enhance the speed of responses when
        data is requested. The data is updated only a few times in a day, so frequent updating is not needed.
        """
        failed_updates = 0
        cooldown_min = self.cooldown * 60
        async with self.__client_session as session:
            while True:
                try:
                    results = await asyncio.gather(self.__fetch_url(session, urls.hospital_data_url),
                                                   self.__fetch_url(session, urls.corona_data_url),
                                                   self.__fetch_url(session, urls.vaccination_data_url))
                    self.hospitalised_data = results[0]
                    self.corona_data = results[1]
                    self.vaccination_data = results[2]
                    self.update_timestamp = datetime.datetime.utcnow()
                    failed_updates = 0
                except Exception as e:
                    print(f"Exception during cache update.")
                    traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
                    failed_updates += 1

                    if failed_updates < 3:
                        print("Trying to update again in 30 seconds.")
                        await asyncio.sleep(30)
                        continue
                    else:
                        print(f"Failed to update cache 3 times in a row. Taking the usual {cooldown_min} minute break.")

                await asyncio.sleep(cooldown_min)


if __name__ == '__main__':
    parser = CovidFiParser()
