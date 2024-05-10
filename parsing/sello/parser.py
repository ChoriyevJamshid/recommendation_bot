from parsing.parsers import *

categories = {
    'smartphone': {
        'category': 'telefony-i-smart-casy',
        'subcategory': 'smartfony',
    }
}
dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, dirname):
        super().__init__(dirname)
        self.URL = 'https://sello.uz'
        self.category = category
        self.subcategory = subcategory

    async def get_soup(self, page=None):
        url = f"{self.URL}/category/elektronika/{self.category}/{self.subcategory}"

        print(f'\n{url}\n')

        if page is not None:
            url += f"?page={page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        html, status = await self.async_fetch(url=url, headers=headers)
        print(f"\nStatus code: {status}\n")
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    async def get_page_data(self, page_number, i=0) -> dict:

        page_data: dict = {}
        soup = await self.get_soup(page_number)

        cards = soup.find_all('div', class_='col mb-3')

        for index, card in enumerate(cards):
            link = self.URL + card.find('a', class_="d-block p-1")['href']
            title = card.find("span", class_="t-truncate-4").get_text(strip=True)
            price = get_number_from_text(
                card.select(f"#__next > div.w-100.h-100.mt-2.mt-lg-0.mb-3 > div.container.py-2 > div.d-block.d-md-flex > div:nth-child(2) > div.row.gx-2.gx-lg-3.row-cols-2.row-cols-sm-3.row-cols-md-4.row-cols-lg-5.row-cols-xl-5 > div:nth-child({index + 1}) > div > div.px-2.pb-3.position-relative > div")[0].get_text(strip=True))

            data = {
                'link': link,
                'title': title,
                'price': price,
            }

            i += 1
            page_data[str(i)] = data
        return page_data

    async def get_total_page(self) -> int:
        soup = await self.get_soup()
        pagination = soup.find_all("li", class_="page-item")[-2]
        number = pagination.get_text(strip=True)
        if number:
            print(number)
            return int(number)
        return 0


if __name__ == '__main__':
    parser = Parser(
        categories['smartphone']['category'],
        categories['smartphone']['subcategory'],
        dir_name
    )

    start_time = time.perf_counter()
    while True:
        print('Start parsing!...')
        try:
            asyncio.run(parser.run())
            break
        except Exception as e:
            end_time = time.perf_counter()
            total_time = round(end_time - start_time, 3)
            print('Total time: ' + str(total_time))
            print(e)
            print('Parsing is sleeping!...')
            time.sleep(5)
            start_time = time.perf_counter()
    end_time = time.perf_counter()
    total_time = round(end_time - start_time, 3)
    print('Total time: ' + str(total_time))
