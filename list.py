import requests
from bs4 import BeautifulSoup as bs
index = 42
with open('./list.txt', 'r', encoding='utf-8') as f:
    s = f.read().split('\n')
    if len(s) == 0:
        print('No data')
    else:
        index = int(s[-2].split(' ')[0][:-1])
        print(f'Read index {index}')
def get_info(idx, link):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
    req = requests.get(link, headers=headers)
    req.encoding = 'utf-8'
    b = bs(req.text, 'html.parser')
    h1s = str(b.h1)[4:-5]
    if '404' in h1s:
        return
    else:
        spans = b.select('body > div.container > div.row > div.col-xs-12.col-sm-12.col-md-9.col-lg-9 > div.m-book_info > div.m-infos > span:nth-child(2)')
        spans = str(spans)[7:-8]
        s = f'{idx}: {h1s} {spans}\n'
        return s
def main():
    with open('./list.txt', 'a', encoding='utf-8') as f:
        for i in range(index + 1, index + 1000):
            res = get_info(i, f'http://lw.131453.xyz/book/{i}/')
            if not res:
                print(f'No book {i}')
                continue
            print(res, end='')
            f.write(res)
def get_tjss():
    url = 'https://lw.131453.xyz/tangjiasanshao/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
    req = requests.get(url, headers=headers)
    req.encoding = 'utf-8'
    soup = bs(req.text, 'html.parser')
    links = soup.find_all('a')
    for link in links[1:]:
        print(link.get('href'))
main()