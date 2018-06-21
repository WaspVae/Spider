# -*- coding:UTF-8 -*-
from requests_html import HTMLSession


def parse_html(res):
    targets = res.html.find('.listmain dd')
    titles = []
    hrefs = []
    for i in range(12, len(targets)):
        titles.append(targets[i].text)
        hrefs.extend(list(targets[i].links))
    return titles, hrefs


def get_onepage(first_url, title, href, session, book_name):
    url = first_url + href
    res = session.get(url=url)
    targets = res.html.find('#content')
    content = targets[0].text
    with open(book_name + '.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + title + '\n')
        f.write(content)


def main():
    first_url = 'http://www.biqukan.com'
    session = HTMLSession()
    targets_url = input('请输入你要下载的小说地址：')
    res = session.get(url=targets_url)
    book_name = res.html.find('.info h2')[0].text
    titles, hrefs = parse_html(res)
    for i in range(len(titles)):
        get_onepage(first_url, titles[i], hrefs[i], session, book_name)


if __name__ == '__main__':
    main()

