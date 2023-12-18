import numpy as np
import random

class Cell:

    position: np.array
    speed: np.array
    alive: bool

    color: list[int]
    radius = 10.0
    walk = 100.0

    identity: str
    targets: list[str]
    fatality = 0.5

    def __init__(self, idendity: str, targets: list[str], fatality: float, color: list[int], radius: float, x: float, y: float):
        self.color = color
        self.radius = radius
        self.position = np.array([x, y])
        self.speed = np.array([0.0, 0.0])
        self.identity = idendity
        self.targets = targets
        self.fatality = fatality
        self.alive = True

    def get_distance(self, position: np.array):
        return np.linalg.norm(self.position - position)
    
    def get_target(self, cells: list):

        min_distance = None
        nearest = None

        for i, cell in enumerate(cells):
            cell: Cell
            if (cell is self) or (cell.identity not in self.targets) or (cell.alive == False):
                continue
            if min_distance == None:
                min_distance = self.get_distance(cell.position)
                nearest = cell
            else:
                distance = self.get_distance(cell.position)
                if distance < min_distance:
                    min_distance = distance
                    nearest = cell

        return nearest
            
    def update(self, millis, cells):
        self.position += (self.speed * (millis / 1000.0))

        target = self.get_target(cells)
        if target is not None:
            distance = self.get_distance(target.position)
            if distance > (self.radius + target.radius) * 1.5:
                direction = target.position - self.position
                norm = np.linalg.norm(direction)
                if norm > 0.0:
                    direction /= norm
                    self.speed = (self.walk * direction)
            else:
                if np.linalg.norm(self.speed) > 0:
                    self.speed = np.array([0.0, 0.0])
                if random.random() < self.fatality * (millis / 1000.0):
                    target.alive = False
        else:
            self.speed[0] = self.speed[1] = 0
        







