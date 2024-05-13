ru_en = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'ж': 'j',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'x',
    'э': 'e'
}


def convert_en(text: str) -> str:
    result = ''
    for letter in text.lower():
        if letter in ru_en.keys():
            letter = ru_en[letter]
        result += letter
    return result


def get_number_from_text(text: str) -> int:
    result = str()
    for letter in text:
        if letter.isdigit():
            result += letter
    if result.isdigit():
        return int(result)


def is_pow_number(number: int, degree: int):
    if isinstance(number, int):
        while number > 1:
            number /= degree
        if number == 1:
            return True
    return False


def remove_alpha(letters: str):
    result = ''
    for letter in letters:
        if ord('/') <= ord(letter) <= ord("9"):
            result += letter
    return result


def filter_items(items: list):
    i = 2
    while True:
        if '/' in items[i]:
            items[i] = remove_alpha(items[i])

            break

        elif 'gb' in convert_en(items[i]) or 'tb' in convert_en(items[i]):
            break

        elif i == len(items) - 1:
            break
        i += 1
    items = items[:i + 1]

    while len(items) > 5:
        if i == len(items) - 1:
            items.pop(i - 1)
            i -= 1
        elif i < len(items):
            items.pop(i + 1)

    return items


def get_hierarchical_dict(data: dict, items: list | tuple, new_data: dict) -> None:
    current_dict = data
    for index, item in enumerate(items):
        if current_dict.get(item) is None:
            if index == len(items) - 1:
                current_dict[item] = new_data
            else:
                current_dict[item] = {}
        current_dict = current_dict[item]


if __name__ == "__main__":
    # items = ['huawei', 'nova', '10', 'se', '8/128', 'гб,', 'серый']
    # data = {
    #     "one": {},
    #     "two": {
    #         "three": {},
    #         "four": {}
    #     }
    # }
    #
    # get_hierarchical_dict(data, ["two", "three", "five"], {'new_data': 'new_data', 'data': 'data'})
    #
    # print(data)
    pass
    print(ord("9"))



