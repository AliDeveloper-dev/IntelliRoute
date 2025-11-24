class Vehicle:
    def __init__(self, vehicle_id, path):
        self.id = vehicle_id
        self.path = path # list of node ids
        self.idx = 0 # current index in path


    def current_node(self):
        return self.path[self.idx]


    def move_next(self):
        if self.idx < len(self.path) - 1:
            self.idx += 1
            return True
            return False


    def is_finished(self):
        return self.idx >= len(self.path) - 1