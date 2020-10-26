from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher

graph = Graph('http://localhost:7474/', username='neo4j', password='zzy117788')


# 查询节点
def MatchNode(m_graph, m_label, m_attrs):
    m_n = "_.name=" + "\'" + m_attrs['name'] + "\'"
    matcher = NodeMatcher(m_graph)
    re_value = matcher.match(m_label).where(m_n).first()
    return re_value


# 创建节点
def CreatNode(m_graph, m_label, m_attrs):
    p = MatchNode(m_graph, m_label, m_attrs)
    # 无返回值则创建节点
    if p is None:
        m_node = Node(m_label, **m_attrs)
        n = graph.create(m_node)
        return n
    return None


# 创建关系
def CreateRelationship(m_graph, m_label1, m_attrs1, m_label2, m_attrs2, m_relation_name):
    reValue1 = MatchNode(m_graph, m_label1, m_attrs1)
    reValue2 = MatchNode(m_graph, m_label2, m_attrs2)
    if reValue1 is None or reValue2 is None:
        return False
    m_relation = Relationship(reValue1, m_relation_name, reValue2)
    n = graph.create(m_relation)
    return n


# 程序主入口
if __name__ == '__main__':
    label1 = 'Stock'
    attrs1 = {'name': '招商银行', 'code': '600036'}
    label2 = 'SecuritiesExchange'
    attrs2 = {'name': '上海证券交易所'}
    m_relation_name1 = '证券交易所'
    m_relation_name2 = '银行'

    CreatNode(graph, label1, attrs1)
    CreatNode(graph, label2, attrs2)

    relationship1 = CreateRelationship(graph, label1, attrs1, label2, attrs2, m_relation_name1)
    relationship2 = CreateRelationship(graph, label2, attrs2, label1, attrs1, m_relation_name2)

    # 删除节点
    #id_5 = graph.evaluate("MATCH (n) where id(n) = 5 RETURN n")
    #graph.delete(id_5)

    # 删除全部
    #graph.delete_all()
