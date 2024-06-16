import numpy as np

class Pendulum:

    mass: float
    length: float
    theta: float
    omega: float

    def __init__(self, mass: float, length: float, theta: float, omega: float):
        self.mass = mass
        self.length = length
        self.theta = theta
        self.omega = omega

    def update(self, acceleration, interval):
        dt = interval / 1000.0
        self.omega += acceleration * dt
        self.theta += self.omega * dt

    def get_view(self):
        return Pendulum.View(self.length, self.theta)
    
    class View:
        length: float
        theta: float

        def __init__(self, length: float, theta: float):
            self.length = length
            self.theta = theta

        def to_cartesian(self):
            return self.length * np.sin(self.theta), self.length * np.cos(self.theta)
