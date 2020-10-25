import json
import requests

url = 'https://m.qidian.com/majax/rank/yuepiaolist?_csrfToken=vwHSDjqNkaUOCWnWhu2mvDKXM9u9ETr58fpq3V9J&gender=male&catId=21&yearmonth=201907&pageNum='


def getHtmlData(url):
    responseHtml = requests.get(url)
    hjson = json.loads(responseHtml.text)  # 读取页面的json数据,读出来相当于一个dict字典。
    a = hjson['data']['records']
    final_data = []
    for b in a:
        bid = b['bid']
        bName = b['bName']  # 书名
        bAuth = b['bAuth']  # 作者
        desc = b['desc']  # 简介
        cat = b['cat']  # 类型
        catId = b['catId']
        cnt = b['cnt']  # 字数
        rankCnt = b['rankCnt']  # 月票数
        singele_data = [bName, bAuth, cat, cnt, rankCnt, desc]
        final_data.append(singele_data)
    # 把json数据写入到excel中
    output = open('G:/My files/crawlTest.xls', 'a', encoding='utf-8')  # 打开该文件以追加的方式进行写入
    # output.write('书名\t作者\t类型\t字数\t月票数\t简介\n')
    for i in range(len(final_data)):
        for j in range(len(final_data[i])):
            output.write(str(final_data[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
            output.write('\t')  # 相当于Tab一下，换一个单元格
        output.write('\n')  # 写完一行立马换行
    final_data.clear()
    output.close()


def appdStr(start, end):
    for i in range(start, end):
        if i == 1:
            output = open('G:/My files/crawlTest.xls', 'a', encoding='utf-8')
            output.write('书名\t作者\t类型\t字数\t月票数\t简介\n')
            output.close()
            getHtmlData(url + str(1))
            # print(url + str(1))
        else:
            getHtmlData(url + str(i))
            # print(url + str(i))
            # time.sleep(2) #执行等待，防止短时间内多次访问被禁。


appdStr(1, 20)
