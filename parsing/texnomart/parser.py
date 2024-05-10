from parsing.parsers import *

categories = {
    'smartphone': {
        'category': 'katalog',
        'subcategory': 'smartfony',
    }
}

dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, dirname):
        super().__init__(dirname)
        self.URL = "https://texnomart.uz"
        self.category = category
        self.subcategory = subcategory

    async def get_soup(self, page=None):
        url = f"{self.URL}/ru/{self.category}/{self.subcategory}/"

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

    async def get_page_data(self, page_number, i=0) -> dict:

        page_data: dict = {}
        soup = await self.get_soup(page_number)

        cards = soup.find_all("div", class_="product-item-wrapper")

        for card in cards:

            link = self.URL + card.find("a", class_="product-name")['href']
            title = card.find("a", class_="product-name").get_text(strip=True)
            price = get_number_from_text(card.find("div", class_="product-price__current").get_text(strip=True))
            price_credit = get_number_from_text(card.find("div", class_="installment-price").get_text(strip=True))

            data = {
                'link': link,
                'title': title,
                'price': price,
                'price_credit': price_credit,
            }

            page_data[str(i)] = data
            i += 1
        print(len(page_data))
        return page_data

    async def get_total_page(self) -> int:
        soup = await self.get_soup()
        pagination = soup.select(
            "#catalog__page > div.catalog-content__products > div:nth-child(2) > div.pagination > div > div.vue-ads-flex-grow.vue-ads-flex.vue-ads-justify-end > button:nth-child(8)")
        number = pagination[0].get_text(strip=True)
        if number:
            print("Total pages:", number)
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
