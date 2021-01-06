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

