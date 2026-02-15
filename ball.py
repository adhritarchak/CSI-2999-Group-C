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

    def impulse(self, impulse: tuple[float, float, float]):
        '''Apply an impulse to the ball, changing its velocity.'''
        self.__velocity = (
            self.__velocity[X] + impulse[X],
            self.__velocity[Y] + impulse[Y],
            self.__velocity[Height] + impulse[Height]
        )
    def bounce(self, normal: tuple[float, float]):
        '''Bounce the ball off a surface with the given normal vector.'''
        # Calculate the dot product of the velocity and the normal
        dot_product = self.__velocity[X] * normal[X] + self.__velocity[Y] * normal[Y]
        # Reflect the velocity across the normal
        self.__velocity = (
            self.__velocity[X] - 2 * dot_product * normal[X],
            self.__velocity[Y] - 2 * dot_product * normal[Y],
            self.__velocity[Height]
        )
    def ground_bounce(self, bounciness = -1):
        '''Bounce the ball off the ground, applying the bounciness factor.'''
        if bounciness == -1:
            bounciness = self.bounciness
        self.__velocity = (
            self.__velocity[X],
            self.__velocity[Y] * bounciness,
            -self.__velocity[Height] * bounciness
        )
    
    def draw(self, screen):
        self.update_position()  # Update the ball's position before drawing
        pg.draw.circle(screen, self.color, (int(self.__position[X]), int(self.__position[Y] - self.__position[Height])), self.radius)

    def update_position(self):
        self.__position = (
            self.__position[X] + self.__velocity[X],
            self.__position[Y] + self.__velocity[Y],
            self.__position[Height] + self.__velocity[Height]
        )

        self.impulse((0, 0, -self.gravity))  # Apply gravity as a constant downward impulse

        if self.__position[Height] < 0:  # If the ball hits the ground
            self.__position = (self.__position[X], self.__position[Y], 0)  # Reset height to ground level
            self.ground_bounce()  # Bounce off the ground
        if self.__position[X] < 0 or self.__position[X] > 800:  # If the ball goes off the left or right edge of the screen
            self.bounce((-1, 0))  # Bounce horizontally
        if self.__position[Y] < 0 or self.__position[Y] > 600:  # If the ball goes off the top or bottom edge of the screen
            self.bounce((0, -1))  # Bounce vertically

ball_characteristics = Ball(x=30, y=300, height=100, color=(255,255,255), speed_x=1.5, speed_y=0.2, radius=8)  # Example initialization
ball_characteristics.draw(pg.display.set_mode((800, 600)))  # Example drawing on a Pygame screen
ball_initial_position = (400, 300)  # Reset ball position to center