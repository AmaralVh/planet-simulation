import pygame
import math

pygame.init()

# Set the dimensions of the window:
WIDTH, HEIGHT  = 1500, 800
# Create a window:
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Subtitle for the window:
pygame.display.set_caption("Planet Simulation")

WHITE = [255, 255, 255]
YELLOW = [255, 255, 0]
BLUE = [100, 149, 237]
RED = [188, 39, 50]
DARK_GREY = [80, 78, 81]
DARK_BLUE = [0, 0, 255]

FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    # Astronomical Unit (in meters by multiplying it to 1000):
    AU = 149.6e6 * 1000
    # Gravitational Constant:
    G = 6.67428e-11
    SCALE = 250 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24 # 1 day in the simulation
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
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

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2 and not self.star:
            
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2 
                updated_points.append((x, y))
        
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        if not self.star:
            distance_text = FONT.render(f"{round(self.distance_to_star/1000, 1)}km", 1, WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

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
        
    def collision(self, other):
        x_self = self.x * self.SCALE + WIDTH / 2
        y_self = self.y * self.SCALE + HEIGHT / 2
        x_other = other.x * other.SCALE + WIDTH / 2
        y_other = other.y * other.SCALE + HEIGHT / 2
        
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

def main():
    run = True
    # Set a clock to the frame change (fixes a velocity to it):
    clock = pygame.time.Clock()
    
    sun1 = Planet(-1.5 * Planet.AU, 0 * Planet.AU, 15, YELLOW, 1.98892 * 10**30)
    sun1.star = True
    # sun1.x_vel = 70 * 1000
    # sun1.y_vel = 30 * 1000
    
    sun2 = Planet(0 * Planet.AU, 0 * Planet.AU, 15, RED, 1.98892 * 10**30)
    sun2.star = True
    # sun2.x_vel = 20 * 1000
    # sun2.y_vel = 10 * 1000
    
    earth = Planet(-1.7 * Planet.AU, 0 * Planet.AU, 8, BLUE, 5.9742 * 10**23)
    earth.y_vel = -16 * 1000
    
    mars1 = Planet(0.5 * Planet.AU, 0, 6, RED, 5.39 * 10**23)
    mars1.y_vel = -50.077 * 1000
    
    mercury1 = Planet(0.387 * Planet.AU, 0, 4, DARK_GREY, 3.30 * 10**23)
    mercury1.y_vel = -60 * 1000
    
    mercury2 = Planet(-0.2 * Planet.AU, 0, 4, DARK_GREY, 3.30 * 10**23)
    mercury2.y_vel = 40 * 1000
    
    mercury3 = Planet(0.5 * Planet.AU, 2 * Planet.AU, 4, DARK_GREY, 3.30 * 10**23)
    mercury3.y_vel = -30 * 1000
    
    venus = Planet(0.4 * Planet.AU, 0 * Planet.AU, 7, WHITE, 4.8685 * 10**28)
    venus.y_vel = 18.9 * 1000
        
    planets = [sun1, sun2, mercury1]
    
    # Loop of open window:
    while run:
        # Maximum frames per second:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        
        # Gets the events in the window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.net_force(planets)
        
        for planet in planets:
            planet.update_position()
            
            planet.draw(WIN)
            
        for planet in planets:
            # Verify collision and then merge if True:
            for other in planets:
                if planet == other:
                    continue
                
                # print(f'comparing collision of {planet.color} with {other.color}')
                
                if planet.collision(other):
                    # print('collision')
                    planet.merge_planets(other)
                    planets.remove(other)
                    del other
                    pass
        
        pygame.display.update()
        
    pygame.quit()
    
main()