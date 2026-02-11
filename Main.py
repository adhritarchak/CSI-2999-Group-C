# Base file
import pygame as pg

class Paddle:
    paddleSurface: pg.Surface
    paddleImages: list[pg.Surface]

    def __init__(self, assetList: list[str]):
        paddleImages = list[pg.Surface]
    def animate_paddle():
        pass
    def smash_hit(self, ball):
        self.speed_x *= 1.5
        self.speed_y *= 1.5
        ball.speed_x *= 1.5
        ball.speed_y *= 1.5
def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("My Game")
    clock = pg.time.Clock()
    if not pg.display.get_init():
        pg.display.init()

    paddle = pg.image.load("assets/Red Paddle.png").convert_alpha()
    paddle_rect = paddle.get_rect(topleft=(100, 100))
    pg.draw.rect(screen, (255, 0, 0), paddle_rect)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Fill screen with black
        screen.blit(paddle, paddle_rect)
        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()

