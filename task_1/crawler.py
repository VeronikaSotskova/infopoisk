import shutil

import requests

from bs4 import BeautifulSoup


def get_next_link(bs):
    """
    :param bs: BeautifulSoup
    :return: next_link: Optional[str]

    Метод принимает объект BeautifulSoup со страницей поста, ищет ссылку на следующий пост
    Возвращает ссылку на следующий пост, если она есть; иначе возвращает None
    """
    a_tags = bs.select("a.b-controls-prev")
    if len(a_tags) > 0:
        for a in a_tags:
            if a.attrs.get("title") == "Previous" and a.attrs.get("href") is not None:
                r = requests.get(a.attrs["href"])
                return r.url
    else:
        return None


def main():
    i = 1
    link_start = 'https://skorobogatov.livejournal.com/90782.html'
    index = open("index.txt", "w", encoding="utf-8")

    # скачиваем страницы до тех пор, пока есть ссылка на следующий пост и количество страниц <= 100
    while link_start is not None and i <= 100:
        print(f"Парсинг {i}-ой страницы")
        response = requests.get(link_start)
        soup = BeautifulSoup(response.text, 'html.parser')
        site = open(f"sites/{i}.txt", "w", encoding="utf-8")

        text = soup.select('article.entry-content')[0].text.split('\n')[0]
        h1 = soup.select('h1')[0].text.strip()

        # записываем заголовок статьи и ее содержание
        site.write(f"{h1}\n{text}")
        site.close()
        index.write(f"{i} {link_start}\n")
        i += 1
        link_start = get_next_link(soup)

    index.close()
    shutil.make_archive("выкачка", 'zip', "sites")


main()
