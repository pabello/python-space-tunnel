import pygame
from math import sin, cos, pi as PI
import random


### Inspo and further development of this project
### https://www.youtube.com/watch?v=qr4siL4Wktc&list=PLi77irUVkDavPkh5VSR7wgYC5J-T8JhSW&index=39


BASE_STAR_SIZE = 1
TUNNEL_RADIUS = 20
STAR_COUNT = 100
WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

screen.fill((0, 0, 0))


def get_random_star_position(radius, width, height):
    """Gets a random position close to the perimeter of a circle (+-20 px x&y)."""
    random_angle = random.uniform(0, 2 * PI)
    point_x = width/2 + radius * cos(random_angle) + random.randint(-2, 2)
    point_y = height/2 + radius * sin(random_angle) + random.randint(-2, 2)
    return point_x, point_y


class Star:
    def __init__(self, x, y, size, color, width, height):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.movement_vector = (x-width/2, y-height/2)

    def distance_to_center_factor(self, width, height):
        center_x = width / 2
        center_y = height / 2
        dx = self.x - center_x
        dy = self.y - center_y
        distance = (dx ** 2 + dy ** 2)**(1/2)
        max_distance = (center_x ** 2 + center_y ** 2)**(1/2)
        return distance / max_distance

    def movement_speed_factor(self, width, height):
        distance_factor = self.distance_to_center_factor(width, height)
        speed_factor = distance_factor / 4
        return speed_factor
    
    def set_new_size(self, width, height):
        distance_factor = self.distance_to_center_factor(width, height)
        self.size = BASE_STAR_SIZE + 12 * distance_factor

    def move(self, width, height):
        speed_factor = self.movement_speed_factor(width, height)
        self.x += self.movement_vector[0] * speed_factor
        self.y += self.movement_vector[1] * speed_factor

    def is_out_of_screen(self, width, height):
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)


def get_new_star():
    return Star(*get_random_star_position(TUNNEL_RADIUS, WIDTH, HEIGHT), BASE_STAR_SIZE, (255, 255, 255), WIDTH, HEIGHT)

stars = []
for _ in range(STAR_COUNT):
    stars.append(get_new_star())

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for star in stars:
        star.move(WIDTH, HEIGHT)
        if star.is_out_of_screen(WIDTH, HEIGHT):
            stars.remove(star)
            del star
            new_star = get_new_star()
            stars.append(new_star)
        else:
            star.set_new_size(WIDTH, HEIGHT)
            star.draw(screen)
    pygame.display.update()

pygame.quit()