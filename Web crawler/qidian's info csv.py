import csv
import requests
from lxml import etree
import time


# 初始化列表，存入爬虫数据
all_info_list = []


# 定义获取爬虫信息的函数
def get_info(url):

    html = requests.get(url)
    selector = etree.HTML(html.text)

    # 定位大标签，以此循环
    infos = selector.xpath('//div[@class="book-img-text"]/ul/li')

    for info in infos:
        title = info.xpath('div[2]/h4/a/text()')[0]
        author = info.xpath('div[2]/p[1]/a[1]/text()')[0]
        style = info.xpath('div[2]/p[1]/a[2]/text()')[0]
        complete = info.xpath('div[2]/p[1]/span/text()')[0]
        introduce = info.xpath('div[2]/p[2]/text()')[0].strip()
        last_update = info.xpath('div[2]/p[3]/span/text()')[0]
        info_list = [title, author, style, complete, introduce, last_update]
        # 把数据存入列表
        all_info_list.append(info_list)
        # 睡眠1秒
        time.sleep(0.1)


# 程序主入口
if __name__ == '__main__':

    urls = ['https://www.qidian.com/rank/fengyun?style=1&page={}'.format(str(i)) for i in range(1, 6)]
    # 获取所有数据
    for url in urls:
        get_info(url)

    # 定义表头
    header = ['title', 'author', 'style', 'complete', 'introduce', 'last_update']
    # 创建工作簿
    csvfile = open('xiaoshuo.csv', 'w', errors='ignore', newline='')
    sheet = csv.writer(csvfile)
    # 写入表头
    sheet.writerow(header)

    # 写入爬虫数据
    for list in all_info_list:
        sheet.writerow(list)

    # 保存文件
    csvfile.close()
