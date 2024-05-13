from parsing.parsers import *
from functions import get_hierarchical_dict, filter_items

categories = {
    'smartphone': {
        'category': 'smartfony',
        'subcategory': '',
    }
}
dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, dirname):
        super().__init__(dirname)
        self.URL = 'https://market.beeline.uz'
        self.category = category
        self.subcategory = subcategory
        self.function = recursion_dict_extend_dict
        self.get_hierarchical_dict = get_hierarchical_dict

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}"

        # print(f'\n{url}\n')

        if page is not None:
            url += f"?page={page}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        html, status = await self.async_fetch(url=url, headers=headers)
        # print(f"\nStatus code: {status}\n")
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    async def get_page_data(self, page_number) -> dict:

        page_data: dict = {}
        soup = await self.get_soup(page_number)

        cards = soup.find_all('a', class_='product-card')
        index = 0
        for index, card in enumerate(cards):
            link = self.URL + card['href']
            title = card.find("h3", class_="product-card__name").get_text(strip=True)
            price = get_number_from_text(card.find("p", class_="text-base").get_text(strip=True))

            data = {
                'link': link,
                'title': title,
                'price': price,
            }

            items = title.lower().split(' ')
            items = filter_items(items)
            print(items)
            # page_data[str(index + 1)] = data
            self.get_hierarchical_dict(page_data, items, data)

        print(f'\nPage number: {page_number}, append = {index + 1} elements\n')
        return page_data

    async def get_total_page(self) -> int:
        soup = await self.get_soup()
        pagination = soup.find_all("button", class_="app-pagination__num-btn")[-1]
        number = pagination.get_text(strip=True)
        if number:
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
