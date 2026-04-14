import pygame
import math
import random
import sys

class Scoreboard:
    def __init__(self, screen, font):
        self.screen = screen
        self.p1_rnd = 0
        self.p2_rnd = 0
        self.p1_pts = 0
        self.p2_pts = 0
        self.round = 1
        self.active = True
        self.round_active = True
        self.match_over = False
        self.waiting = False
        self.winner = None
        self.rnd_winner = None
        self.flash_timer = 0
        self.flash_player = 0
        self.alpha = 0
        self.point_confetti = []
        self.showing_round_end = False
        self.showing_match_end = False
        
    def reset_round(self):
        self.p1_pts = 0
        self.p2_pts = 0
        self.active = True
        self.round_active = True
        self.rnd_winner = None
        self.waiting = False
        # Don't reset showing_round_end here
        
    def reset_match(self):
        self.p1_rnd = 0
        self.p2_rnd = 0
        self.round = 1
        self.round_active = True
        self.match_over = False
        self.winner = None
        self.alpha = 0
        self.point_confetti = []
        self.showing_round_end = False
        self.showing_match_end = False
        self.reset_round()
        
    def add_point(self, p):
        if not self.active or self.match_over:
            return False
            
        self.flash_timer = 10
        self.flash_player = p
        
        if p == 1:
            self.p1_pts += 1
            print(f"Player 1 scores! Points: {self.p1_pts}/3")
        else:
            self.p2_pts += 1
            print(f"Player 2 scores! Points: {self.p2_pts}/3")
        
        self.add_confetti(20)
        
        # Check if round is won (first to 3 points)
        if self.p1_pts >= 3:
            print(f"🎯 Player 1 wins Round {self.round}!")
            return self.end_round(1)
        if self.p2_pts >= 3:
            print(f"🎯 Player 2 wins Round {self.round}!")
            return self.end_round(2)
            
        return True
        
    def add_confetti(self, count=30):
        for _ in range(count):
            self.point_confetti.append({
                'x': random.randint(0, self.screen.get_width()),
                'y': random.randint(0, self.screen.get_height() // 2),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(2, 6),
                'color': random.choice([(255, 215, 0), (255, 100, 100), (100, 100, 255), (255, 255, 255)]),
                'size': random.randint(3, 7),
                'life': 90
            })
        
    def update_confetti(self):
        for conf in self.point_confetti[:]:
            conf['x'] += conf['vx']
            conf['y'] += conf['vy']
            conf['life'] -= 1
            if conf['life'] <= 0 or conf['y'] > self.screen.get_height():
                self.point_confetti.remove(conf)
                
    def draw_confetti(self):
        for conf in self.point_confetti:
            pygame.draw.rect(self.screen, conf['color'], 
                           (conf['x'], conf['y'], conf['size'], conf['size']))
        
    def end_round(self, w):
        self.active = False
        self.round_active = False
        self.rnd_winner = w
        self.waiting = True
        
        # Update round wins
        if w == 1:
            self.p1_rnd += 1
        else:
            self.p2_rnd += 1
            
        print(f"Round {self.round} final score: {self.p1_pts} - {self.p2_pts}")
        print(f"Match score: {self.p1_rnd} - {self.p2_rnd}")
        
        self.add_confetti(80)
        
        # Check if we've completed all 5 rounds OR someone reached 3 wins
        if self.round >= 5 or self.p1_rnd >= 3 or self.p2_rnd >= 3:
            self.match_over = True
            if self.p1_rnd > self.p2_rnd:
                self.winner = 1
            else:
                self.winner = 2
            self.showing_match_end = True
            print(f"\n🏆 PLAYER {self.winner} WINS THE MATCH! 🏆")
            print(f"Final match score: {self.p1_rnd} - {self.p2_rnd}")
            self.add_confetti(200)
            return False
        
        # Show round end screen
        self.showing_round_end = True
        print(f"\n--- Round {self.round} complete ---")
        return True
        
    def start_next_round(self):
        """Called when player presses SPACE to start next round"""
        self.round += 1
        self.reset_round()
        print(f"\n--- Starting Round {self.round} ---")
    
    def draw(self):
        w = self.screen.get_width()
        if self.flash_timer > 0:
            self.flash_timer -= 1
        
        self.update_confetti()
        self.draw_confetti()
        
        # Don't draw normal scoreboard during end screens
        if self.showing_round_end or self.showing_match_end:
            return
        
        # Background
        y = 5
        s = pygame.Surface((500, 65), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        pygame.draw.rect(s, (255, 215, 0, 80), s.get_rect(), 2, 10)
        self.screen.blit(s, (w//2 - 250, y))
        
        c1 = (255, 220, 80) if self.flash_player == 1 and self.flash_timer > 0 else (255, 200, 50)
        c2 = (255, 220, 80) if self.flash_player == 2 and self.flash_timer > 0 else (255, 200, 50)
        
        # Player 1 score (points in current round)
        p1_label = pygame.font.Font(None, 20).render("P1", True, (255, 150, 150))
        self.screen.blit(p1_label, (w//2 - 230, y + 5))
        p1_score = pygame.font.Font(None, 44).render(str(self.p1_pts), True, c1)
        self.screen.blit(p1_score, (w//2 - 200, y + 18))
        
        # Player 2 score (points in current round)
        p2_label = pygame.font.Font(None, 20).render("P2", True, (150, 150, 255))
        self.screen.blit(p2_label, (w//2 + 200, y + 5))
        p2_score = pygame.font.Font(None, 44).render(str(self.p2_pts), True, c2)
        self.screen.blit(p2_score, (w//2 + 170, y + 18))
        
        # Round number
        round_text = pygame.font.Font(None, 16).render(f"ROUND {self.round}/5", True, (200, 200, 220))
        round_rect = round_text.get_rect(center=(w//2, y + 12))
        self.screen.blit(round_text, round_rect)
        
        # Match score (rounds won)
        match_text = pygame.font.Font(None, 20).render(f"{self.p1_rnd} - {self.p2_rnd}", True, (255, 215, 0))
        match_rect = match_text.get_rect(center=(w//2, y + 32))
        self.screen.blit(match_text, match_rect)
        
        # Progress dots
        dot_y = y + 60
        for i in range(3):
            c1d = (255, 100, 100) if i < self.p1_pts else (40, 40, 50)
            c2d = (100, 100, 255) if i < self.p2_pts else (40, 40, 50)
            pygame.draw.circle(self.screen, c1d, (w//2 - 210 + i*22, dot_y), 3)
            pygame.draw.circle(self.screen, c2d, (w//2 + 190 - i*22, dot_y), 3)

    def draw_round_end(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        
        self.update_confetti()
        self.draw_confetti()
        
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        bounce = abs(math.sin(pygame.time.get_ticks() * 0.004)) * 8
        
        if self.rnd_winner == 1:
            winner_text = f"PLAYER 1 WINS ROUND {self.round}!"
            winner_color = (255, 120, 120)
        else:
            winner_text = f"PLAYER 2 WINS ROUND {self.round}!"
            winner_color = (120, 120, 255)
        
        big_font = pygame.font.Font(None, 52)
        title = big_font.render(winner_text, True, winner_color)
        self.screen.blit(title, title.get_rect(center=(w//2, h//2 - 60 + bounce)))
        
        score_text = big_font.render(f"{self.p1_pts}  -  {self.p2_pts}", True, (255, 215, 0))
        self.screen.blit(score_text, score_text.get_rect(center=(w//2, h//2 + 20)))
        
        series_font = pygame.font.Font(None, 32)
        series_text = series_font.render(f"MATCH SCORE: {self.p1_rnd} - {self.p2_rnd}", True, (200, 200, 200))
        self.screen.blit(series_text, series_text.get_rect(center=(w//2, h//2 + 80)))
        
        rounds_left = 5 - self.round
        if rounds_left > 0:
            remaining_text = series_font.render(f"{rounds_left} ROUNDS REMAINING", True, (150, 150, 150))
            self.screen.blit(remaining_text, remaining_text.get_rect(center=(w//2, h//2 + 110)))
        
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.5 + 0.5
        color_val = max(0, min(255, int(255 * pulse)))
        continue_font = pygame.font.Font(None, 28)
        continue_text = continue_font.render("PRESS SPACE TO CONTINUE", True, (color_val, color_val, 255))
        self.screen.blit(continue_text, continue_text.get_rect(center=(w//2, h//2 + 140)))

    def draw_match_end(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        
        self.update_confetti()
        self.draw_confetti()
        
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        if random.randint(0, 15) == 0:
            self.add_confetti(15)
        
        if self.winner == 1:
            winner_text = "PLAYER 1 WINS THE MATCH!"
            winner_color = (255, 150, 150)
        else:
            winner_text = "PLAYER 2 WINS THE MATCH!"
            winner_color = (150, 150, 255)
        
        big_font = pygame.font.Font(None, 54)
        title = big_font.render(winner_text, True, winner_color)
        self.screen.blit(title, title.get_rect(center=(w//2, h//2 - 60)))
        
        final_font = pygame.font.Font(None, 54)
        final_score = final_font.render(f"{self.p1_rnd}  -  {self.p2_rnd}", True, (255, 215, 0))
        self.screen.blit(final_score, final_score.get_rect(center=(w//2, h//2 + 10)))
        
        rounds_font = pygame.font.Font(None, 28)
        rounds_text = rounds_font.render(f"BEST OF 5 ROUNDS", True, (200, 200, 200))
        self.screen.blit(rounds_text, rounds_text.get_rect(center=(w//2, h//2 + 60)))
        
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.003)) * 0.5 + 0.5
        color_val = max(0, min(255, int(255 * pulse)))
        continue_font = pygame.font.Font(None, 32)
        continue_text = continue_font.render("PRESS SPACE TO PLAY AGAIN", True, (color_val, color_val, 100))
        self.screen.blit(continue_text, continue_text.get_rect(center=(w//2, h//2 + 100)))
        
        quit_font = pygame.font.Font(None, 24)
        quit_text = quit_font.render("PRESS ESC TO QUIT", True, (150, 150, 150))
        self.screen.blit(quit_text, quit_text.get_rect(center=(w//2, h//2 + 140)))