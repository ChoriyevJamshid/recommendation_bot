from parsing.parsers import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

categories = {
    'smartphone': {
        'category': 'category',
        'subcategory': 'smartfony-12690',
    }
}

dir_name = str(os.path.dirname(__file__)).split('/')[-1]


def recursion_dict_extend_dict(main: dict, second: dict) -> None:
    for key, value in second.items():
        if key not in main.keys():
            main[key] = value
        else:
            if isinstance(main[key], dict):
                recursion_dict_extend_dict(main[key], value)


def append_dict(main: dict, second: dict, number: int) -> None:
    main[number] = second


class Parser(BaseParser):

    def __init__(self, category, subcategory, dirname):
        super().__init__(dirname)

        self.category = category
        self.subcategory = subcategory

        self.URL = f'https://uzum.uz'
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

    def get_soup(self, page=None):
        browser = webdriver.Chrome()
        browser.get(self.URL + f"/{self.category}/{self.subcategory}")
        time.sleep(10)
        html = browser.page_source

        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)
        return soup

    def get_json_data(self):

        json_data = dict()
        total_page = self.get_total_page()
        if not total_page:
            raise Exception("Pagination number must be an integer")

        for page_number in range(1, total_page + 1):
            page_data = self.get_page_data(page_number, total_page * (page_number - 1))
            append_dict(json_data, page_data, page_number)

        return json_data

    def get_page_data(self, page_number, i=0) -> dict:

        page_data = dict()
        soup = self.get_soup(page_number)
        cards_div = soup.find("div", id="category-products")

        cards = cards_div.find_all("div", class_="product-card")
        # print(cards)
        for card in cards:
            card_block = card.find("div", class_="card-info-block")

            link = self.URL + card_block.find("a", class_="subtitle-item")['href']
            title = card_block.find("a", class_="subtitle-item").get_text(strip=True)
            price_credit = get_number_from_text(card_block.find("div", class_="badge").get_text(strip=True))
            price = get_number_from_text(card.find("span", class_="product-card-price").get_text(strip=True))

            data = {
                'link': link,
                'title': title,
                'price': price,
                'price_credit': price_credit,
            }

            i += 1
            page_data[i] = data
        pprint(page_data)
        return page_data

    def get_total_page(self) -> int:
        soup = self.get_soup()
        return 27

    def write_json_file(self):
        json_data = self.get_json_data()
        os.makedirs('json_data', exist_ok=True)
        with open(f'json_data/{str(self.dirname)}.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    def run(self):
        self.write_json_file()


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
            parser.run()
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
