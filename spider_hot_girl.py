import requests
from bs4 import BeautifulSoup
import os

Hostreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mzitu.com'
}
Picreferer = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://i.meizitu.net'
}
# 此请求头破解盗链


# 保存地址
path = 'E:/mzitu/'

# 找寻最大页数
# domain = 'http://www.mzitu.com'
# start_html = requests.get(domain, headers=Hostreferer)
# soup = BeautifulSoup(start_html.text, "lxml")
# page = soup.find_all('a', class_='page-numbers')
# max_page = page[-2].text
max_page = int(input('请输入爬取页面数量：'))
url = 'http://www.mzitu.com/page/'
for n in range(1, int(max_page) + 1):
    url += str(n)
    start_html = requests.get(url, headers=Hostreferer)
    soup = BeautifulSoup(start_html.text, "lxml")
    targets = soup.find('div', class_='postlist').find_all('a', target='_blank')
    for each in targets:
        title = each.get_text()  # 提取文本
        if title:
            print(f'正在爬取：{title}')
            if os.path.exists(path + title): 
                flag = 1
            else:
                os.makedirs(path + title)
                flag = 0
            os.chdir(path + title)
            href = each['href']
            html = requests.get(href, headers=Hostreferer)
            mess = BeautifulSoup(html.text, "lxml")
            pic_max = mess.find(class_='pagenavi').find_all('span')
            pic_max = pic_max[-2].text  # 最大页数
            if flag == 1 and len(os.listdir(path + title)) >= int(pic_max):
                print('已经保存完毕，跳过')
                continue
            for num in range(1, int(pic_max) + 1):
                pic = href + '/' + str(num)
                html = requests.get(pic, headers=Hostreferer)
                mess = BeautifulSoup(html.text, "lxml")
                pic_url = mess.find('img', alt=title)
                html = requests.get(pic_url['src'], headers=Picreferer)
                file_name = pic_url['src'].split(r'/')[-1]
                with open(file_name, 'wb') as f:
                    f.write(html.content)
    print(f'第{n}页爬取完成')
