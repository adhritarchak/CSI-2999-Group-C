import pygame
import sys

pygame.init()

# random constants

# Window Constants
Width = 1000
Height = 600
FPS = 60
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Supreme Pong")
clock = pygame.time.Clock()

# Table Layout/Dimensions
Table_Margin = 80
Table_Border = 5
Net_Thickness = 4
Midline_Thickness = 3

Table_Rect = pygame.Rect(Table_Margin, Table_Margin,
                         Width - Table_Margin * 2,
                         Height - Table_Margin * 2,)

Left_Boundary = Table_Rect.left
Right_Boundary = Table_Rect.right
Top_Boundary = Table_Rect.top
Bot_Boundary = Table_Rect.bottom
Center_x = Table_Rect.centerx
Center_y = Table_Rect.centery

# Paddle Constants
Paddle_Speed = 5
Paddle_Boost = 1.4
Paddle_Width = 20
Paddle_Height = 80
BasePaddleSpeed = 5
Paddle1_Speed = BasePaddleSpeed
Paddle2_Speed = BasePaddleSpeed
Smash_start_time = 0
Smash1_hold_time = 0
Smash1_active = False
Smash2_hold_time = 0
Smash2_active = False
Smash_duration = 3000

# Ball Constants
Ball_Radius = 10
Ball_Max_Height = 25

# Ball Physics Constants
ball_init_vel_x = 3
ball_init_vel_y = 1.5
ball_init_vel_z = 8
Gravity = 0.35
BounceSpeedLost = 0.85
Max_Speed = 10
Bounce_MinZ = 8
paddle_hit_boost = 1


ball_x = Width // 2
ball_y = Height // 2
ball_vel_x = 1
ball_vel_y = 0.8
ball_height = 0
ball_vel_z = 0



# colors constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_TABLE = (170, 40, 40)
LIGHT_BROWN = (200, 170, 130)
ORANGE = (255, 165, 0)
SHADOW = (0, 50, 0, 100)
PADDLE1_COLOR = (255, 100, 100)
PADDLE2_COLOR = (100, 100, 255)


#sample paddles
paddle1_surface = pygame.Surface((Paddle_Width, Paddle_Height))
paddle1_surface.fill((PADDLE1_COLOR))
pygame.draw.rect(paddle1_surface, WHITE, (0, 0, Paddle_Width, Paddle_Height), 2)

paddle2_surface = pygame.Surface((Paddle_Width, Paddle_Height))
paddle2_surface.fill((PADDLE2_COLOR))
pygame.draw.rect(paddle2_surface, WHITE, (0, 0, Paddle_Width, Paddle_Height), 2)

paddle1_x = Left_Boundary + 50
paddle1_y = Center_y - Paddle_Height // 2

paddle2_x = Right_Boundary - 50 - Paddle_Width
paddle2_y = Center_y - Paddle_Height // 2

def draw_table():
    # Background
    screen.fill(LIGHT_BROWN)
    shadow = Table_Rect.move(6, 6)
    pygame.draw.rect(screen, BLACK, shadow, border_radius=6)
    pygame.draw.rect(screen, RED_TABLE, Table_Rect)

    # Table border
    pygame.draw.rect(screen, WHITE, Table_Rect, Table_Border)

    # PingPong Net
    pygame.draw.line(
        screen, WHITE,
        (Table_Rect.centerx, Table_Rect.top),
        (Table_Rect.centerx, Table_Rect.bottom),
        Net_Thickness
    )

    # Center horizontal line
    pygame.draw.line(
        screen, WHITE,
        (Table_Rect.left, Table_Rect.centery),
        (Table_Rect.right, Table_Rect.centery),
        Midline_Thickness
    )

