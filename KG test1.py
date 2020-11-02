from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import requests
from lxml import etree
import time
import PySimpleGUI as sg

# 创建图
g = Graph('http://localhost:7474/', username='neo4j', password='zzy117788')

# 初始化列表，存入爬虫数据
all_info_list = []
# 创建全局变量存放“类型”
style = ''
author = ''
book = ''

# 创建GUI界面获取用户需求
def RequestGUI():
    global style, author, book
    sg.theme('DarkAmber')
    layout1 = [
        [sg.Text('Please choose the info you want:')],
        [sg.Text(" ")],
        [sg.Button('Style', size=(24, 2))],
        [sg.Button('Author', size=(24, 2))],
        [sg.Button("Book's info", size=(24, 2))],
        [sg.Text(" ")],
    ]
    layout2 = [
        [sg.Text("Please write the style you want: (eg.历史)")],
        [sg.Input(size=(15, 1))],
        [sg.Text(" ")],
        [sg.Submit(), sg.Text(" "), sg.Exit()],
    ]
    layout3 = [
        [sg.Text("Please write a author's name: (eg.J神)")],
        [sg.Input(size=(15, 1))],
        [sg.Text(" ")],
        [sg.Submit(), sg.Text(" "), sg.Exit()],
    ]
    layout4 = [
        [sg.Text("Please write the book you want: (eg.万族之劫)")],
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
        window3 = sg.Window("Qidian information system", layout3)
        event3, values3 = window3.read()
        if event3 == 'Submit':
            if values3[0] == '':
                window3.close()
                print("You have to input a name!")
                return -1
            else:
                author = values3[0]
                window3.close()
                return 2
        elif event3 == 'Exit':
            window3.close()
            return -1
    elif event1 == "Book's info":
        window1.close()
        window4 = sg.Window("Qidian information system", layout4)
        event4, values4 = window4.read()
        if event4 == 'Submit':
            if values4[0] == '':
                window4.close()
                print("You have to input a name!")
                return -1
            else:
                book = values4[0]
                window4.close()
                return 3
        elif event4 == 'Exit':
            window4.close()
            return -1


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
        ranking = info.xpath('div[1]/span/text()')[0]
        last_update = info.xpath('div[2]/p[3]/span/text()')[0]
        info_list = [title, author, style, complete, ranking, last_update]
        # 把数据存入列表
        all_info_list.append(info_list)
        # 睡眠0.05秒
        time.sleep(0.05)


# 程序主入口
if __name__ == '__main__':

    # 人脸识别 TODO

    label_match_node = 0
    choice = -1
    while choice == -1:
        choice = RequestGUI()
    # 将得到的用户输入存入cypher语句
    cypher_text_style = 'MATCH(p: Style{name:"' + style + '"}) return p'
    cypher_text_book = 'MATCH(p: Style{name:"' + style + '"})-[k: 风格]-(r)-[q: 作者]-(a)  return p, k, r, q, a'
    cypher_text_author = 'MATCH(p: Author{name:"' + author + '"})-[q: 作者]-(r)  return p, q, r'
    cypher_text_info = 'MATCH(p: Book{name:"' + book + '"})-[q: 作者]-(a) return p, a'

    if choice != -1 and choice is not None:
        # #获取网页数据
        # urls = ['https://www.qidian.com/rank/fengyun?style=1&page={}'.format(str(i)) for i in range(1, 6)]
        # for url in urls:
        #     get_info(url)
        #
        # # 创建neo4j图形数据库
        # g.delete_all()
        # for item in all_info_list:
        #     book_attrs = {'name': item[0], 'rank': item[4], 'complete': item[3], 'last_update': item[5]}
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

        # 查找分类对应的书目
        if choice == 1:
            stys_in_graph = list(g.run(cypher_text_style))
            for sty in stys_in_graph:
                if sty['p']['name'] == style:
                    print("进入风云排行榜%s类的书目：" % (sty['p']['name']))
                    label_match_node = 1
                    break
            if label_match_node == 0:
                print("排行榜中未找到对应的小说类别！")
            elif label_match_node == 1:
                # 找到分类后输出类别里的小说及作者信息
                label_match_node = 0
                books_in_sty = list(g.run(cypher_text_book))
                for book in books_in_sty:
                    print('目前排行:', book['r']['rank'], '   书名:', book['r']['name'], '  (作者:', book['a']['name'], ")")

        # 查找作者的作品
        elif choice == 2:
            auths_in_graph = list(g.run(cypher_text_author))
            for auth in auths_in_graph:
                if auth['p']['name'] == author:
                    label_match_node = 1
                    print(author, '的上榜作品有:', auth['r']['name'], '\n目前排行:', auth['r']['rank'])
                    break
            if label_match_node == 0:
                print("排行榜中未找到作者：%s！" % author)
            label_match_node = 0

        # 查询对应作品的信息
        elif choice == 3:
            bks_in_graph = list(g.run(cypher_text_info))
            for bk in bks_in_graph:
                if bk['p']['name'] == book:
                    label_match_node = 1
                    print(book, '的作者是', bk['a']['name'], '\n目前处于:', bk['p']['complete'], '\n排行第', bk['p']['rank'], '\n最后更新时间为', bk['p']['last_update'])
                    break
            if label_match_node == 0:
                print("排行榜中未找到书目：%s！" % book)
            label_match_node = 0

