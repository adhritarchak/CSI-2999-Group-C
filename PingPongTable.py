import pygame
import sys

pygame.init()
pygame.display.set_caption("SupremePong")

# Window
WIDTH, HEIGHT = 1000, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# GameColors
LIGHT_BROWN = (200, 170, 130)
RED_TABLE = (170, 40, 40)
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)

# Table layout
TABLE_MARGIN = 80
TABLE_BORDER = 5
NET_THICKNESS = 4
MIDLINE_THICKNESS = 3

table_rect = pygame.Rect(
    TABLE_MARGIN,
    TABLE_MARGIN,
    WIDTH - TABLE_MARGIN * 2,
    HEIGHT - TABLE_MARGIN * 2
)
def draw_table():
    # Background
    SCREEN.fill(LIGHT_BROWN)
    shadow = table_rect.move(6, 6)
    pygame.draw.rect(SCREEN, BLACK, shadow, border_radius=6)
    pygame.draw.rect(SCREEN, RED_TABLE, table_rect)

    # Table border
    pygame.draw.rect(SCREEN, WHITE, table_rect, TABLE_BORDER)

    # PingPong Net
    pygame.draw.line(
        SCREEN, WHITE,
        (table_rect.centerx, table_rect.top),
        (table_rect.centerx, table_rect.bottom),
        NET_THICKNESS
    )

    # Center horizontal line
    pygame.draw.line(
        SCREEN, WHITE,
        (table_rect.left, table_rect.centery),
        (table_rect.right, table_rect.centery),
        MIDLINE_THICKNESS
    )

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_table()
        pygame.display.flip()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()
