from math import pi

class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_error = 0
        self.derivative_error = 0
        self.old_e = 0

    @staticmethod
    def nozzle_angle_limit(a):
        return max(min(a, pi/36), -pi/36) #Max of 5 degree motor deflection
    
    @staticmethod
    def targeting_aggressivness(a):
        return max(min(a, pi/39), -pi/39) #Degree of freedom for targeting
    
    @staticmethod
    def trust_limit(t):
        return max(min(t, 0), -9.81*2) #Max/min trust

    def compute(self, e, setpoint, dt):
        if dt!=0:
            error = setpoint-e
            self.integral_error += error * dt
            self.derivative_error = (error-self.old_e)/dt
            self.old_e = error
            correction = self.kp*error + self.ki*self.integral_error + self.kd*self.derivative_error
            return correction
        else: return 0
    
    def update_coef(self):
        pass