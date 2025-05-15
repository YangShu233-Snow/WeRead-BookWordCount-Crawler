import lxml.etree
import requests
import lxml
import time
import random

base_url = "https://book.douban.com/top250?start="
index = 0
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    'Cookie': "bid=mjyaoIylXv4; __utma=30149280.198888673.1747224760.1747224760.1747224760.1; __utmc=30149280; __utmz=30149280.1747224760.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_douban=1; __utma=81379588.456664132.1747224760.1747224760.1747224760.1; __utmc=81379588; __utmz=81379588.1747224760.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1747224761%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_id.100001.3ac3=c70a46fc0a537fba.1747224761.; _pk_ses.100001.3ac3=1; __utmb=30149280.7.10.1747224760; __utmb=81379588.7.10.1747224760"
}
pattern = r'//div[@class="pl2"]/a/text()'

while(index < 10):
    start = str(index * 25)
    url = base_url + start
    print(url)
    html = requests.get(url=url, headers=headers)
    html_node = lxml.etree.HTML(html.content.decode("utf-8"))
    results = html_node.xpath(pattern)
    with open('./input/books.txt', 'a', encoding="utf-8") as f:
        for book in results:
            book: str = book.replace(" ", '').replace("\n", '')
            book = book + '\n'
            f.write(book)
    index += 1
    time.sleep(random.uniform(1,1.2))