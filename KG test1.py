from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import requests
from lxml import etree
import time
import PySimpleGUI as sg

# 创建图
g = Graph('http://localhost:7474/', username='neo4j', password='zzy117788')

# 初始化列表，存入爬虫数据
all_info_list = []
# 创建一个全局变量存放“类型”
style = ''


# 创建GUI界面获取用户需求
def RequestGUI():
    global style
    sg.theme('DarkAmber')
    layout1 = [
        [sg.Text('Please choose the info you want:')],
        [sg.Text(" ")],
        [sg.Button('Style', size=(24, 1))],
        [sg.Button('Author', size=(24, 1))],
        [sg.Button("Book's info", size=(24, 1))],
        [sg.Text(" ")],
    ]
    layout2 = [
        [sg.Text("Please write the style you want:")],
        [sg.Input(size=(15, 1))],
        [sg.Text(" ")],
        [sg.Submit(), sg.Text(" "), sg.Exit()],
    ]
    window1 = sg.Window("Qidian information system", layout1)
    event1, values1 = window1.read()

    if event1 == 'Style':
        window1.close()
        window2 = sg.Window("Qidian information system", layout2)
        event2, values2 = window2.read()
        if event2 == 'Submit':
            if values2[0] == '':
                window2.close()
                print("You have to input a style!")
                return -1
            else:
                style = values2[0]
                window2.close()
                return 1
        elif event2 == 'Exit':
            window2.close()
            return -1
    elif event1 == 'Author':
        window1.close()
        return 2
    elif event1 == "Book's info":
        window1.close()
        return 3


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
        # 睡眠0.05秒
        time.sleep(0.05)


# 程序主入口
if __name__ == '__main__':

    # 人脸识别 TODO

    label_match_node = 0
    label_create_graph = 0
    choice = -1
    while choice == -1:
        choice = RequestGUI()

    if choice != -1 and choice is not None:
        # 获取网页数据
        # urls = ['https://www.qidian.com/rank/fengyun?style=1&page={}'.format(str(i)) for i in range(1, 6)]
        # for url in urls:
        #     get_info(url)
        #
        # # 创建neo4j图形数据库
        # g.delete_all()
        # for item in all_info_list:
        #     book_attrs = {'name': item[0], 'complete': item[3], 'last_update': item[5]}  # , 'introduce': item[4]}
        #     style_node = Node("Style", name=item[2])
        #     # g.create(style_node)
        #     book_node = Node("Book", **book_attrs)
        #     g.create(book_node)
        #     author_node = Node("Author", name=item[1])
        #     g.create(book_node)
        #     relation1 = Relationship(style_node, '风格', book_node)
        #     # g.create(relation1)
        #     relation2 = Relationship(author_node, '作者', book_node)
        #     g.create(relation2)
        #
        #     g.merge(style_node, "Style", "name")
        #     # g.merge(book_node, "Book", "name")
        #     # g.merge(author_node, "Author", "name")
        #     g.merge(relation1, "Style", "name")
        #     # g.merge(relation2, "Author", "name")

        if choice == 1:
            sty_in_graph = list(g.run('MATCH (s:Style) RETURN s'))
            # 在已有的类别中进行匹配
            for i in range(0, 11):
                if sty_in_graph[i]['s']['name'] == style:
                    print("进入风云排行榜%s类的小说：" % (sty_in_graph[i]['s']['name']))
                    label_match_node = 1
                    break
            if label_match_node == 0:
                print("未找到对应的小说类别！")
            elif label_match_node == 1:
                # 找到分类后输出类别里的小说及作者信息
                if style == '历史':
                    books_in_sty = list(
                        g.run('MATCH(p: Style{name: "历史"})-[k: 风格]-(r) - [q: 作者]-(a)  return p, k, r, q, a'))
                    for book in books_in_sty:
                        print('书名:', book['r']['name'], '  (作者:', book['a']['name'], ")")
