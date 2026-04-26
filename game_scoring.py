class GameScoring:
    def __init__(self, scoreboard, ball, paddle1, paddle2, bounds):
        self.scoreboard = scoreboard
        self.ball = ball
        self.paddle1 = paddle1
        self.paddle2 = paddle2
        self.left_boundary = bounds['left']
        self.right_boundary = bounds['right']
        
    def check_score(self):
        # Get the ball's actual X position
        ball_x = self.ball.get_position()[0]
        ball_y = self.ball.get_position()[1]
        
        # Check if ball passed left boundary (Player 2 scores)
        if ball_x < self.left_boundary - 20:
            print(f"Ball passed left boundary at x={ball_x} - Player 2 scores!")
            return True, 2
        # Check if ball passed right boundary (Player 1 scores)
        if ball_x > self.right_boundary + 20:
            print(f"Ball passed right boundary at x={ball_x} - Player 1 scores!")
            return True, 1
        if ball_y < self.scoreboard.screen.get_height() * 0.1:  # Top 10% of screen
            print(f"Ball passed top boundary at y={ball_y} - Player 2 scores!")
            return True, 2
    
    # Check if ball passed bottom boundary (Player 1 scores)
        if ball_y > self.scoreboard.screen.get_height() * 0.9:  # Bottom 10% of screen
            print(f"Ball passed bottom boundary at y={ball_y} - Player 1 scores!")
            return True, 1
        return False, None
        
    def reset_ball_for_serve(self, ball_config, scorer=None):
        """Reset ball on the loser's side (whoever didn't score)"""
        if scorer == 1:
            # Player 1 won the previous round, so Player 2 serves (ball on Player 2's side)
            self.ball.set_position(
                self.paddle2.hitbox.left - self.ball.radius - 5,
                self.paddle2.hitbox.centery,
                ball_config['init_height']
            )
        elif scorer == 2:
            # Player 2 won the previous round, so Player 1 serves (ball on Player 1's side)
            self.ball.set_position(
                self.paddle1.hitbox.right + self.ball.radius + 5,
                self.paddle1.hitbox.centery,
                ball_config['init_height']
            )
        else:
            # First round of the match - Player 1 serves
            self.ball.set_position(
                self.paddle1.hitbox.right + self.ball.radius + 5,
                self.paddle1.hitbox.centery,
                ball_config['init_height']
            )
        self.paddle1.hitbox.width = self.paddle1.original_width if hasattr(self.paddle1, 'original_width') else self.paddle1.hitbox.width
        self.paddle1.hitbox.height = self.paddle1.original_height if hasattr(self.paddle1, 'original_height') else self.paddle1.hitbox.height
        self.paddle2.hitbox.width = self.paddle2.original_width if hasattr(self.paddle2, 'original_width') else self.paddle2.hitbox.width
        self.paddle2.hitbox.height = self.paddle2.original_height if hasattr(self.paddle2, 'original_height') else self.paddle2.hitbox.height

        self.ball.radius = ball_config['Radius']

        self.ball.grav_pull_active = False
        self.ball.grav_pull_activator = None
        self.ball.grav_pull_timer = 0
        self.ball.grav_pull_waiting = False
        self.ball.grav_pull_triggered = False
        self.ball.grav_pull_bounced = False

        self.paddle1.set_hitbox_pos(0, 0)
        self.paddle2.set_hitbox_pos(0, 0)
        self.ball.set_velocity(0, 0, 0)
        self.ball.served = False
        self.ball.spin = 0

    def reset_paddle_states(self):
        self.paddle1.smash_charging = False
        self.paddle2.smash_charging = False
        self.paddle1.smashPower = 0
        self.paddle2.smashPower = 0
        self.paddle1.swinging = False
        self.paddle2.swinging = False
        self.paddle1.has_hit_ball = False
        self.paddle2.has_hit_ball = False
        self.paddle1.swingTimer = 0
        self.paddle2.swingTimer = 0
        self.paddle1.cooldownTimer = 0
        self.paddle2.cooldownTimer = 0
        self.paddle1.smashTimer = 0
        self.paddle2.smashTimer = 0
        self.paddle1.can_hit_ball = False
        self.paddle2.can_hit_ball = False
        self.paddle1.paddleSurface = self.paddle1.sprites[0] 
        self.paddle2.paddleSurface = self.paddle2.sprites[0]
        
    def reset_for_new_round(self, paddle_config, ball_config, center_y, left_boundary, right_boundary, round_winner=None):
        self.paddle1.position = (left_boundary + 50, center_y - paddle_config['Paddle_Height'] // 2)
        self.paddle2.position = (right_boundary - 50 - paddle_config['Paddle_Width'], center_y - paddle_config['Paddle_Height'] // 2)
        self.paddle1.set_hitbox_pos(0, 0)
        self.paddle2.set_hitbox_pos(0, 0)
        
        self.reset_ball_for_serve(ball_config, round_winner)
        
        self.reset_paddle_states()
        self.paddle1.can_swing = True
        self.paddle2.can_swing = True
        self.paddle1.cooldownTimer = 0
        self.paddle2.cooldownTimer = 0