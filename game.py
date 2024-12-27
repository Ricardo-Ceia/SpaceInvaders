import pygame
import random
import math

class Spaceship:
    def __init__(self, color):
        self.color = color  

class Missile:
    def __init__(self, color, start, end):
        self.color = color
        self.start = start
        self.end = end

class Invaders:
    def __init__(self,color,center,radius):
        self.color = color
        self.center = center
        self.radius = radius


def check_colisions(missiles,invaders):
    collisions = []

    for missile in missiles:
       for invader in invaders:
            distance = math.sqrt((missile.start[0]-invader.center[0])**2+(missile.start[1]-invader.center[1])**2)
            if distance<=invader.radius:
                collisions.append((missile,invader))
    return collisions

def game_over(invaders,font,score):
    for invader in invaders:
        if invader.center[1] + invader.radius >= 720:
            game_over_text = font.render(f'GAME OVER:{score}',True,(0,255,0))
            screen.fill('black')
            screen.blit(game_over_text,(640-80,360))
            return 

pygame.init()
pygame.font.init()

pygame.mixer.init()
laser_sound = pygame.mixer.Sound('space_laser.wav')

screen = pygame.display.set_mode((1280, 720))
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
running = True

space_ship = Spaceship((200, 100, 106))

initial_position = [[640, 680], [620, 700], [660, 700]]
missiles = []
invaders = []
score = 0

last_execution_time = 0
interval = 5000

while running:
    laser_channel = pygame.mixer.Channel(0)
    current_time = pygame.time.get_ticks()
    if current_time - last_execution_time >= interval:
        last_execution_time = current_time
        invader = Invaders((57, 255, 20), [random.randint(10, 1270), 10], 10)
        invaders.append(invader)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Create copies of the positions to avoid reference issues
            start = initial_position[0][:]
            end = [initial_position[0][0], initial_position[0][1] - 10]
            missile = Missile((255, 165, 0), start, end)
            missiles.append(missile)   
            if not laser_channel.get_busy():
                laser_channel.play(laser_sound) 

    # Clear the screen first
    screen.fill("black")

    # Update score
    collisions = check_colisions(missiles, invaders)

    for missile, invader in collisions:
        score += 1
        if missile in missiles:
            missiles.remove(missile)
        if invader in invaders:
            invaders.remove(invader)
 
    for invader in invaders:
        pygame.draw.circle(screen, invader.color, invader.center, invader.radius)
        invader.center[1] += 0.5
    # Update and draw missiles
    for missile in missiles:
        missile.start[1] -= 1
        missile.end[1] -= 1
        pygame.draw.line(screen, missile.color, missile.start, missile.end, width=1)
    
    # Draw spaceship
    pygame.draw.polygon(screen, space_ship.color, tuple(initial_position))

    # Move spaceship with keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        initial_position[0][0] -= 1
        initial_position[1][0] -= 1
        initial_position[2][0] -= 1
    if keys[pygame.K_d]:
        initial_position[0][0] += 1
        initial_position[1][0] += 1
        initial_position[2][0] += 1
    print("score:",score)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    game_over(invaders,font,score)
    pygame.display.flip()

