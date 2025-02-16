from Render import *
from math import pi
from PID import *

class Rocket:
    def __init__(self, mass, mI, pos, cg=VectorZero(), vel=VectorZero(),
                 acc=VectorZero(), alpha=0, angle=0, omega=0):
        self.mass = mass
        self.mI = mI
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.theta = angle
        self.omega = omega
        self.alpha = alpha
        self.cg = -cg.rotate(angle)

        self.width = 10
        self.height = 86
        self.shape = Rectangle(self.pos, self.width, self.height, color="black")

        self.target = vec2(400, 255)
        self.angle_pid_controller = PID(kp=2*.6, ki=1.2*2/2.72, kd=.075*2*2.72) #PID
        self.target_pid_controller = PID(kp=1, ki=0, kd=0.85) #PID
        self.trust_pid_controller = PID(kp=1, ki=0, kd=1) #PD
        self.trustDir = vec2(sin(self.theta), cos(self.theta))
        self.trustOrigin = self.pos + (self.height/2)*vec2(sin(self.theta), cos(self.theta))
    
    def applyForce(self, force, forceApplPoint):
        lever = (self.pos+self.cg) - forceApplPoint
        self.applyForceOnCG(force)
        self.applyTorque((lever.x*force.y - lever.y*force.x)/100)
    
    def applyTorque(self, torque):
        self.alpha += torque/self.mI

    def applyForceOnCG(self, force):
        self.acc += force/self.mass

    def setTarget(self, target) -> 'vec2':
        self.target = target
    
    def rotate(self, dt):
        dTheta = self.omega*dt
        self.pos += self.cg - self.cg.rotate(dTheta)
        self.theta += dTheta
    
    def update(self, dt):
        self.vel += self.acc*dt
        self.pos += self.vel*dt*100

        self.omega += self.alpha*dt
        self.rotate(dt)

        self.acc = vec2(0, 9.81)
        self.alpha = 0
        self.autocontrol(dt)

    def autocontrol(self, dt):
        a = PID.nozzle_angle_limit(self.angle_pid_controller.compute(-self.theta, 0, dt))
        b = PID.targeting_aggressivness(self.target_pid_controller.compute(self.pos.x, self.target.x, dt))
        self.trustOrigin = self.pos + (self.height/2)*vec2(sin(self.theta), cos(self.theta))
        self.trustDir = vec2(sin(self.theta + a + b), cos(self.theta + a + b))

        trust = PID.trust_limit(self.trust_pid_controller.compute(self.pos.y, self.target.y, dt))

        self.applyForce(trust*self.mass*self.trustDir, self.trustOrigin)

    def draw(self, pg, screen):
        self.shape.pos = self.pos
        self.shape.set_rotRad(self.theta)
        self.shape.draw(pg, screen)
        pg.draw.line(screen, "orange", self.trustOrigin.get(), (self.trustOrigin + 20*self.trustDir).get(), 3)
        pg.draw.circle(screen, "red", self.trustOrigin.get(), 3)
        pg.draw.circle(screen, "green", (self.pos + self.cg).get(), 3)