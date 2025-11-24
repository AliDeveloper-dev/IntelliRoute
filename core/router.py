import math
import heapq

class MinHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, priority, item):
        heapq.heappush(self.heap, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.heap)
    
    def empty(self):
        return len(self.heap) == 0

class Router:
    def __init__(self, graph):
        self.g = graph
    
    def dijkstra(self, source, target):
        dist = {source: 0.0}
        prev = {}
        h = MinHeap()
        h.push(0.0, source)
        while not h.empty():
            d, u = h.pop()
            if u == target:
                break
            if d > dist.get(u, math.inf):
                continue
            for v, w in self.g.neighbors(u):
                alt = d + w
                if alt < dist.get(v, math.inf):
                    dist[v] = alt
                    prev[v] = u
                    h.push(alt, v)
        return dist, prev

    def shortest_path(self, source, target):
        # reconstruct path using dijkstra up to target
        dist = {source: 0.0}
        prev = {}
        h = MinHeap()
        h.push(0.0, source)
        while not h.empty():
            d, u = h.pop()
            if u == target:
                break
            if d > dist.get(u, math.inf):
                continue
            for v, w in self.g.neighbors(u):
                alt = d + w
                if alt < dist.get(v, math.inf):
                    dist[v] = alt
                    prev[v] = u
                    h.push(alt, v)
        # reconstruct path
        if target not in prev and target != source:
            return None # unreachable
        path = [target]
        cur = target
        while cur != source:
            cur = prev[cur]
            path.append(cur)
        path.reverse()
        return path

    def a_star(self, source, target):
        # A* using haversine heuristic from Graph
        open_set = MinHeap()
        g_score = {source: 0.0}
        f_score = {source: self.g.haversine(self.g.coords[source], self.g.coords[target])}
        open_set.push(f_score[source], source)
        came_from = {}
        while not open_set.empty():
            fcur, current = open_set.pop()
            if current == target:
                # build path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path
            for neighbor, w in self.g.neighbors(current):
                tentative_g = g_score[current] + w
                if tentative_g < g_score.get(neighbor, math.inf):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    h = self.g.haversine(self.g.coords[neighbor], self.g.coords[target])
                    f_score[neighbor] = tentative_g + h
                    open_set.push(f_score[neighbor], neighbor)
        return None