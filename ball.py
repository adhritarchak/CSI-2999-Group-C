import pygame as pg
from Enums import *
class Ball:
    '''Class to manage the ball in the game.'''
    __position: tuple[float, float, float]  # (x, y) coordinates of the ball
    __velocity: tuple[float, float, float]  # (speed_x, speed_y) components of the ball's velocity
    __bounds: tuple[float, float, float, float]  # (top, bottom, left, right) of the area the ball can move in
    color: tuple[int, int, int] = (255, 255, 255)  # RGB color of the ball
    radius: int  # radius of the ball
    gravity: float = 0.1  # gravity affecting the ball's vertical movement
    bounciness: float = 0.99  # how much the ball bounces back after hitting the ground (0 to 1)
    draw_prediction: bool = False  # whether to draw a prediction of the ball's trajectory
    ellipse_scale: tuple[float, float] = (1.8, 1.2)  # scale of the ellipse drawn at the predicted landing position (x scale, y scale)

    def __init__(self, x, y, height, speed_x, speed_y, radius, spin):
        self.__position = (x, y, height)
        self.__velocity = (speed_x, speed_y, 0)  # Vertical speed starts at 0
        self.__bounds = (0, 600, 0, 800)  # Default bounds for the ball to move in (top, bottom, left, right)
        self.radius = radius
        self.spin = spin

    def get_velocity(self):
        return self.__velocity
    
    def get_height(self):
        return self.__position[HEIGHT]
    
    def set_bounds(self, top, bottom, left, right):
        self.__bounds = (top, bottom, left, right)
    def set_gravity(self, gravity):
        self.gravity = gravity
    def set_bounciness(self, bounciness):
        self.bounciness = bounciness
    def do_draw_prediction(self, value: bool):
        '''Draw a prediction of the ball's trajectory on the screen.'''
        # This function can be implemented to show a trajectory prediction for the ball, which could be useful for certain card effects.
        self.draw_prediction = value

    def impulse(self, impulse: tuple[float, float, float]):
        '''Apply an impulse to the ball, changing its velocity.'''
        self.__velocity = (
            self.__velocity[X] + impulse[X],
            self.__velocity[Y] + impulse[Y],
            self.__velocity[HEIGHT] + impulse[HEIGHT]
        )
    def bounce(self, normal: tuple[float, float]):
        '''Bounce the ball off a surface with the given normal vector.'''
        # Calculate the dot product of the velocity and the normal
        dot_product = self.__velocity[X] * normal[X] + self.__velocity[Y] * normal[Y]
        # Reflect the velocity across the normal
        self.__velocity = (
            self.__velocity[X] - 2 * dot_product * normal[X],
            self.__velocity[Y] - 2 * dot_product * normal[Y],
            self.__velocity[HEIGHT]
        )
    
    def draw(self, screen):
        self.update_position()  # Update the ball's position before drawing
        pg.draw.circle(surface=screen, color=(60, 60, 60), center=(int(self.__position[X]), int(self.__position[Y] + self.radius)), radius=max(1, self.radius - (self.__position[HEIGHT] // 20)))  # Shadow
        pg.draw.circle(surface=screen, color=self.color, center=(int(self.__position[X]), int(self.__position[Y] - self.__position[HEIGHT])), radius=self.radius)
        self.draw_trajectory(screen, self.draw_prediction)

        if(self.draw_prediction):
            # Implement drawing the trajectory prediction here
            self.draw_ground_trajectory(screen)

    def step_physics(self, pos: tuple[float, float, float], vel: tuple[float, float, float]) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        '''Calculate the next position and velocity of the ball based on its current state and physics.'''
        nextPos = (
            pos[X] + vel[X],
            pos[Y] + vel[Y],
            pos[HEIGHT] + vel[HEIGHT]
        )
        nextVel = (
            vel[X] + self.spin,  
            vel[Y],
            vel[HEIGHT] - self.gravity
        )
        self.spin *= 0.98  # Dampen spin over time

        if nextPos[HEIGHT] < 0:  # If the ball hits the ground
            nextPos = (nextPos[X], nextPos[Y], 0)  # Reset height to ground level
            nextVel = (
                nextVel[X],
                nextVel[Y],
                -nextVel[HEIGHT] * self.bounciness
            )  # Bounce off the ground
        if nextPos[X] < self.__bounds[LEFT] + self.radius or nextPos[X] > self.__bounds[RIGHT] - self.radius:  # If the ball goes off the left or right bounds
            nextVel = (-nextVel[X], nextVel[Y], nextVel[HEIGHT])  # Bounce horizontally
        if nextPos[Y] < self.__bounds[TOP] + self.radius or nextPos[Y] > self.__bounds[BOTTOM] - self.radius:  # If the ball goes off the top or bottom bounds
            nextVel = (nextVel[X], -nextVel[Y], nextVel[HEIGHT])  # Bounce vertically
        return nextPos, nextVel

    def draw_trajectory(self, screen, draw_lines = False):
        '''Draw a prediction of the ball's trajectory on the screen.'''
        # Create a list to store predicted positions
        predicted_positions: list[tuple] = []
        current_pos = self.__position
        current_vel = self.__velocity

        # Predict positions for the next 2 bounces
        bounces = 0
        for _ in range(1000):  # Predict until the ball bounces twice or 1000 steps have been calculated
            current_pos, current_vel = self.step_physics(current_pos, current_vel)
            predicted_positions.append(current_pos)
            if current_pos[HEIGHT] <= 0:  # Stop prediction if ball bounces twice
                bounces += 1
                if bounces >= 2:
                    break

        # Draw the trajectory as a series of lines
        if draw_lines:
            for i in range(len(predicted_positions) - 1):
                pg.draw.line(screen, (255, 255, 255), (int(predicted_positions[i][X]), int(predicted_positions[i][Y] - predicted_positions[i][HEIGHT])),
                          (int(predicted_positions[i+1][X]), int(predicted_positions[i+1][Y] - predicted_positions[i+1][HEIGHT])), 2)
            
        pg.draw.ellipse(surface=screen, color=(255, 255, 255), width=2, rect=pg.Rect(predicted_positions[-1][X] - self.ellipse_scale[X] * self.radius, 
                predicted_positions[-1][Y] - self.ellipse_scale[Y] * self.radius, self.ellipse_scale[X] * 2 * self.radius, 
                self.ellipse_scale[Y] * 2 * self.radius))  # Draw an ellipse at the final predicted position
    def draw_ground_trajectory(self, screen):
        '''Draw a prediction of where the ball will hit the ground on the screen.'''
        # Create a list to store predicted positions
        predicted_positions: list[tuple] = []
        current_pos = self.__position
        current_vel = self.__velocity

        # Predict positions for the next 2 bounces
        bounces = 0
        for _ in range(1000):  # Predict until the ball hits the ground twice or 1000 steps have been calculated
            current_pos, current_vel = self.step_physics(current_pos, current_vel)
            predicted_positions.append(current_pos)
            if current_pos[HEIGHT] <= 0:  # Stop prediction if ball bounces twice
                bounces += 1
                if bounces >= 2:
                    break

        # Draw the trajectory as a series of lines
        for i in range(len(predicted_positions) - 1):
            pg.draw.line(screen, (100, 100, 100), (int(predicted_positions[i][X]), int(predicted_positions[i][Y])),
                          (int(predicted_positions[i+1][X]), int(predicted_positions[i+1][Y])), 2)
        
    def update_position(self):
        self.__position, self.__velocity = self.step_physics(self.__position, self.__velocity)

#ball_characteristics = Ball(x=30, y=300, height=100, speed_x=1.5, speed_y=0.2, radius=8, spin=0.1)  # Example initialization
#ball_characteristics.draw(pg.display.set_mode((800, 600)))  # Example drawing on a Pygame screen
ball_initial_position = (400, 300)  # Reset ball position to center