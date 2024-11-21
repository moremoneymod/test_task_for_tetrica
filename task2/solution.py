from bs4 import BeautifulSoup
import requests
import csv

base_link = "https://ru.wikipedia.org"


def parse_wiki(link):
    current_link = link

    flag = True

    animals_dict = {chr(i): 0 for i in range(ord('А'), ord('Я') + 1)}
    animals_dict['Ё'] = 0

    while flag:
        response = requests.get(url=current_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        data_section = soup.find(class_="mw-category mw-category-columns")
        columns = data_section.find_all(class_="mw-category-group")
        for index in range(len(columns)):
            animals_data = columns[index].ul
            for animal in animals_data:
                text = animal.text
                dict_key = text[0]
                if dict_key not in animals_dict and dict_key != '\n':
                    flag = False
                    break
                if text != '\n':
                    animals_dict[dict_key] += 1
        next_page = soup.find_all(title="Категория:Животные по алфавиту")[-1]
        if next_page.text == "Следующая страница":
            current_link = base_link + next_page.get("href")

    with open("beasts.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for (letter, count) in animals_dict.items():
            writer.writerow([f"{letter},{count}"])


# Ссылки для теста: 1 ссылка - для проверки парсинга всех животных, 2 ссылка - середина списка всех животных, 3 ссылка - переход от русскоязычных названий к англоязычным
tests = [
    "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83",
    "https://ru.m.wikipedia.org/w/index.php?from=%D0%A1%D0%B6&title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83",
    "https://ru.m.wikipedia.org/w/index.php?from=%D0%AF%D1%89&title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"]

parse_wiki(tests[0])
