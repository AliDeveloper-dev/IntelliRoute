import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.vehicle import Vehicle
import time


class Simulation:
    def __init__(self, graph, router, tick_ms=200):
        self.graph = graph
        self.router = router
        self.vehicles = []
        self.tick = tick_ms / 1000.0
        self.log = []

    def spawn_vehicle(self, vehicle_id, source, target, use_astar=True):
        if use_astar:
            path = self.router.a_star(source, target)
        else:
            path = self.router.shortest_path(source, target)
        if not path:
            raise ValueError('No path found')
        v = Vehicle(vehicle_id, path)
        self.vehicles.append(v)
        return v

    def step(self):
        # advance all vehicles by one node
        for v in list(self.vehicles):
            prev = v.current_node()
            moved = v.move_next()
            cur = v.current_node()
            self.log.append((v.id, prev, cur))
            if v.is_finished():
                # optionally remove finished vehicles
                pass

    def run(self, steps=100):
        for i in range(steps):
            self.step()
            time.sleep(self.tick)

    def get_state(self):
        # return list of (vehicle_id, current_node)
        return [(v.id, v.current_node()) for v in self.vehicles]


