from flask import Flask, render_template, jsonify, request
from core.graph import Graph
from core.router import Router
import time

app = Flask(__name__)

class WebVisualizer:
    def __init__(self):
        self.G = None
        self.router = None
        self.load_graph()
    
    def load_graph(self):
        try:
            # Create graph instance using your existing Graph class
            self.G = Graph()
            
            # Add Karachi nodes with realistic positions and names
            nodes_data = [
                (1, 24.8607, 67.0011, 'Saddar Downtown'),
                (2, 24.8707, 67.0111, 'Clifton Area'), 
                (3, 24.8507, 67.0211, 'Korangi Crossing'),
                (4, 24.8407, 67.0011, 'Lyari Junction'),
                (5, 24.8307, 67.0311, 'Landhi Central'),
                (6, 24.8907, 67.0411, 'North Nazimabad'),
                (7, 24.8207, 67.0511, 'Malir City'),
                (8, 24.9007, 67.0611, 'Gulshan-e-Iqbal')
            ]
            
            for node_id, lat, lng, name in nodes_data:
                self.G.add_node(node_id, lat, lng)
                # Store name separately since your Graph class doesn't have name field
                if not hasattr(self.G, 'node_names'):
                    self.G.node_names = {}
                self.G.node_names[node_id] = name
            
            # Add roads with different weights (in meters)
            roads = [
                (1, 2, 2100),    # Shahrah-e-Faisal: 2.1 km
                (2, 3, 3200),    # Korangi Road: 3.2 km
                (3, 4, 2800),    # Mauripur Road: 2.8 km
                (4, 1, 1500),    # Lyari Expressway: 1.5 km
                (2, 6, 4100),    # University Road: 4.1 km
                (6, 8, 3300),    # North Karachi Road: 3.3 km
                (3, 5, 2700),    # Landhi Road: 2.7 km
                (5, 7, 3000),    # Malir Road: 3.0 km
                (7, 8, 4200),    # Super Highway: 4.2 km
                (1, 6, 3800)     # M.A. Jinnah Road: 3.8 km
            ]
            
            for u, v, distance in roads:
                # Convert distance to weight (using distance as weight for simplicity)
                self.G.add_edge(u, v, weight=distance, bidirectional=True)
            
            print("Created detailed test graph with 8 nodes")
            
            self.router = Router(self.G)
            print(f"Graph loaded successfully: {len(self.G.adj)} nodes, {sum(len(neighbors) for neighbors in self.G.adj.values())} edges")
            
        except Exception as e:
            print(f"Error loading graph: {e}")

viz = WebVisualizer()

# Car types with different speeds (km/h)
CAR_TYPES = {
    'motorcycle': {'speed': 60, 'color': '#FF6B35', 'icon': '🏍️'},
    'car': {'speed': 80, 'color': '#4ECDC4', 'icon': '🚗'},
    'suv': {'speed': 70, 'color': '#45B7D1', 'icon': '🚙'},
    'truck': {'speed': 50, 'color': '#FFA07A', 'icon': '🚚'},
    'emergency': {'speed': 100, 'color': '#FF0000', 'icon': '🚑'}
}

@app.route('/')
def index():
    return render_template('index.html', car_types=CAR_TYPES)

@app.route('/api/graph')
def get_graph():
    graph_data = {
        'nodes': [],
        'edges': [],
        'available_nodes': []
    }
    
    if viz.G:
        for node_id in viz.G.adj.keys():
            if node_id in viz.G.coords:
                lat, lng = viz.G.coords[node_id]
                node_name = getattr(viz.G, 'node_names', {}).get(node_id, f'Location {node_id}')
                
                node_data = {
                    'id': node_id,
                    'lat': lat,
                    'lng': lng,
                    'name': node_name
                }
                graph_data['nodes'].append(node_data)
                graph_data['available_nodes'].append({
                    'id': node_id,
                    'name': node_name
                })
        
        # Extract edges from adjacency list
        for u, neighbors in viz.G.adj.items():
            for v, weight in neighbors:
                graph_data['edges'].append({
                    'source': u,
                    'target': v,
                    'weight': weight,
                    'length': weight,  # Using weight as length for simplicity
                    'road_type': 'primary'  # Default road type
                })
    
    return jsonify(graph_data)

@app.route('/api/route', methods=['POST'])
def calculate_route():
    data = request.json
    source = data.get('source')
    target = data.get('target')
    car_type = data.get('car_type', 'car')
    
    if not viz.router:
        return jsonify({'error': 'Router not initialized'})
    
    if source not in viz.G.adj:
        return jsonify({'error': f'Start node {source} not found in graph'})
    
    if target not in viz.G.adj:
        return jsonify({'error': f'End node {target} not found in graph'})
    
    start_time = time.time()
    path = viz.router.shortest_path(source, target)
    calculation_time = time.time() - start_time
    
    if path:
        route_coords = []
        total_distance = 0
        steps = []
        
        # Calculate route details
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            
            # Find the edge weight between u and v
            edge_weight = None
            for neighbor, weight in viz.G.neighbors(u):
                if neighbor == v:
                    edge_weight = weight
                    break
            
            if edge_weight is not None:
                distance = edge_weight
                total_distance += distance
                
                u_coords = viz.G.coords.get(u, (0, 0))
                v_coords = viz.G.coords.get(v, (0, 0))
                u_name = getattr(viz.G, 'node_names', {}).get(u, f'Node {u}')
                v_name = getattr(viz.G, 'node_names', {}).get(v, f'Node {v}')
                
                steps.append({
                    'from': u,
                    'to': v,
                    'from_name': u_name,
                    'to_name': v_name,
                    'distance': distance,
                    'road_type': 'road',
                    'from_coords': {'lat': u_coords[0], 'lng': u_coords[1]},
                    'to_coords': {'lat': v_coords[0], 'lng': v_coords[1]}
                })
        
        # Calculate estimated time based on car type
        car_speed = CAR_TYPES[car_type]['speed']  # km/h
        estimated_time = (total_distance / 1000) / car_speed * 60  # minutes
        
        for node_id in path:
            if node_id in viz.G.coords:
                lat, lng = viz.G.coords[node_id]
                node_name = getattr(viz.G, 'node_names', {}).get(node_id, f'Node {node_id}')
                route_coords.append({
                    'lat': lat,
                    'lng': lng,
                    'name': node_name
                })
            
        return jsonify({
            'path': route_coords,
            'nodes': path,
            'steps': steps,
            'summary': {
                'total_distance': total_distance,
                'total_time': estimated_time,
                'car_type': car_type,
                'car_speed': car_speed,
                'calculation_time': calculation_time,
                'num_steps': len(steps),
                'start_name': getattr(viz.G, 'node_names', {}).get(source, f'Node {source}'),
                'end_name': getattr(viz.G, 'node_names', {}).get(target, f'Node {target}')
            }
        })
    
    return jsonify({'error': 'Route not found'})

@app.route('/api/car-types')
def get_car_types():
    return jsonify(CAR_TYPES)

@app.route('/api/available-nodes')
def get_available_nodes():
    nodes = []
    if viz.G:
        for node_id in viz.G.adj.keys():
            if node_id in viz.G.coords:
                lat, lng = viz.G.coords[node_id]
                node_name = getattr(viz.G, 'node_names', {}).get(node_id, f'Location {node_id}')
                nodes.append({
                    'id': node_id,
                    'name': node_name,
                    'lat': lat,
                    'lng': lng
                })
    return jsonify(nodes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)