import pygame as pg
from Enums import *
class Ball:
    '''Class to manage the ball in the game.'''
    __position: tuple[float, float, float]  # (x, y) coordinates of the ball
    __velocity: tuple[float, float, float]  # (speed_x, speed_y) components of the ball's velocity
    color: tuple[int, int, int]  # RGB color of the ball
    radius: int  # radius of the ball
    gravity: float = 0.1  # gravity affecting the ball's vertical movement
    bounciness: float = 0.99  # how much the ball bounces back after hitting the ground (0 to 1)

    def __init__(self, x, y, height, color, speed_x, speed_y, radius):
        self.__position = (x, y, height)
        self.color = color
        self.__velocity = (speed_x, speed_y, 0)  # Vertical speed starts at 0
        self.radius = radius

    def get_velocity(self):
        return self.__velocity
    
    def get_height(self):
        return self.__position[Height]
    
    def set_gravity(self, gravity):
        self.gravity = gravity
    def set_bounciness(self, bounciness):
        self.bounciness = bounciness
    
    def draw(self, screen):
        self.update_position()  # Update the ball's position before drawing
        pg.draw.circle(screen, self.color, (int(self.__position[X]), int(self.__position[Y] - self.__position[Height])), self.radius)

    def update_position(self):
        self.__position = (
            self.__position[X] + self.__velocity[X],
            self.__position[Y] + self.__velocity[Y],
            self.__position[Height] + self.__velocity[Height]
        )

        self.__velocity = (
            self.__velocity[X],
            self.__velocity[Y],
            self.__velocity[Height] - self.gravity  # Apply gravity to vertical velocity
        )

        if self.__position[Height] < 0:  # If the ball hits the ground
            self.__position = (self.__position[X], self.__position[Y], 0)  # Reset height to ground level
            self.__velocity = (self.__velocity[X], self.__velocity[Y], -self.__velocity[Height] * self.bounciness)  # Bounce with damping from bounciness
        if self.__position[X] < 0 or self.__position[X] > 800:  # If the ball goes off the left or right edge of the screen
            self.__velocity = (-self.__velocity[X], self.__velocity[Y], self.__velocity[Height])  # Reverse horizontal velocity
        if self.__position[Y] < 0 or self.__position[Y] > 600:  # If the ball goes off the top or bottom edge of the screen
            self.__velocity = (self.__velocity[X], -self.__velocity[Y], self.__velocity[Height])  # Reverse vertical velocity

ball_characteristics = Ball(x=30, y=30, height=100, color=(255,255,255), speed_x=1, speed_y=0.1, radius=8)  # Example initialization
ball_characteristics.draw(pg.display.set_mode((800, 600)))  # Example drawing on a Pygame screen
ball_initial_position = (400, 300)  # Reset ball position to center