import os
import json
import time
import selenium
import requests
import aiohttp
import asyncio
import pyppeteer
from bs4 import BeautifulSoup
from pprint import pprint


ALLOWED_MARKS = ('apple', 'samsung', 'iphone', 'xiaomi', 'huawei', 'blackview',
                 'zte', 'vivo', 'oppo', 'honor', 'techno', 'infinix', 'oppo', 'realme', 'google')


async def recursion_dict_extend_dict(main: dict, second: dict) -> None:
    for key, value in second.items():
        if key not in main.keys():
            main[key] = value
        else:
            if isinstance(main[key], dict):
                await recursion_dict_extend_dict(main[key], value)


def get_number_from_text(text: str) -> int:
    result = str()
    for letter in text:
        if letter.isdigit():
            result += letter
    if result.isdigit():
        return int(result)


class BaseParser:
    def __init__(self, dirname: str = ''):
        self.dirname = dirname

    def fetch(self, url, headers=None):
        response = requests.get(url)
        if headers is not None:
            response.headers.update(**headers)
        return response.text

    async def async_fetch(self, url, headers=None):
        async with aiohttp.ClientSession() as session:
            if headers:
                session.headers.extend(**headers)
            async with session.get(url) as response:
                return await response.text(), response.status

    async def get_json_data(self):
        json_data = dict()
        total_page: int = await self.get_total_page()

        if total_page == 0:
            raise Exception("Not found total page!")

        tasks = [self.get_page_data(page_number, total_page * (page_number - 1))
                 for page_number in range(1, total_page + 1)]

        page_data = await asyncio.gather(*tasks)
        for data in page_data:
            pprint(data)
        await asyncio.gather(*[recursion_dict_extend_dict(json_data, data) for data in page_data])
        return json_data

    async def get_page_data(self, page_number, i=0) -> dict:
        pass

    async def get_total_page(self) -> int:
        return 1

    async def write_json_file(self):
        json_data = await self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open(f'json_data/{str(self.dirname)}.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    async def run(self):
        await self.write_json_file()
