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
import datetime
import dateutil.parser
from typing import Union
import aiohttp

tz_fi = pytz.timezone("Europe/Helsinki")


def localize_timestamp(original_ts: Union[str, datetime.datetime], fmt: str = "%Y-%m-%d %H:%M") -> str:
    dt = dateutil.parser.parse(str(original_ts)).replace(microsecond=0, tzinfo=None)
    localized = pytz.utc.localize(dt).astimezone(tz_fi).strftime(fmt)
    return localized


async def fetch_url(session: aiohttp.ClientSession, url: str) -> aiohttp.ClientResponse:
    if url is None:
        raise ValueError("Url can not be None.")
    async with session.get(url, timeout=10) as resp:
        if resp.status != 200:
            resp.raise_for_status()
        return resp

if __name__ == '__main__':
    a = localize_timestamp("2020-12-29T15:00:00.000Z")
    print(a)
    print(type(a))

