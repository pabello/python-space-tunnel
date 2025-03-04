import pygame
import random

from math import sin, cos, tan, pi as PI
from color_gradient import linear_gradient


### Inspo and further development of this project
### https://www.youtube.com/watch?v=qr4siL4Wktc&list=PLi77irUVkDavPkh5VSR7wgYC5J-T8JhSW&index=39


BASE_STAR_SIZE = 1
MAX_STAR_SIZE = 13
TUNNEL_RADIUS = 20
STAR_COUNT = 400
WIDTH, HEIGHT = 800, 600
FPS = 60


start_color = "#FFFBC4FF"
end_color = "#3A78FFFF"
GRADIENT = linear_gradient(start_color, end_color, n=MAX_STAR_SIZE+5)[::-1]

# STAR_COLORS = [
#     "#ECF9F4",
#     "#E4F6E5",
#     "#D1E8F0",
#     "#D5D5F1",
#     "#ECD1F0",
#     "#D0BAE8",
#     "#ABB0E3",
#     "#E6E0B3",
#     "#D6CB85",
#     "#C7AB57",
#     "#6669CC",
#     "#6247C2",
# ]

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
    TOP_PROXIMITY = 0
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.size = BASE_STAR_SIZE
        self.initial_size = self.size
        self.color = random.choice(GRADIENT)
        self.movement_vector = (x-width/2, y-height/2)
        self.internal_speed_factor = random.uniform(0, 0.3)

    def distance_to_center_factor(self, width, height):
        center_x = width / 2
        center_y = height / 2
        dx = self.x - center_x
        dy = self.y - center_y
        distance = (dx ** 2 + dy ** 2)**(1/2)
        max_distance = (center_x ** 2 + center_y ** 2)**(1/2)
        return distance / max_distance

    def proximity_speed_factor(self, width, height):
        distance_factor = self.distance_to_center_factor(width, height)
        # speed_factor = tan(distance_factor)
        proximity_factor = distance_factor + self.internal_speed_factor
        if proximity_factor > Star.TOP_PROXIMITY:
            print(proximity_factor)
            Star.TOP_PROXIMITY = proximity_factor
        speed_factor = tan(proximity_factor)
        return speed_factor
    
    def update_size_and_color(self, width, height):
        distance_factor = self.distance_to_center_factor(width, height)
        self.size = self.initial_size + (MAX_STAR_SIZE-1) * distance_factor

    def move(self, width, height):
        proximity_speed_factor = self.proximity_speed_factor(width, height)
        if proximity_speed_factor < 0:
            raise Exception()
        self.x += self.movement_vector[0] * proximity_speed_factor
        self.y += self.movement_vector[1] * proximity_speed_factor

    def is_out_of_screen(self, width, height):
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, width=0)

def get_new_star():
    return Star(*get_random_star_position(TUNNEL_RADIUS, WIDTH, HEIGHT), WIDTH, HEIGHT)

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
            star.update_size_and_color(WIDTH, HEIGHT)
            star.draw(screen)
    pygame.display.update()

pygame.quit()
