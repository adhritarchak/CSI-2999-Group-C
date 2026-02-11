import pygame as pg
class Ball:
    def __init__(self, x, y, color, speed_x, speed_y, radius):
        self.x = x
        self.y = y
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius

    def speed(self):
        return (self.speed_x, self.speed_y)
    
    def initial_position(self):
        return (self.x, self.y)
    
    def draw(self, screen):
        pg.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


ball_characteristics = Ball(30,30, (255,255,255), 10, 10, 8)  # Example initialization
ball_characteristics.draw(pg.display.set_mode((800, 600)))  # Example drawing on a Pygame screen
ball_initial_position = (400, 300)  # Reset ball position to center