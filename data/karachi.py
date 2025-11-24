import networkx as nx

# Create a simple test graph immediately
G = nx.MultiDiGraph()

# Add Karachi area nodes
nodes = {
    1: (24.8607, 67.0011),  # Karachi coordinates
    2: (24.8707, 67.0111),
    3: (24.8507, 67.0211),
    4: (24.8407, 67.0011),
    5: (24.8307, 67.0311)
}

for node_id, (lat, lon) in nodes.items():
    G.add_node(node_id, y=lat, x=lon)

# Add roads
G.add_edge(1, 2, length=150, weight=1.5, highway='primary')
G.add_edge(2, 3, length=200, weight=2.0, highway='primary')
G.add_edge(3, 4, length=180, weight=1.8, highway='secondary')
G.add_edge(4, 1, length=120, weight=1.2, highway='secondary')
G.add_edge(3, 5, length=250, weight=2.5, highway='primary')

# Save as GraphML
nx.write_graphml(G, "karachi_test.graphml")
print(f"Created test graph: {len(G.nodes())} nodes, {len(G.edges())} edges")
print("Saved as karachi_test.graphml - Ready for routing!")