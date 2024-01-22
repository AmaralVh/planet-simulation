import pygame
import math

class Planet:
    # Astronomical Unit (in meters by multiplying it to 1000):
    AU = 149.6e6 * 1000
    # Gravitational Constant:
    G = 6.67428e-11
    SCALE = 250 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day in the simulation
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x * self.AU
        self.y = y * self.AU
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        
        # If the object is a star:
        self.star = False
        self.distance_to_star = 0
        
        self.x_vel = 0
        self.y_vel = 0
        self.net_fx = 0
        self.net_fy = 0
        
    def __del__(self):
        pass

    def draw(self, win, width, height, font):
        x = self.x * self.SCALE + width / 2
        y = self.y * self.SCALE + height / 2
        
        if len(self.orbit) > 2 and not self.star:
            
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + width / 2
                y = y * self.SCALE + height / 2 
                updated_points.append((x, y))
        
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        if not self.star:
            distance_text = font.render(f"{round(self.distance_to_star/1000, 1)}km", 1, [255, 255, 255])
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

    def distance(self, other):
        other_x, other_y = other.x, other.y

        distance_x = other_x - self.x
        distance_y = other_y - self.y
        
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        return distance
    
    def angle_distance(self, other):
        other_x, other_y = other.x, other.y

        distance_x = other_x - self.x
        distance_y = other_y - self.y
        
        # Calculate angle theta through arctan:
        theta = math.atan2(distance_y, distance_x)
        
        return theta

    def attraction(self, other):
        distance = self.distance(other)
        
        if other.star:
            self.distance_to_star = distance
            
        force = self.G * self.mass * other.mass / distance**2
        
        theta = self.angle_distance(other)
        
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
    
    def net_force(self, planets):
        self.net_fx = self.net_fy = 0
        
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            self.net_fx += fx
            self.net_fy += fy
    
    def update_position(self):
        self.x_vel += self.net_fx / self.mass * self.TIMESTEP
        self.y_vel += self.net_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        self.orbit.append((self.x, self.y))
        
    def collision(self, other, width, height):
        x_self = self.x * self.SCALE + width / 2
        y_self = self.y * self.SCALE + height / 2
        x_other = other.x * other.SCALE + width / 2
        y_other = other.y * other.SCALE + height / 2
        
        distance = math.sqrt((x_other - x_self)**2 + (y_other - y_self)**2)
        
        # distance = self.distance(other)
        
        # print(f'Distance: {distance}, radius: {self.radius} and {other.radius}')
        
        if distance < (self.radius + other.radius):
            return True
        else:
            return False
        
    def merge_planets(self, other):
        self.radius = (self.radius + other.radius) * 0.7
        
        for i in range(0, len(self.color)):
            self.color[i] = (self.color[i] + other.color[i]) / 2
        
        print(f'y_vel_self = {self.y_vel} and y_vel_other = {other.y_vel}')
        print(f'x_vel_self = {self.x_vel} and x_vel_other = {other.x_vel}')
        
        # Momentum conservation:
        self.x_vel = (self.mass * self.x_vel + other.mass * other.x_vel) / (self.mass + other.mass)
        self.y_vel = (self.mass * self.y_vel + other.mass * other.y_vel) / (self.mass + other.mass)
        
        self.mass = self.mass + other.mass