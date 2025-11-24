from core.graph import Graph
from core.router import Router
from simulator.simulation import Simulation
from visualization.map_visualizer import MapVisualizer
import osmnx as ox
import os

# 1. load or download graphml
DATA_PATH = 'data/karachi_graph.graphml'
if not os.path.exists(DATA_PATH):
    # download small area around a coordinate in Karachi
    G = ox.graph_from_point((24.8607, 67.0011), dist=500, network_type='drive')
    ox.save_graphml(G, DATA_PATH)

# 2. convert osmnx graph to custom Graph
from networkx import Graph as NXGraph
Gnx = ox.load_graphml(DATA_PATH)

custom = Graph()
for n, data in Gnx.nodes(data=True):
    lat = float(data.get('y'))
    lon = float(data.get('x'))
    custom.add_node(int(n), lat=lat, lon=lon)

for u, v, data in Gnx.edges(keys=False, data=True):
    # length may exist
    length = data.get('length')
    u_i, v_i = int(u), int(v)
    if length is None:
        length = custom.distance(u_i, v_i)
    custom.add_edge(u_i, v_i, weight=length)

# 3. initialize router and sim
router = Router(custom)
sim = Simulation(custom, router, tick_ms=200)

# 4. spawn a couple vehicles
nodes = list(custom.coords.keys())
if len(nodes) >= 10:
    sim.spawn_vehicle('car1', nodes[0], nodes[5])
    sim.spawn_vehicle('car2', nodes[2], nodes[8])

# 5. run a few steps
sim.run(steps=10)

# 6. visualize
viz = MapVisualizer(custom)
viz.draw_graph_nodes()
for v in sim.vehicles:
    viz.draw_path(v.path)
viz.draw_vehicles(sim.get_state())
viz.save('output/map.html')
print('Saved output/map.html')
