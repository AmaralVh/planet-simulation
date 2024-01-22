from planet import pygame
from planet import Planet

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
GREEN = [0, 255, 0]

FONT = pygame.font.SysFont("comicsans", 16)




def main():
    run = True
    # Set a clock to the frame change (fixes a velocity to it):
    clock = pygame.time.Clock()
    
    blackHole = Planet(0, 0, 4, [255, 255, 255], 1.98892 * 10**32)
    blackHole.star = True
    
    star1 = Planet(-1.5, 0, 2, [255, 255, 255], 1.98892 * 10**30)
    star1.star = True
    star1.x_vel = 16 * 1000
    
    star2 = Planet(-1.5, 0.2, 2, [255, 255, 255], 1.98892 * 10**30)
    star2.star = True
    star2.x_vel = 16 * 1000
    
    star3 = Planet(-1.5 , 0.4, 2, [255, 255, 255], 1.98892 * 10**30)
    star3.star = True
    star3.x_vel = 16 * 1000
    
    star4 = Planet(-1.5, 0.5, 2, [255, 255, 255], 1.98892 * 10**30)
    star4.star = True
    star4.x_vel = 16 * 1000
    
    star5 = Planet(-1.5, 0.6, 2, [255, 255, 255], 1.98892 * 10**30)
    star5.star = True
    star5.x_vel = 16 * 1000
    
    sun1 = Planet(-1.5, 0, 15, [255, 255, 0], 1.98892 * 10**30)
    sun1.star = True
    # sun1.x_vel = 70 * 1000
    # sun1.y_vel = 30 * 1000
    
    sun2 = Planet(0, 0, 15, [255, 100, 0], 1.98892 * 10**30)
    sun2.star = True
    # sun2.x_vel = 20 * 1000
    # sun2.y_vel = 20 * 1000
    
    sun3 = Planet(1, 0, 15, [255, 100, 0], 1.98892 * 10**30)
    sun3.y_vel = -20 * 1000
    sun3.star = True
    
    earth1 = Planet(1.7, 0, 8, [0, 0, 255], 5.9742 * 10**23)
    earth1.y_vel = -16 * 1000
    
    earth2 = Planet(1.5, 0, 8, [0, 255, 0], 5.9742 * 10**23)
    earth2.y_vel = -16 * 1000
    
    moon = Planet(1.4, -0.2, 5, [255, 255, 255], 5.9742 * 2**10)
    moon.y_vel = -16 * 1000
    
    mars1 = Planet(0.5, 0, 6, [255, 0, 0], 5.39 * 10**23)
    mars1.y_vel = -50.077 * 1000
    
    mercury1 = Planet(0.387, 0, 4, [80, 78, 81], 3.30 * 10**23)
    mercury1.y_vel = -60 * 1000
    
    mercury2 = Planet(-1.2, 0, 4, WHITE, 3.30 * 10**23)
    mercury2.y_vel = 40 * 1000
    
    mercury3 = Planet(1, 1, 4, DARK_BLUE, 3.30 * 10**23)
    mercury3.y_vel = -10 * 1000
    
    mercury4 = Planet(0, 1.5, 4, [0, 255, 0], 3.30 * 10**23)
    mercury4.x_vel = 30 * 1000
    
    venus = Planet(0.4, 0, 7, WHITE, 4.8685 * 10**28)
    venus.y_vel = 18.9 * 1000
        
    planets = [sun1, sun2, mercury1, mercury2, mercury3, mercury4, earth1, earth2]
    
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
            
            planet.draw(WIN, WIDTH, HEIGHT, FONT)
            
        for planet in planets:
            # Verify collision and then merge if True:
            for other in planets:
                if planet == other:
                    continue
                
                # print(f'comparing collision of {planet.color} with {other.color}')
                
                if planet.collision(other, WIDTH, HEIGHT):
                    # print('collision')
                    planet.merge_planets(other)
                    planets.remove(other)
                    del other
                    pass
        
        pygame.display.update()
        
    pygame.quit()
    
main()