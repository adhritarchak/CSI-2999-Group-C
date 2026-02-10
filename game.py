import pygame
import sys

pygame.init()

# random constants
Width = 800
Height = 600
FPS = 60
Paddle_Speed = 5

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)

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

    screen.fill(BLACK)

    screen.blit(table_surface, (0, 0))

    screen.blit(paddle1_surface, (paddle1_x, paddle1_y))
    screen.blit(paddle2_surface, (paddle2_x, paddle2_y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
