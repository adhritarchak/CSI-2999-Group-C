# Base file
import pygame as pg
from Pong import *

SCREEN_SIZE = (800, 600)

class Paddle:
    paddleSurface: pg.Surface
    paddleImages: list[pg.Surface]

    def __init__(self, assetList: list[str]):
        paddleImages = list[pg.Surface]
    def animate_paddle():
        pass
    def smash_hit(self, ball: Ball):
        ball.impulse((ball.velocity()[X] * 1.5, ball.velocity()[Y] * 1.5, 0))
def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("My Game")
    clock = pg.time.Clock()
    if not pg.display.get_init():
        pg.display.init()

    # paddle = pg.image.load("assets/Red Paddle.png").convert_alpha()
    # paddle_rect = paddle.get_rect(topleft=(100, 100))
    # pg.draw.rect(screen, (255, 0, 0), paddle_rect)
    
    ball = Ball(x=30, y=300, height=100, speed_x=1.5, speed_y=1, radius=8)
    ball.do_draw_prediction(True)
    ball.set_bounds(top=100, bottom=SCREEN_SIZE[Y], left=0, right=SCREEN_SIZE[X])

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    ball.do_draw_prediction(not ball.draw_prediction)

        screen.fill((0, 0, 0))  # Fill screen with black
        # screen.blit(paddle, paddle_rect)
        ball.draw(screen)
        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()

