import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv


# from selenium import webdriver
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
def get_one_page(url, headers):
    response = requests.get(url, headers=headers)
    return response.text


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    movies = []
    targets = soup.find_all(class_='name')
    for item in targets:
        movies.append(item.get_text())
    stars = []
    targets = soup.find_all(class_='star')
    for item in targets:
        stars.append(item.get_text())
    releasetime = []
    targets = soup.find_all(class_='releasetime')
    for item in targets:
        releasetime.append(item.get_text())
    targets = soup.find_all(class_='score')
    score = []
    for item in targets:
        score.append(item.get_text())
    result = []
    for i in range(len(movies)):
        result.append([movies[i], stars[i].split('：')[1].strip(), releasetime[i].split('：')[1].strip(), score[i]])
    return result


def save_to_excel(result):
    with open('猫眼.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['电影名', '主演', '上映时间', '评分'])
        for i in range(len(result)):
            writer.writerow(result[i])


def main():
    result = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    }
    for i in range(10):
        url = 'http://maoyan.com/board/4?offset=' + str(i * 10)
        html = get_one_page(url, headers)
        result.extend(parse_one_page(html))
    save_to_excel(result)


if __name__ == '__main__':
    main()


'''法二(采用requests-html)来获取'''
# from requests_html import HTMLSession
# import csv
#
# session = HTMLSession()
# url = 'http://maoyan.com/board/4?offset=0'
# res = session.get(url)
# html = res.text
# targets = res.html.find('.name')
# movies = []
# for item in targets:
#     movies.append(item.text)
# targets = res.html.find('.star')
# stars = []
# for item in targets:
#     stars.append(item.text)
# targets = res.html.find('.releasetime')
# releasetime = []
# for item in targets:
#     releasetime.append(item.text)
# targets = res.html.find('.score')
# scores = []
# for item in targets:
#     scores.append(item.text)
# with open('法二.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['电影名', '主演', '上映时间', '评分'])
#     for i in range(len(movies)):
#         writer.writerow([movies[i], stars[i], releasetime[i], scores[i]])
'''法三(采用selenium模拟登陆)'''
# from selenium import webdriver
# import csv
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
# url = 'http://maoyan.com/board/4?offset=0'
# with open('法三.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['电影名', '主演', '上映时间', '评分'])
#     i = 10
#     while i < 110:
#         browser.get(url)
#         data = browser.find_element_by_class_name('board-wrapper').find_elements_by_tag_name('dd')
#         for item in data:
#             movie = item.find_element_by_class_name('name').text
#             star = item.find_element_by_class_name('star').text
#             releasetime = item.find_element_by_class_name('releasetime').text
#             score = item.find_element_by_class_name('score').text
#             writer.writerow([movie, star, releasetime, score])
#         url = 'http://maoyan.com/board/4?offset=' + str(i)
#         i += 10
