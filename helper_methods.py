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
from caching import Cache
from typing import Union
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

tz_fi = pytz.timezone("Europe/Helsinki")


def localize_timestamp(original_ts: Union[str, datetime.datetime], fmt: str = "%Y-%m-%d %H:%M") -> str:

    dt = dateutil.parser.parse(str(original_ts)).replace(microsecond=0, tzinfo=None)
    localized = pytz.utc.localize(dt).astimezone(tz_fi).strftime(fmt)
    return localized


def isofy_timestamp(original_ts: datetime.datetime, date_only: bool = False) -> str:
    if date_only:
        result = original_ts.strftime("%Y-%m-%d")
        return result
    else:
        result = str(original_ts.replace(microsecond=0))

    return result


def titlecase(original: str, delimiter: str = " ", small_words: list = None) -> str:
    """
    Convert a string into titlecase format, because the builtin title-method capitalizes all words and letters
    after apostrophe characters.

    :param original: Original string that is titlecased.
    :param delimiter: Delimiter to separate the words in string. Result is joined with same delimiter.
    :param small_words: Words that are skipped for capitalization. If given, collisions are eliminated with default
                        small words.
    :return:
    """
    small_words_ = ["of", "in", "at", "to", "the", "on", "an", "a"]
    if small_words:
        list(set(small_words_ + small_words))

    original_splitted = original.split(delimiter)
    result = []

    for word in original_splitted:
        word = word.lower()
        if word in small_words_:
            result.append(word)
        else:
            result.append(word.capitalize())

    return delimiter.join(result)


def parse_wiki_search_candidates(search_result: str, base_url: str, cache: Cache = None) -> list:
    """
    Parse potential matches for a wiki search in a "Did you mean?" manner. Supports the official osrs wiki and
    melvoridle wiki. If a cache object is passed, all wiki page urls found are added into it so they can be found

    :param search_result:
    :param base_url:
    :param cache:
    :return:
    """
    hyperlinks_list = []

    results_html = BeautifulSoup(search_result, "html.parser")
    html_headings = results_html.findAll("div", class_="mw-search-result-heading")

    for heading in html_headings:
        heading_a = heading.find("a")
        heading_link_end = heading_a["href"]
        heading_title = heading_a["title"]
        heading_link = f"{base_url}{heading_link_end}"

        if cache is not None:
            cache.add(heading_link)

        if heading_link[-1] == ")":
            heading_link = list(heading_link)
            heading_link[-1] = "\\)"
            heading_link = "".join(heading_link)

        hyperlink = f"[{heading_title}]({heading_link})"
        hyperlinks_list.append(hyperlink)

    return hyperlinks_list


def parse_message(string: str):
    return string.replace("\\\\n", "n").replace("\\n", "\n")


def string_to_timedelta(time_string: str) -> relativedelta:
    """
    Convert string from format '[years][months][days][hours][minutes][seconds]' to relativedelta object. Any time unit
    can be left out if not needed.
    :param time_string: Relative time in string format
    :return: datetutil.relativedelta.relativedelta object
    """

    replace_dict = {"years": "yrs",
                    "yrs": "y",
                    "months": "mon",
                    "mon": "m",
                    "days": "d",
                    "hours": "H",
                    "h": "H",
                    "minutes": "min",
                    "min": "M",
                    "seconds": "sec",
                    "sec": "S",
                    "s": "S",
                    " ": ""}

    for old in replace_dict.keys():
        new = replace_dict[old]
        time_string = time_string.replace(old, new)

    time_units = {"y": 0, "m": 0, "d": 0, "H": 0, "M": 0, "S": 0}

    # Extract all different time units from string
    for char in time_string:
        if char not in list(time_units):
            if not char.isdigit():
                raise ValueError("Invalid character in timedelta string.")
            continue

        char_idx = time_string.find(char)
        time_units[char] = int(time_string[:char_idx])

        target_substring = time_string[:char_idx + 1]
        time_string = time_string.replace(target_substring, "")

    timedelta = relativedelta(years=time_units["y"],
                              months=time_units["m"],
                              days=time_units["d"],
                              hours=time_units["H"],
                              minutes=time_units["M"],
                              seconds=time_units["S"])
    return timedelta


if __name__ == '__main__':
    ts = datetime.datetime.utcnow().replace(microsecond=0)
    isofied = isofy_timestamp(ts)
    isofied2 = isofy_timestamp(ts, date_only=True)
    print(isofied)
    print(isofied2)
