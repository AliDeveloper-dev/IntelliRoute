from core.graph import Graph
from core.router import Router

def test_tiny_graph():
    g = Graph()
    g.add_node(1, 0, 0)
    g.add_node(2, 0, 0.001)
    g.add_node(3, 0.002, 0.001)
    g.add_edge(1,2,weight=100)
    g.add_edge(2,3,weight=100)
    r = Router(g)
    p = r.shortest_path(1,3)
    assert p == [1,2,3]