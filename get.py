import requests
from bs4 import BeautifulSoup
import os
books = []
with open('list.txt', 'r', encoding='utf-8') as f:
    s = f.read().strip()
s = s.split('\n')
for i in s:
    books.append((i.split(':')[0], i.split(':')[1].split(' ')[1]))
def get_text(id):
    base = 'http://lw.131453.xyz'
    if not id.isdigit():
        url = base + '/' + str(id)
    else:
        url = base + '/book/' + str(id)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = BeautifulSoup(req.text, 'html.parser')
    div = soup.find_all('div', id='play_0')[0]
    links = div.find_all('a')
    if id == 'guangzhizi':
        div = soup.find_all('ul')[1:13]
        links = sum([ul.find_all('a') for ul in div], [])
    title = soup.find_all('h1')[0].text
    dir = './books/' + title
    if not os.path.exists(dir):
        os.makedirs(dir)
    total = len(links)
    print('总共有', total, '章')
    if total == len(os.listdir(dir)):
        print('已下载完成')
        return
    for i, link in enumerate(links):
        href = base + link.get('href')
        name = str(i + 1).zfill(len(str(total))) + link.text
        chars = r'\/:*?"<>|' + '\n\r\t'
        for c in chars:
            name = name.replace(c, '')
        if os.path.exists(dir + '/' + name + '.txt'):
            continue
        req = requests.get(href, headers=headers)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, 'html.parser')
        content = soup.find_all('div', id='content')[0]
        paras = content.find_all('p')[1:]
        content = ''
        for p in paras:
            content += p.text + '\n'
        with open(dir + '/' + name + '.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        print(name)
for j, i in enumerate(books):
    if j < len(books) - 1 and os.path.exists('./books/' + books[j + 1][1]):
        continue
    print(i[0])
    get_text(i[0])