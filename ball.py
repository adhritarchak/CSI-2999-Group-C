import pygame as pg
from Enums import *
from math import *
from colorsys import hsv_to_rgb

class TrailQueue:
    trailPositions: list[tuple[float, float, float]]
    trailHead: int
    trailSize: int

    def __init__(self, length: int = 100):
        self.trailPositions = []
        self.trailHead = 0
        self.trailSize = length

    def length(self) -> int:
        return len(self.trailPositions)

    def push(self, value: tuple[float, float, float]):
        if len(self.trailPositions) < self.trailSize:
            self.trailPositions.append(value)
            return
        if self.trailHead == self.trailSize - 1:
            self.trailHead = 0
            self.trailPositions[-1] = value
        else:
            self.trailPositions[self.trailHead] = value
            self.trailHead += 1

    def clear(self):
        self.trailPositions = []
        self.trailHead = 0

    def iter(self) -> list[tuple[float, float, float]]:
        out = self.trailPositions[self.trailHead:]
        if self.trailHead != 0:
            out += self.trailPositions[:self.trailHead]
        return out
    def positionList(self) -> list[tuple[float, float]]:
        out = []
        for pos in self.iter():
            out.append((pos[X], pos[Y] - pos[HEIGHT]))
        return out
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
    trailPositions: TrailQueue
    trailThickness: int = 8
    max_velocity: float = 15

    def __init__(self, x, y, height, speed_x, speed_y, radius, max_velocity, spin = 0):
        self.__position = (x, y, height)
        self.__velocity = (speed_x, speed_y, 0)  # Vertical speed starts at 0
        self.__bounds = (0, 600, 0, 800)  # Default bounds for the ball to move in (top, bottom, left, right)
        self.radius = radius
        self.max_velocity = max_velocity
        
        self.trailPositions = TrailQueue(length=50)
        self.spin = spin

    def velocity(self) -> tuple[float, float]:
        return (self.__velocity[X], self.__velocity[Y])
    def velocityMagnitude(self):
        return dist((0,0), self.velocity())
    def height(self):
        return self.__position[HEIGHT]
    def heightVelo(self) -> float:
        return self.__velocity[HEIGHT]
    
    def is_falling(self):
        return self.__velocity[HEIGHT] < 0
    def xy_pos(self) -> tuple[float, float]:
        return (self.__position[X], self.__position[Y])
    
    def clamp_velocity(self):
        speed_x, speed_y, speed_z = self.__velocity
        speed = sqrt(speed_x ** 2 + speed_y ** 2)
        if speed > self.max_velocity:
            scale = self.max_velocity / speed
            self.__velocity = (speed_x * scale, speed_y * scale, speed_z)
    
    def set_bounds(self, top, bottom, left, right):
        self.__bounds = (top, bottom, left, right)
    def within_rect(self, rect: pg.Rect, x_offset: float, y_offset: float) -> bool:
        if self.__position[X] > rect.left + x_offset and self.__position[X] < rect.right + x_offset \
                and self.__position[Y] > rect.top + y_offset and self.__position[Y] < rect.bottom + y_offset:
            return True
        return False
    def within_rect(self, rect: pg.Rect, offset: tuple[float, float]) -> bool:
        x_offset = offset[X]
        y_offset = offset[Y]
        if self.__position[X] > rect.left + x_offset and self.__position[X] < rect.right + x_offset \
                and self.__position[Y] > rect.top + y_offset and self.__position[Y] < rect.bottom + y_offset:
            return True
        return False
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
    def impulse(self, impulse: tuple[float, float]):
        '''Apply an impulse to the ball, changing its velocity.'''
        self.__velocity = (
            self.__velocity[X] + impulse[X],
            self.__velocity[Y] + impulse[Y],
            self.__velocity[HEIGHT]
        )
    def bounce(self, normal_x: float, normal_y: float):
        '''Bounce the ball off a surface with the given normal vector.'''
        # Calculate the dot product of the velocity and the normal
        dot_product = self.__velocity[X] * normal_x + self.__velocity[Y] * normal_y
        # Reflect the velocity across the normal
        self.__velocity = (
            self.__velocity[X] - 2 * dot_product * normal_x,
            self.__velocity[Y] - 2 * dot_product * normal_y,
            abs(self.__velocity[HEIGHT]) - (self.gravity * 2)
        )
        self.trailPositions.clear()
    def multiplyVelocity(self, value: float):
        self.__velocity = (
            self.__velocity[X] * value,
            self.__velocity[Y] * value,
            self.__velocity[HEIGHT]
        )
    
    def draw(self, screen):
        self.update_position()  # Update the ball's position before drawing
        self.draw_trail(screen)
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
            predicted_positions.append((current_pos[X], current_pos[Y] - current_pos[HEIGHT]))
            if current_pos[HEIGHT] <= 0:  # Stop prediction if ball bounces twice
                bounces += 1
                if bounces >= 2:
                    break

        # Draw the trajectory as a series of lines
        if draw_lines:
            pg.draw.lines(surface=screen, color=WHITE, closed=False, points=predicted_positions, width=2)
              
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
            predicted_positions.append((current_pos[X], current_pos[Y]))
            if current_pos[HEIGHT] <= 0:  # Stop prediction if ball bounces twice
                bounces += 1
                if bounces >= 2:
                    break

        # Draw the trajectory as a series of lines
        pg.draw.lines(surface=screen, color=(100,100,100), closed=False, points=predicted_positions, width=2)
         
    def update_position(self):
        self.__position, self.__velocity = self.step_physics(self.__position, self.__velocity)
        self.trailPositions.push(self.__position)

    def draw_trail(self, screen: pg.Surface):
        if self.trailPositions.length() < 2:
            return
        points = self.trailPositions.positionList()
        trailColor = hsv_to_rgb(1 - min(self.velocityMagnitude() / self.max_velocity, 1), 1, 1)
        trailColor = (
            int(trailColor[0] * 255),
            int(trailColor[1] * 255),
            int(trailColor[2] * 255)
        )
        if len(points) >= int(self.trailPositions.trailSize / 4):
            pg.draw.lines(surface=screen, color=WHITE, closed=False, 
                        points=points[:int(self.trailPositions.trailSize / 4)], 
                        width=int(self.trailThickness / 4))
        else:
            pg.draw.lines(surface=screen, color=WHITE, closed=False, 
                        points=points, width=int(self.trailThickness / 4))
            return
        if len(points) >= int(self.trailPositions.trailSize / 2):
            pg.draw.lines(surface=screen, color=WHITE, closed=False, 
                        points=points[int(self.trailPositions.trailSize / 4):int(self.trailPositions.trailSize / 2)],
                        width=int(self.trailThickness / 2))
            pg.draw.lines(surface=screen, color=trailColor, closed=False,
                        points=points[int(self.trailPositions.trailSize / 4):int(self.trailPositions.trailSize / 2)], 
                        width=int(self.trailThickness / 4) - 1)
        else:
            pg.draw.lines(surface=screen, color=WHITE, closed=False, 
                        points=points[int(self.trailPositions.trailSize / 4) - 2:], 
                        width=int(self.trailThickness / 2))
            pg.draw.lines(surface=screen, color=trailColor, closed=False,
                        points=points[int(self.trailPositions.trailSize / 4) - 2:], 
                        width=int(self.trailThickness / 4) - 1)
            return
        if len(points) >= int(self.trailPositions.trailSize * 3/4):
            pg.draw.lines(surface=screen, color=WHITE, closed=False, 
                        points=points[int(self.trailPositions.trailSize / 2):int(self.trailPositions.trailSize * 3/4)],
                        width=int(self.trailThickness * 3/4))
            pg.draw.lines(surface=screen, color=trailColor, closed=False,
                        points=points[int(self.trailPositions.trailSize / 2):int(self.trailPositions.trailSize * 3/4)], 
                        width=int(self.trailThickness * 3/8))
        else:
            pg.draw.lines(surface=screen, color=WHITE, closed=False, 
                        points=points[int(self.trailPositions.trailSize / 2) - 2:], 
                        width=int(self.trailThickness * 3/4))
            pg.draw.lines(surface=screen, color=trailColor, closed=False,
                        points=points[int(self.trailPositions.trailSize / 2) - 2:], 
                        width=int(self.trailThickness * 3/8))
            return
        pg.draw.lines(surface=screen, color=WHITE, closed=False, 
                    points=points[int(self.trailPositions.trailSize * 3/4) - 2:], width=int(self.trailThickness))
        pg.draw.lines(surface=screen, color=trailColor, closed=False,
                    points=points[int(self.trailPositions.trailSize * 3/4) - 2:], width=int(self.trailThickness / 2))

#ball_characteristics = Ball(x=30, y=300, height=100, speed_x=1.5, speed_y=0.2, radius=8, spin=0.1)  # Example initialization
#ball_characteristics.draw(pg.display.set_mode((800, 600)))  # Example drawing on a Pygame screen