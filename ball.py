import pygame as pg
class Ball:
    def __init__(self, speed_x, speed_y, radius):
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius

    def speed(self):
        return (self.speed_x, self.speed_y)
    
    def initial_position(self):
        return (self.x, self.y)

def ball_start_movement(ball, paddle1, paddle2):
    ball.initial_position(300,400) #Example for now, its gonna be infront of player1s position

    if ball.collidirect(paddle1):
        ball.speed_x *= 1.5
        ball.speed_y *= 1
    elif ball.collidirect(paddle2):
        ball.speed_x *= 1.5
        ball.speed_y *= 1

    else:
        pass

def ball_smash_hit(ball, paddle1, paddle2):
    ball.speed_x *= 2
    ball.speed_y *= 2
    paddle1.speed_x *= 2
    paddle1.speed_y *= 2
    paddle2.speed_x *= 2
    paddle2.speed_y *= 2

def ball_reset(ball):
    pass
    ## if game_over == True:
    ##     if player1_score > player2_score:
    ##         print("Player 1 wins!")
                #ball.initial_position (whatever paddle2 position is)
    ##     elif player2_score > player1_score:
    ##         print("Player 2 wins!")
                #ball.initial_position (whatever paddle1 position is)
