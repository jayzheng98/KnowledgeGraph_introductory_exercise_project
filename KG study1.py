from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import csv

g = Graph('http://localhost:7474', user='neo4j', password='zzy117788')

with open('G:/Programming files/python/code/KG TEST/Web crawler/triples.csv', 'r') as f:
    reader = csv.reader(f)
    for item in reader:
        if reader.line_num == 1:
            continue
        # 跳过第一行头部信息
        # print("当前行数：", reader.line_num, "当前内容：", item)
        start_node = Node("Person", name=item[0])
        end_node = Node("Person", name=item[1])
        relation = Relationship(start_node, item[3], end_node)

        g.merge(start_node, "Person", "name")
        g.merge(end_node, "Person", "name")
        g.merge(relation, "Person", "name")

        query = 'MATCH (p1:Person {name:"贾宝玉"}),(p2:Person{name:"林黛玉"}),p=shortestpath((p1)-[*..10]-(p2)) RETURN p'
        g.run(query).data  # TODO
