import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Supreme Pong")

# Fonts
title_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 45)

# Colors
BLUE = (0, 120, 255)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# Play button
button_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 240, 70)

clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Play button clicked")  # placeholder

    # Title
    title_text = title_font.render("Supreme Pong", True, WHITE)
    screen.blit(
        title_text,
        (WIDTH//2 - title_text.get_width()//2, 120)
    )

    # Button hover effect
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, DARK_GRAY, button_rect)
    else:
        pygame.draw.rect(screen, GRAY, button_rect)

    # Play text
    play_text = button_font.render("Play", True, BLACK)
    screen.blit(
        play_text,
        (
            button_rect.centerx - play_text.get_width()//2,
            button_rect.centery - play_text.get_height()//2,
        )
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
