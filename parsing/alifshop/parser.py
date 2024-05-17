from parsing.base.parser import *

categories = {
    'smartphone': {
        'category': 'categories',
        'subcategory': 'smartfoni-i-telefoni',
    }
}
dir_name = str(os.path.dirname(__file__)).split('/')[-1]


class Parser(BaseParser):
    def __init__(self, category, subcategory, dirname):
        super().__init__(dirname)
        self.URL = 'https://alifshop.uz'
        self.category = category
        self.subcategory = subcategory
        self.function = append_dict

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

    async def get_page_data(self, page_number) -> dict:

        page_data: dict = {}
        soup = await self.get_soup(page_number)

        main = soup.find("main", class_="flex-grow")
        cards = main.find_all("div", class_="h-full grid grid-cols-1 content-between")
        index = 0
        i = 0
        for index, card in enumerate(cards):

            link = self.URL + card.find("a", class_="cursor-pointer")["href"]
            title = card.find("p", class_="max-w-xs text-sm text-grey-900 line-clamp-2 text-ellipsis mb-1").get_text(
                strip=True)

            price_credit = card.find("strong", class_="mr-0.5 font-medium").get_text(strip=True)
            price: list = card.select_one(
                f"#__nuxt > div > div.flex.flex-col.h-full > main > div.container.mb-6 > div.flex.flex-col.gap-6.md\:flex-row.relative.w-full > div.md\:basis-5\/6.mb-12.w-full > div.grid.grid-cols-2.md\:grid-cols-3.lg\:grid-cols-4.gap-5.mb-9 > div:nth-child({index + 1}) > a > figure > figcaption > div > p.text-red.text-sm")

            if not price:
                price: list = card.select_one(
                    f"#__nuxt > div > div.flex.flex-col.h-full > main > div.container.mb-6 > div.flex.flex-col.gap-6.md\:flex-row.relative.w-full > div.md\:basis-5\/6.mb-12.w-full > div.grid.grid-cols-2.md\:grid-cols-3.lg\:grid-cols-4.gap-5.mb-9 > div:nth-child({index + 1}) > a > figure > figcaption > p.text-grey-400.text-sm")
            price, _ = price.get_text(strip=True).split(' ')

            price = get_number_from_text(price)
            price_credit = get_number_from_text(price_credit)

            if title.lower().split(" ")[1] in ALLOWED_MARKS:
                data = {
                    'link': link,
                    'title': title,
                    'price': price,
                    'price_credit': price_credit,
                }
                i += 1
            else:
                continue
            page_data[str(i)] = data
        print(f'\nPage number: {page_number}, append = {i} elements\n')
        return page_data

    async def get_total_page(self) -> int:
        soup = await self.get_soup()
        pagination = soup.find("nav", {"aria-label": "Pagination"}).get_text()
        number = pagination.split(' ')[-1]
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
