from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import csv

g = Graph('http://localhost:7474', user='neo4j', password='zzy117788')
g.delete_all()
result = {}
# 程序主入口
if __name__ == '__main__':
    with open('G:/Programming files/python/code/KG TEST/Web crawler/triples.csv', 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            if reader.line_num == 1:
                continue
            # 跳过第一行头部信息
            start_node = Node("Person", name=item[0])
            end_node = Node("Person", name=item[1])
            relation = Relationship(start_node, item[3], end_node)

            g.merge(start_node, "Person", "name")  # g.merge(node_1,"Person","name") 根据name属性对Person结点进行merge
            g.merge(end_node, "Person", "name")
            g.merge(relation, "Person", "name")

