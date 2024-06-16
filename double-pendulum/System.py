from __future__ import annotations
from Pendulum import *

class System:
    
    p1: Pendulum
    p2: Pendulum

    def __init__(self, p1: Pendulum, p2: Pendulum):
        self.p1 = p1
        self.p2 = p2

    def get_double_pendulum_angular_acceleration(self, p1: Pendulum, p2: Pendulum):
        m1, l1, t1, w1 = p1.mass, p1.length, p1.theta, p1.omega
        m2, l2, t2, w2 = p2.mass, p2.length, p2.theta, p2.omega
        g = 9.80
        a1 = (m1 + m2)*(l1**2)
        a2 = m1*l1*l2*np.cos(t1-t2)
        b1 = m2*l1*l2*np.cos(t1-t2)
        b2 = m2*(l2**2)
        c1 = m2*l1*l2*(w2**2)*np.sin(t1-t2) + (m1+m2)*g*l1*np.sin(t1)
        c2 = -m2*l1*l2*(w1**2)*np.sin(t1-t2) + m2*g*l2*np.sin(t2)
        return (b1*c2 - b2*c1) / (a1*b2 - a2*b1), (a1*c2 - a2*c1) / (a2*b1 - a1*b2)
    
    def get_potential_energy(self):
        p1, p2 = self.p1, self.p2
        y1 = -p1.length * np.cos(p1.theta)
        y2 = -p2.length * np.cos(p2.theta) + y1
        g = 9.80
        pe1 = p1.mass * g * y1
        pe2 = p2.mass * g * y2
        return (pe1 + pe2)

    def get_kinetic_energy(self):
        p1, p2 = self.p1, self.p2
        vx1 = p1.length * p1.omega * np.sin(p1.theta)
        vy1 = p1.length * p1.omega * np.cos(p1.theta)
        vx2 = p2.length * p2.omega * np.sin(p2.theta) + vx1
        vy2 = p2.length * p2.omega * np.cos(p2.theta) + vy1
        v1 = np.hypot(vx1, vy1)
        v2 = np.hypot(vx2, vy2)
        ke1 = p1.mass * v1**2 / 2.0
        ke2 = p2.mass * v2**2 / 2.0
        return (ke1 + ke2)

    def update(self, interval: float):
        a1, a2 = self.get_double_pendulum_angular_acceleration(self.p1, self.p2)
        self.p1.update(a1, interval)
        self.p2.update(a2, interval)        

    def get_view(self):
        return System.View(self)
    
    class View:
        p1: Pendulum.View
        p2: Pendulum.View
        potential_energy: float
        kinetic_energy: float

        def __init__(self, system: System):
            self.p1 = system.p1.get_view()
            self.p2 = system.p2.get_view()
            self.potential_energy = system.get_potential_energy()
            self.kinetic_energy = system.get_kinetic_energy()