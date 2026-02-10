import pygame
import sys

pygame.init()

# random constants
Width = 800
Height = 600
FPS = 60
Paddle_Speed = 5
Ball_Radius = 10
Gravity = 0.35
BounceSpeedLost = 0.85
Max_Speed = 8
Paddle_Boost = 1.4

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)
SHADOW = (0, 50, 0, 100)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Supreme Pong")
clock = pygame.time.Clock()

# table surface
table_surface = pygame.Surface((800, 600))
table_surface.fill(DARK_GREEN)

# table border
pygame.draw.rect(table_surface, WHITE, (50, 50, 700, 500), 5)

pygame.draw.line(table_surface, WHITE, (400, 50), (400, 550), 3)


#sample paddles
paddle1_surface = pygame.Surface((20,80))
paddle1_surface.fill((255, 100, 100))
pygame.draw.rect(paddle1_surface, WHITE, (0, 0, 20, 80), 2)

paddle2_surface = pygame.Surface((20,80))
paddle2_surface.fill((100, 100, 255))
pygame.draw.rect(paddle1_surface, WHITE, (0, 0, 20, 80), 2)

paddle1_x = 100
paddle1_y = Height // 2 - 40

paddle2_x = Width - 120
paddle2_y = Height // 2 - 40

Left_Boundary = 50
Right_Boundary = Width - 50
Top_Boundary = 50
Bot_Boundary = Height - 50
Center_x = Width // 2

# ball physics
ball_x = Width // 2
ball_y = Height // 2
ball_vel_x = 1
ball_vel_y = 0.8
ball_height = 0
ball_vel_z = 0
ball_max_height = 25

# actual game
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # paddle 1 movement (WASD)
    if keys[pygame.K_w] and paddle1_y > Top_Boundary:
        paddle1_y -= Paddle_Speed
    if keys[pygame.K_s] and paddle1_y + 80 < Bot_Boundary:
        paddle1_y += Paddle_Speed
    if keys[pygame.K_a] and paddle1_x > Left_Boundary:
        paddle1_x -= Paddle_Speed
    if keys[pygame.K_d] and paddle1_x + 20 < Center_x:
        paddle1_x += Paddle_Speed

    # paddle 2 movement (arrow keys)
    if keys[pygame.K_UP] and paddle2_y > Top_Boundary:
        paddle2_y -= Paddle_Speed
    if keys[pygame.K_DOWN] and paddle2_y + 80 < Bot_Boundary:
        paddle2_y += Paddle_Speed
    if keys[pygame.K_LEFT] and paddle2_x > Center_x:
        paddle2_x -= Paddle_Speed
    if keys[pygame.K_RIGHT] and paddle2_x + 20 < Right_Boundary:
        paddle2_x += Paddle_Speed

    # Trying to make a ball
    ball_vel_z -= Gravity
    ball_height += ball_vel_z

    # bounce when ball hits table
    if ball_height <= 0:
        ball_height = 0
        ball_vel_z = abs(ball_vel_z) * BounceSpeedLost

        # reduce speed on bounce
        ball_vel_x *= 0.9
        ball_vel_y *= 0.9

        # keeping ball velocity
        if ball_vel_z < 8:
            ball_vel_z = 8

    ball_x += ball_vel_x
    ball_y += ball_vel_y

    # ball collision with walls
    if ball_x - Ball_Radius <= Left_Boundary or ball_x + Ball_Radius >= Right_Boundary:
        ball_vel_x *= -1
        ball_x = max(Left_Boundary + Ball_Radius, min(ball_x, Right_Boundary - Ball_Radius))

    if ball_y - Ball_Radius <= Top_Boundary or ball_y + Ball_Radius >= Bot_Boundary:
        ball_vel_y *= -1
        ball_y = max(Top_Boundary + Ball_Radius, min(ball_y, Bot_Boundary - Ball_Radius))

    # ball collision with paddles
    if ball_height < 15:
        if (paddle1_x < ball_x < paddle1_x + 20 and paddle1_y
            < ball_y < paddle1_y + 80):
            ball_vel_x = abs(ball_vel_x) +1
            # speed cap
            ball_vel_x = min(ball_vel_x, Max_Speed)
            ball_vel_y = min(abs(ball_vel_y), Max_Speed) * (1 if ball_vel_y > 0 else -1)
            ball_vel_z = 8 # bounce this

        if (paddle2_x < ball_x < paddle2_x + 20 and paddle2_y
            < ball_y < paddle2_y + 80):
            ball_vel_x = -abs(ball_vel_x) -1
            # speed cap
            ball_vel_x = max(ball_vel_x, -Max_Speed)
            ball_vel_y = min(abs(ball_vel_y), Max_Speed) * (1 if ball_vel_y > 0 else -1)
            ball_vel_z = 8 # bounce this

   

    screen.fill(BLACK)

    screen.blit(table_surface, (0, 0))

    screen.blit(paddle1_surface, (paddle1_x, paddle1_y))
    screen.blit(paddle2_surface, (paddle2_x, paddle2_y))

    # ball shadow
    shadow_offset = ball_height * 0.3
    shadow_radius = max(3, int(Ball_Radius * (1 - ball_height / 150)))
    shadow_transparency = max(30, int(150 * (1 - ball_height / 150)))

    shadow_surface = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(shadow_surface, (0, 50, 0, shadow_transparency),
                       (shadow_radius, shadow_radius), shadow_radius)
    screen.blit(shadow_surface, 
                (int(ball_x - shadow_radius + shadow_offset), 
                 int(ball_y - shadow_radius + shadow_offset))) 


    # actual ball
    ball_screen_y = ball_y - ball_height
    pygame.draw.circle(screen, ORANGE, (int(ball_x), int(ball_screen_y)), Ball_Radius)
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_screen_y)), Ball_Radius, 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