def draw_ball(bx, by, bheight):
    # shadow 
    shadow_offset = bheight * 0.3
    shadow_radius = max(3, int(Ball_Radius * (1 - bheight / 150)))
    shadow_transparency = max(30, int(150 * (1 - bheight / 150)))

    shadow_surface = pygame.Surface((shadow_radius * 2, shadow_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(shadow_surface, (0, 50, 0, shadow_transparency),
                       (shadow_radius, shadow_radius), shadow_radius)
    screen.blit(shadow_surface, 
                (int(bx - shadow_radius + shadow_offset), 
                 int(by - shadow_radius + shadow_offset))) 


    # actual ball
    ball_screen_y = by - bheight
    pygame.draw.circle(screen, ORANGE, (int(bx), int(ball_screen_y)), Ball_Radius)
    pygame.draw.circle(screen, WHITE, (int(bx), int(ball_screen_y)), Ball_Radius, 2)


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
    if keys[pygame.K_SPACE]: # regular
        if paddle1_x < ball_x < paddle1_x + 20 and paddle1_y < ball_y < paddle1_y + 80:
            ball_vel_x += 1 
    if keys[pygame.K_LSHIFT]: #smash
        Smash1_hold_time += clock.get_time()
    if Smash1_hold_time >= 3000 and not Smash1_active:
            Smash1_active = True
            Smash1_start_time = pygame.time.get_ticks()
            Paddle1_Speed = BasePaddleSpeed - 2.5
            Smash1_hit = False
    if Smash1_active == True:
        if paddle1_x < ball_x < paddle1_x + 20 and paddle1_y < ball_y < paddle1_y + 80:
                ball_vel_x += 10
                Smash1_hit = True
    if Smash1_active and pygame.time.get_ticks() - Smash1_start_time >= Smash_duration:
            Smash1_active = False
            Smash1_hold_time = 0
            Paddle1_Speed = BasePaddleSpeed 
            Smash1_hit = False

    # paddle 2 movement (arrow keys)
    if keys[pygame.K_UP] and paddle2_y > Top_Boundary:
        paddle2_y -= Paddle_Speed
    if keys[pygame.K_DOWN] and paddle2_y + 80 < Bot_Boundary:
        paddle2_y += Paddle_Speed
    if keys[pygame.K_LEFT] and paddle2_x > Center_x:
        paddle2_x -= Paddle_Speed
    if keys[pygame.K_RIGHT] and paddle2_x + 20 < Right_Boundary:
        paddle2_x += Paddle_Speed
    if keys[pygame.K_RETURN]: # regular
        if paddle2_x < ball_x < paddle2_x + 20 and paddle2_y < ball_y < paddle2_y + 80:
            ball_vel_x += 1 
    if keys[pygame.K_RSHIFT]: #smash
        Smash2_hold_time += clock.get_time()
    if Smash2_hold_time >= 3000 and not Smash2_active:
            Smash2_active = True
            Smash2_start_time = pygame.time.get_ticks()
            Paddle2_Speed = BasePaddleSpeed - 2.5
            Smash2_hit = False
    if Smash2_active == True:
        if paddle2_x < ball_x < paddle2_x + 20 and paddle2_y < ball_y < paddle2_y + 80:
                ball_vel_x *= 2
                Smash2_hit = True
    if Smash2_active and pygame.time.get_ticks() - Smash2_start_time >= Smash_duration:
            Smash2_active = False
            Smash2_hold_time = 0
            Paddle2_Speed = BasePaddleSpeed 
            Smash2_hit = False

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
        if ball_vel_z < Bounce_MinZ:
            ball_vel_z = Bounce_MinZ

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
        p1_hit = (paddle1_x < ball_x < paddle1_x + Paddle_Width and 
                  paddle1_y < ball_y < paddle1_y + Paddle_Height)
        p2_hit = (paddle2_x < ball_x < paddle2_x + Paddle_Width and 
                  paddle2_y < ball_y < paddle2_y + Paddle_Height)

        if p1_hit:
            ball_vel_x = min(abs(ball_vel_x) + paddle_hit_boost, Max_Speed)
            ball_vel_y = (min(abs(ball_vel_y), Max_Speed) * (1 if ball_vel_y > 0 else -1))
            ball_vel_z = Bounce_MinZ

        if p2_hit:
            ball_vel_x = max(-(abs(ball_vel_x) + paddle_hit_boost), -Max_Speed)
            ball_vel_y = (min(abs(ball_vel_y), Max_Speed) * (1 if ball_vel_y > 0 else -1))
            ball_vel_z = Bounce_MinZ

    draw_table()

    screen.blit(paddle1_surface, (paddle1_x, paddle1_y))
    screen.blit(paddle2_surface, (paddle2_x, paddle2_y))

    draw_ball(ball_x, ball_y, ball_height)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
