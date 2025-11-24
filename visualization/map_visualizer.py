import folium
from folium.features import DivIcon

class MapVisualizer:
    def __init__(self, graph):
        # pick center
        any_node = next(iter(graph.coords))
        lat, lon = graph.coords[any_node]
        self.map = folium.Map(location=[lat, lon], zoom_start=14)
        self.graph = graph

    def draw_graph_nodes(self):
        for n, (lat, lon) in self.graph.coords.items():
            folium.CircleMarker(location=[lat, lon], radius=2, fill=True).add_to(self.map)

    def draw_path(self, path, popup=None):
        latlons = [self.graph.coords[n] for n in path]
        folium.PolyLine(locations=latlons, weight=4).add_to(self.map)

    def draw_vehicles(self, vehicles_state):
        # vehicles_state: list of (id, node)
        for vid, node in vehicles_state:
            lat, lon = self.graph.coords[node]
            folium.map.Marker([lat, lon], icon=DivIcon(html=f"<div style='font-size:12px'>{vid}</div>")).add_to(self.map)

    def save(self, path='map.html'):
        self.map.save(path)
