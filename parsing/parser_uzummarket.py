import os
import json

import aiohttp
import asyncio
import pyppeteer
import httpx

from bs4 import BeautifulSoup, BeautifulStoneSoup
from pprint import pprint

from functions import (
    get_hierarchical_dict_second,
    get_price_in_number,
    recursion_dict_extend_dict,
    filter_list
)

from core import ALLOWED_MARKS

uzum_market_categories = {
    'smartphone': {
        'category': 'category',
        'sub_category': 'smartfony-12690',
    }
}


class ParserUzumMarket:
    def __init__(self, category, sub_category):
        self.URL = "https://uzum.uz"
        self.category = category
        self.sub_category = sub_category

    async def fetch_html(self, url):
        browser = await pyppeteer.launch()
        page = await browser.newPage()
        await page.goto(url)
        html = await page.content()
        await browser.close()
        return html

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}/{self.sub_category}"

        if page is not None:
            url += f"?currentPage={page}"

        async with aiohttp.ClientSession() as session:
            session.headers.add(
                key="User-Agent",
                value="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )

            session.headers.add(
                'Accept',
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            )

            session.headers.add('scheme', 'https')

            async with session.get(url) as response:

                print("Status Code: " + str(response.status))

                if response.status == 200:
                    await asyncio.sleep(5)
                    html = await response.text()
                    soup = BeautifulSoup(html, "lxml")
                    print(soup)
                    return soup
                else:
                    return

    async def get_json_data(self):
        json_data = dict()
        total_page = await self.get_pagination_number()
        if not total_page.isdigit():
            raise Exception("Pagination number must be an integer")

        tasks = [self.get_page_data(page_number) for page_number in range(1, int(total_page) + 1)]
        page_data = await asyncio.gather(*tasks)

        await asyncio.gather(*[recursion_dict_extend_dict(json_data, data) for data in page_data])
        return json_data

    async def get_page_data(self, page_number: int):
        page_data: dict = {}

        soup = await self.get_soup(page_number)
        cards = soup.find_all("div", class_="product-card")

        print(soup)

    async def get_pagination_number(self):
        soup = await self.get_soup()
        return 27

    async def write_json_file(self):
        json_data = await self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open('json_data/uzummarket.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    async def run(self):
        await self.write_json_file()


parser = ParserUzumMarket(
    category=uzum_market_categories['smartphone']['category'],
    sub_category=uzum_market_categories['smartphone']['sub_category']
)

if __name__ == "__main__":
    response = httpx.get('https://uzum.uz', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})
    print(response.text)

# asyncio.run(parser.get_soup(1))
# start_time = time.perf_counter()
# while True:
#     print('Start parsing!...')
#     try:
#         asyncio.run(parser.run())
#         break
#     except Exception as e:
#         end_time = time.perf_counter()
#         total_time = round(end_time - start_time, 3)
#         print('Total time: ' + str(total_time))
#         print(e)
#         print('Parsing is sleeping!...')
#         time.sleep(5)
#         start_time = time.perf_counter()
# end_time = time.perf_counter()
# total_time = round(end_time - start_time, 3)
# print('Total time: ' + str(total_time))
